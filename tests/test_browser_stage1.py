"""Synthetic browser regression cases; no requests to the recruitment site."""
import io
import logging
from pathlib import Path
import sys
import time
import unittest
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import observer_source, quiet_browser_logging


FIXTURE = r'''
<style>p {white-space: pre-line} .pointer {cursor:pointer}</style>
<div id="owner"><div class="scrollsection"><div class="box pointer">test card</div></div>
<div id="detail_info"><div><div><div>
<div id="title" class="ft5 NotoSansM"></div>
<div id="site" class="time ft11 col_gra04 NotoSansL"></div>
<div class="ft11">
  <div id="type" class="ft10"></div>
  <div class="col_blu02 ft10"><div><div>일급</div><span>170,000 원</span></div></div>
  <div id="sex" class="ft11 col_blu02">남성</div>
  <div id="people" class="ft10" style="display: flex;"><div>초보</div><div>&nbsp;2명</div></div>
  <div id="manager" class="ft10" style="display: flex;">담당자</div>
  <div id="phone" class="ft10 RobotoM"></div>
</div>
<div id="conditions" class="ft11 col_blu02">숙식제공</div>
<div id="image"></div><p id="body" class="ft10 lin_h2"></p>
</div></div></div></div></div>
<script>
class FakeXHR extends EventTarget {
  open() {}
  send() { setTimeout(() => { this.status = window.responseStatus || 200; this.onload(); this.dispatchEvent(new Event('loadend')); }, 20); }
}
window.XMLHttpRequest = FakeXHR;
const el = id => document.getElementById(id);
const model = (idx, content) => ({idx, title: '테스트 공고', locNm:'서울',locDetailNm:'강남구',
  cateNm:'조공',priceDiv:'1',pricepub:'170,000 원',sex:'M',workDiv:'99',gongDiv:['0'],workNum:['2'],
  manager:'담당자',phone:'010-0000-0000',content,workcatelist:['숙식제공'],recuritImg:''});
window.currentModel = model('new', '첫째 줄\n\u00a0둘째 줄\u00a0\n\n셋째 줄'.replaceAll('\\n','\n'));
window.vm = {$el:el('owner'), recuitDetail:model('old','이전 본문'),normalRecruList:[{idx:'new'}],emergenRecruList:[],
  $global:{isEmpty: value => !value}, $config:{getS3Prefix:()=> 'https://images.invalid'},
  _vnode:{children:[{key:'normalRecruList0',elm:document.querySelector('.box.pointer')}]}};
el('owner').__vue__ = vm;
window.render = () => {
  for(const [id,value] of Object.entries({title:vm.recuitDetail.title,site:'location_on 서울 강남구',
    type:'조공',phone:vm.recuitDetail.phone,body:vm.recuitDetail.content})) el(id).textContent=value;
};
render();
window.partial = false; window.reuse = false;
document.querySelector('.box.pointer').onclick = () => {
  const xhr = new XMLHttpRequest(); xhr.open('POST','https://fixture.invalid/web/Jobinfo/getBoardJobDetail');
  xhr.onload = () => { if (xhr.status !== 200) return; if (!reuse) vm.recuitDetail = {...currentModel}; if (!partial) render(); };
  xhr.send(JSON.stringify({idx:'new'}));
};
</script>
'''


class BrowserVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1600,1000')
        cls.driver = webdriver.Chrome(options=options)
        # Block downloads in this entirely synthetic fixture, including image URLs.
        cls.driver.execute_cdp_cmd('Network.enable', {})
        cls.driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ['https://*.invalid/*']})

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get('data:text/html;charset=utf-8,' + quote(FIXTURE))
        self.driver.execute_script('currentModel.content = arguments[0]',
                                   '첫째 줄\n \u00a0둘째 줄\u00a0 \n\n셋째 줄')
        self.driver.execute_script(observer_source())

    def click(self, number=1):
        card = self.driver.find_element(By.CSS_SELECTOR, '.box.pointer')
        self.driver.execute_script('return __recruObserver.arm(arguments[0],arguments[1])', card, number)
        card.click()
        time.sleep(.15)
        return self.driver.execute_script('return __recruObserver.snapshot()')

    def test_ready_time_is_observed_before_half_second_and_text_matches(self):
        snapshot = self.click()
        self.assertTrue(snapshot['ok'], snapshot)
        timing = self.driver.execute_script('return __recruObserver.summary().attempt.readySeconds')
        self.assertGreater(timing, 0)
        self.assertLess(timing, .5)
        for name in ('detail', 'people'):
            selector = self.driver.execute_script('return __recruObserver.selectors[arguments[0]]', name)
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            legacy = elements[0].text if name == 'detail' else [element.text for element in elements]
            self.assertEqual(snapshot['raw'][name], legacy)

    def test_new_id_with_old_body_is_rejected(self):
        self.driver.execute_script('partial=true')
        snapshot = self.click()
        self.assertFalse(snapshot['ok'])
        self.assertIn('detail', snapshot['mismatches'])
        self.driver.execute_script('render()')
        self.assertTrue(self.driver.execute_script('return __recruObserver.snapshot().ok'))

    def test_list_end_requires_explicit_event_and_reports_pending_render(self):
        self.driver.execute_script('''
            vm.$events = {$on: (name, fn) => { window.listEvent = fn; }};
            vm.loadFlag = false;
        ''')
        state = self.driver.execute_script('return __recruObserver.listState()')
        self.assertFalse(state['complete'])
        self.assertEqual(state['events'], 0)
        self.driver.execute_script("listEvent('loaded'); vm.loadFlag=true")
        state = self.driver.execute_script('return __recruObserver.listState()')
        self.assertFalse(state['complete'])
        self.assertTrue(state['pending'])
        self.driver.execute_script("listEvent('complete'); vm.loadFlag=false")
        state = self.driver.execute_script('return __recruObserver.listState()')
        self.assertTrue(state['complete'])
        self.assertFalse(state['pending'])
        self.assertEqual(state['events'], 2)

    def test_salary_metadata_uses_the_selected_cards_render_identity(self):
        self.driver.execute_script('''
            const old=document.querySelector('.box.pointer');
            old.innerHTML='<div class="sub_info foot"><div><div>12만</div></div></div>';
            const second=old.cloneNode(true); old.parentElement.prepend(second);
            second.querySelector('.foot > div > div').textContent='14만';
            vm.normalRecruList=[{idx:'first',priceDiv:'1',price:'120000'},
                               {idx:'second',priceDiv:'2',price:'140000'}];
            vm._vnode.children.push({key:'normalRecruList1',elm:second});
        ''')
        card = self.driver.find_element(By.CSS_SELECTOR, '.box.pointer')
        metadata = self.driver.execute_script('return __recruObserver.salaryCard(arguments[0])', card)
        self.assertEqual(metadata, {'priceDiv': '2', 'price': '140000', 'pay': '14만'})

    def test_same_id_retry_requires_a_new_detail_object(self):
        self.assertTrue(self.click()['ok'])
        self.driver.execute_script('reuse=true')
        snapshot = self.click(2)
        self.assertFalse(snapshot['ok'])
        self.assertEqual(snapshot['reason'], 'identity')

    def test_summary_returns_only_requested_attempt_after_same_job_retry(self):
        self.assertTrue(self.click(1)['ok'])
        self.assertTrue(self.click(2)['ok'])
        previous = self.driver.execute_script('return __recruObserver.summary(1).requests')
        current = self.driver.execute_script('return __recruObserver.summary(2).requests')
        self.assertEqual([r['attempt'] for r in previous], [1])
        self.assertEqual([r['attempt'] for r in current], [2])
        self.assertNotEqual(previous[0]['sequence'], current[0]['sequence'])

    def test_debug_crawler_logging_does_not_expose_browser_script_payload(self):
        root = logging.getLogger()
        transport = logging.getLogger('selenium.webdriver.remote.remote_connection')
        names = ['selenium', transport.name, 'urllib3', 'urllib3.connectionpool']
        levels = {name: logging.getLogger(name).level for name in names}
        root_level = root.level
        output = io.StringIO()
        handler = logging.StreamHandler(output)
        root.addHandler(handler)
        try:
            root.setLevel(logging.DEBUG)
            transport.setLevel(logging.DEBUG)
            # Confirm this test captures the real WebDriver DEBUG response path.
            self.driver.execute_script('return arguments[0]', 'unprotected-fixture-value')
            self.assertIn('unprotected-fixture-value', output.getvalue())
            output.seek(0)
            output.truncate(0)
            quiet_browser_logging()
            value = self.driver.execute_script('return arguments[0]', 'private-fixture-value')
            self.assertEqual(value, 'private-fixture-value')
            logging.getLogger('recru-test').debug('crawler diagnostic remains enabled')
            self.assertNotIn('private-fixture-value', output.getvalue())
            self.assertIn('crawler diagnostic remains enabled', output.getvalue())
        finally:
            root.removeHandler(handler)
            root.setLevel(root_level)
            for name, level in levels.items():
                logging.getLogger(name).setLevel(level)

    def test_retry_cannot_start_while_previous_request_is_pending(self):
        self.driver.execute_script('''
            const xhr = new XMLHttpRequest();
            xhr.open('POST', 'https://fixture.invalid/web/Jobinfo/getBoardJobDetail');
            xhr.onload = () => {};
            xhr.send(JSON.stringify({idx:'new'}));
            // Attempt in the same task, before the response can arrive.
            try { __recruObserver.arm(document.querySelector('.box.pointer'), 1); window.armBlocked=false; }
            catch (_) { window.armBlocked=true; }
        ''')
        self.assertTrue(self.driver.execute_script('return armBlocked'))

    def test_page_response_status_still_stops_when_network_logs_are_missing(self):
        self.driver.execute_script('responseStatus=429')
        snapshot = self.click()
        self.assertFalse(snapshot['ok'])
        self.assertEqual(snapshot['reason'], 'source_unavailable')

    def test_same_title_on_different_ids_is_valid(self):
        self.assertTrue(self.click()['ok'])

    def test_emergency_card_uses_numeric_render_key(self):
        self.driver.execute_script('vm.emergenRecruList=vm.normalRecruList; vm.normalRecruList=[]; vm._vnode.children[0].key=0')
        self.assertTrue(self.click()['ok'])

    def test_condition_text_preserves_spaces_inside_a_multiline_text_node(self):
        self.driver.execute_script('''
            currentModel.workcatelist = ['숙식 \\n제공', '4대보험'];
            document.getElementById('conditions').style.whiteSpace = 'pre-line';
            document.getElementById('conditions').innerHTML = ' 숙식 \\n제공<span>,</span>';
            const other = document.createElement('div'); other.className='ft11 col_blu02';
            other.textContent=' 4대보험'; document.getElementById('conditions').after(other);
        ''')
        snapshot = self.click()
        self.assertTrue(snapshot['ok'], snapshot)
        legacy = [element.text for element in self.driver.find_elements(By.CSS_SELECTOR, '#detail_info div.ft11.col_blu02')]
        self.assertEqual(snapshot['raw']['etcs'], legacy)

    def test_condition_clipped_by_ancestor_matches_webdriver_visibility(self):
        self.driver.execute_script('''
            const el=document.getElementById('conditions'), wrapper=document.createElement('div');
            wrapper.style.cssText='height:1px;width:1px;overflow:hidden;position:relative';
            el.replaceWith(wrapper); wrapper.appendChild(el); el.style.cssText='position:absolute;left:20px;top:20px';
        ''')
        snapshot = self.click()
        self.assertTrue(snapshot['ok'], snapshot)
        legacy = [element.text for element in self.driver.find_elements(By.CSS_SELECTOR, '#detail_info div.ft11.col_blu02')]
        self.assertEqual(snapshot['raw']['etcs'], legacy)

    def test_image_requires_full_matching_url_but_not_download_completion(self):
        self.assertTrue(self.click()['ok'])
        self.driver.execute_script("vm.recuitDetail.recuritImg='jobs/한글.png'; document.getElementById('image').innerHTML='<img src=\"https://wrong.invalid/jobs/%ED%95%9C%EA%B8%80.png\">'")
        snapshot = self.driver.execute_script('return __recruObserver.snapshot()')
        self.assertFalse(snapshot['ok'])
        self.assertIn('imageURL', snapshot['mismatches'])
        self.driver.execute_script("document.querySelector('#image img').src='https://images.invalid/jobs/%ED%95%9C%EA%B8%80.png'")
        self.assertTrue(self.driver.execute_script('return __recruObserver.snapshot().ok'))


if __name__ == '__main__':
    unittest.main()
