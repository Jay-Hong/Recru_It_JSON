"""Bounded list loading: preserve readiness and stop viewport-triggered chaining."""
from copy import deepcopy
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import Mock, patch
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import EvidenceUnavailable, Observation, observer_source
from recru_it.settings import CRAWL_CONFIG
from recru_it.validate_run import validate
from test_attempt_stage1 import Driver
from test_combined_pacing import Clock
from test_stage1 import valid_run

LIMITS = CRAWL_CONFIG['optimizations']['list_readiness']


class BoundedReadinessTests(unittest.TestCase):
    def setUp(self):
        self.obs = Observation(Driver(), 'https://fixture.invalid')
        self.clock = Clock()
        self.obs.sleep = self.clock.sleep
        self.obs.park_list = Mock()
        self.before = dict(count=15, modelCount=15, events=0, complete=False,
                           pending=False, networkPending=0, loadFlag=False, requestsStarted=1)
        self.record = {}
        self.budget = dict(started=0, initial_requests=1, max_requests=62)

    def wait(self, state, **kwargs):
        self.obs.list_state = Mock(side_effect=state) if callable(state) else Mock(return_value=state)
        with patch('recru_it.observation.time.monotonic', self.clock):
            return self.obs.wait_list_bounded(self.before, self.record, LIMITS, self.budget, **kwargs)

    def test_park_on_request_start_but_wait_for_model_and_render_and_stability(self):
        def state():
            if self.clock.now < .2:
                return {**self.before, 'requestsStarted': 2, 'pending': True, 'networkPending': 1}
            if self.clock.now < .4:
                return {**self.before, 'requestsStarted': 2, 'modelCount': 30, 'loadFlag': True, 'pending': True}
            return {**self.before, 'requestsStarted': 2, 'modelCount': 30, 'count': 30, 'events': 1}
        result, outcome, seconds = self.wait(state)
        self.assertEqual(outcome, 'grown')
        self.assertEqual(result['count'], 30)
        self.assertGreaterEqual(seconds, .6)
        self.obs.park_list.assert_called_once()
        self.assertEqual(self.record['parked_after_seconds'], 0)

    def test_load_flag_alone_cannot_be_treated_as_ready(self):
        with self.assertRaisesRegex(EvidenceUnavailable, 'stalled'):
            self.wait({**self.before, 'count': 30, 'modelCount': 30, 'events': 1,
                       'pending': True, 'networkPending': 0, 'loadFlag': True})
        self.obs.park_list.assert_called_once()

    def test_continuous_progress_still_has_a_total_deadline(self):
        def state():
            n = int(self.clock.now)
            return {**self.before, 'count': 30 + n, 'modelCount': 30 + n,
                    'pending': True, 'requestsStarted': 2, 'networkPending': 1}
        with self.assertRaisesRegex(EvidenceUnavailable, 'list_scroll_timeout'):
            self.wait(state)
        self.assertLess(self.clock.now, 10.2)

    def test_request_limit_is_failure_even_when_new_cards_are_ready(self):
        for requests, reason in [(6, 'budget'), (0, 'regressed')]:
            with self.subTest(requests=requests), self.assertRaisesRegex(EvidenceUnavailable, reason):
                self.wait({**self.before, 'requestsStarted': requests, 'count': 30, 'modelCount': 30})
        self.obs.park_list.assert_not_called()

    def test_whole_collection_budget_and_deadline(self):
        self.budget['max_requests'] = 0
        with self.assertRaisesRegex(EvidenceUnavailable, 'budget'):
            self.wait({**self.before, 'requestsStarted': 2})
        self.budget['max_requests'] = 62
        self.clock.now = LIMITS['total_seconds']
        with self.assertRaisesRegex(EvidenceUnavailable, 'collection_timeout'):
            self.wait(self.before)

    def test_initial_no_request_is_allowed_only_for_first_scroll(self):
        _, outcome, _ = self.wait(self.before, first=True)
        self.assertEqual(outcome, 'initial_no_request')
        self.obs.park_list.assert_not_called()
        with self.assertRaisesRegex(EvidenceUnavailable, 'stalled'):
            self.wait(self.before)

    def test_explicit_empty_end_still_requires_no_pending_request(self):
        self.before.update(count=0, modelCount=0)
        _, outcome, _ = self.wait({**self.before, 'complete': True})
        self.assertEqual(outcome, 'complete')
        self.obs.park_list.assert_called_once()

    def test_shrinking_list_is_not_published_as_progress(self):
        with self.assertRaisesRegex(EvidenceUnavailable, 'regressed'):
            self.wait({**self.before, 'count': 0, 'modelCount': 0, 'complete': True})


class BoundedPublicationTests(unittest.TestCase):
    def test_pending_hidden_over_budget_or_missing_final_evidence_blocks_publication(self):
        items, stats = valid_run()
        stats['optimizations'] = {'scroll_interval': [1.5, 2.5], 'list_readiness': LIMITS}
        stats['scrolls'] = [{'outcome': 'grown'}]
        stats['list_collection'] = {'planned': 1, 'completed': 1, 'ended': False, 'readiness_version': 1,
                                   'requests': 1, 'max_requests': 9,
                                   'final_state': {'count': 50, 'modelCount': 50, 'pending': False},
                                   'inventory': {'count': 50, 'hidden': 0}}
        validate(items, stats, 'current')
        for field, changes in [('final_state', {'pending': True}), ('final_state', {'modelCount': 49}),
                               ('inventory', {'hidden': 1}), ('inventory', {'count': 49}),
                               (None, {'requests': 10}), (None, {'final_state': {}})]:
            changed = deepcopy(stats)
            target = changed['list_collection'] if field is None else changed['list_collection'][field]
            target.update(changes)
            with self.subTest(field=field, changes=changes), self.assertRaises(ValueError):
                validate(items, changed, 'current')


PAGE = '''<style>.scrollsection{height:250px;overflow:auto;scroll-behavior:smooth}.box{height:180px}</style>
<div id="owner"><div class="scrollsection"></div></div>
<script>
const list=document.querySelector('.scrollsection');
window.vm={$el:document.querySelector('#owner'),recuitDetail:{},normalRecruList:[],emergenRecruList:[],loadFlag:false,
 $events:{$on:(name,fn)=>{window.listEvent=fn;}}};vm.$el.__vue__=vm;
function append(){for(let i=0;i<3;i++){const c=document.createElement('div');c.className='box pointer';
 c.innerHTML='<div class="sub_info foot"><div class="ft12">location_on 서울</div></div>';list.append(c);vm.normalRecruList.push({idx:vm.normalRecruList.length});}}
append();
class FakeXHR extends EventTarget {open(){} send(){setTimeout(()=>{this.status=200;this.onload();this.dispatchEvent(new Event('loadend'));},300);}}
window.XMLHttpRequest=FakeXHR;
window.posts=0;
window.load=()=>{if(vm.loadFlag)return;vm.loadFlag=true;posts++;const x=new XMLHttpRequest();
 x.open('POST','https://fixture.invalid/web/Jobinfo/getJobBoardList');x.onload=()=>{
 const atEnd=list.scrollTop+list.clientHeight>=list.scrollHeight-10;append();vm.loadFlag=false;if(window.listEvent)listEvent('loaded');
 if(atEnd){list.scrollTop=list.scrollHeight;if(posts<8)load();}};x.send('{}');};
</script>'''


class BrowserListSettlingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1600,1000')
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get('data:text/html;charset=utf-8,' + quote(PAGE))
        self.obs = Observation(self.driver, 'https://fixture.invalid')
        self.driver.execute_script(observer_source())

    def test_parking_stops_automatic_chaining_without_cancelling_response(self):
        before = self.obs.list_state()
        self.driver.execute_script("list.scrollTo({top:list.scrollHeight,behavior:'instant'});load()")
        record = {}
        state, outcome, _ = self.obs.wait_list_bounded(before, record, LIMITS,
            {'initial_requests': before['requestsStarted'], 'started': time.monotonic(), 'max_requests': 10})
        settled_posts = self.driver.execute_script('return posts')
        time.sleep(.4)
        self.assertLessEqual(settled_posts, 2)  # An already-started continuation may finish.
        self.assertEqual(self.driver.execute_script('return posts'), settled_posts)
        self.assertEqual(state['count'], 3 + settled_posts * 3)
        self.assertEqual(outcome, 'grown')
        self.assertFalse(state['pending'])
        self.assertEqual(self.obs.list_inventory(), {'count': state['count'], 'hidden': 0, 'empty_site': 0})
        self.assertTrue(self.driver.execute_script(
            'return list.scrollHeight-list.clientHeight-list.scrollTop > list.clientHeight'))

    def test_fixture_chains_when_viewport_remains_at_the_loader(self):
        self.obs.list_state()
        self.driver.execute_script("list.scrollTo({top:list.scrollHeight,behavior:'instant'});load()")
        time.sleep(1)
        self.assertGreaterEqual(self.driver.execute_script('return posts'), 2)

    def test_hidden_cards_are_counted_separately_from_empty_region_text(self):
        self.driver.execute_script("list.children[0].style.display='none';list.children[1].querySelector('.ft12').textContent=''")
        self.assertEqual(self.obs.list_inventory(), {'count': 3, 'hidden': 1, 'empty_site': 1})
