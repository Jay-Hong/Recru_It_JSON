"""Actual smooth scrolling and ordering tests; no recruitment-site requests."""
from copy import deepcopy
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import Mock
from urllib.parse import quote

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import ClickNotReady, Observation, ServerUnavailable, observer_source
from recru_it.validate_run import validate
from test_attempt_stage1 import Card
from test_browser_stage1 import FIXTURE
import test_combined_pacing as combined
from test_stage1 import valid_run


class MotionBrowserTests(unittest.TestCase):
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
        self.driver.get('data:text/html;charset=utf-8,' + quote(FIXTURE))
        self.observer = Observation(self.driver, 'https://fixture.invalid')
        self.driver.execute_script(observer_source())
        self.driver.execute_script('''
            const area=document.querySelector('.scrollsection'), card=area.firstElementChild;
            area.style.cssText='height:240px;width:280px;overflow:auto;scroll-behavior:smooth';
            card.style.cssText='height:60px;width:200px';
            card.innerHTML='<span>clickable child</span>';
            for (const before of [true,false]) {
                const spacer=document.createElement('div'); spacer.style.height='30000px';
                if(before) area.prepend(spacer); else area.append(spacer);
            }
        ''')
        self.card = self.driver.find_element(By.CSS_SELECTOR, '.box.pointer')
        self.record = {'number': 1}

    def begin(self):
        self.observer.begin_movement(self.card, self.record, .2)

    def center(self):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center',inline:'nearest'})", self.card)

    def instant_center(self):
        self.driver.execute_script("document.querySelector('.scrollsection').style.scrollBehavior='auto'")
        self.center()

    def state(self):
        return self.driver.execute_script('return __recruObserver.movementStatus(1)')

    def test_far_smooth_scroll_waits_for_stable_unobstructed_center(self):
        self.begin()
        self.center()
        self.assertFalse(self.state()['ok'])
        self.observer.wait_clickable(self.record, 5)
        state = self.record['click_readiness']
        self.assertTrue(state['ok'], state)
        self.assertGreater(state['position_changes'], 3)
        self.assertGreaterEqual(state['stable_seconds'], .2)
        self.assertGreater(state['elapsed_seconds'], .3)

    def test_stability_is_already_observed_during_region_wait(self):
        self.instant_center()
        self.begin()
        time.sleep(.3)  # Simulate the already-required region/cadence wait.
        self.assertTrue(self.state()['ok'])
        self.observer.wait_clickable(self.record, 1)
        self.assertLess(self.record['click_ready_wait_seconds'], .2)

    def test_cover_disappearing_requires_a_new_clear_stability_window(self):
        self.instant_center()
        self.driver.execute_script('''
            const cover=document.createElement('div'); cover.id='cover';
            cover.style.cssText='position:fixed;inset:0;z-index:999999;background:white';
            document.body.append(cover); setTimeout(()=>cover.remove(),350);
        ''')
        self.begin()
        self.assertEqual(self.state()['reason'], 'obstructed')
        self.observer.wait_clickable(self.record, 2)
        self.assertGreater(self.record['click_readiness']['elapsed_seconds'], .45)
        self.assertGreater(self.record['click_readiness']['obstructed_samples'], 0)

    def test_slow_subpixel_movement_cannot_accumulate_unnoticed(self):
        self.instant_center()
        self.driver.execute_script('''
            const card=document.querySelector('.box.pointer'), start=performance.now(); let n=0;
            function move(){card.style.transform=`translateY(${++n * .04}px)`;
              if(performance.now()-start<2000) requestAnimationFrame(move);}
            move();
        ''')
        self.begin()
        with self.assertRaises(ClickNotReady):
            self.observer.wait_clickable(self.record, .35)
        self.assertFalse(self.record['click_readiness']['ok'])

    def test_an_observation_gap_cannot_count_as_stable_time(self):
        self.instant_center()
        self.begin()
        time.sleep(.3)
        self.assertTrue(self.state()['ok'])
        self.driver.execute_script('const start=performance.now(); while(performance.now()-start<250){}')
        self.assertFalse(self.state()['ok'])
        self.observer.wait_clickable(self.record, 1)
        self.assertGreaterEqual(self.record['click_readiness']['stable_seconds'], .2)

    def test_detached_card_is_never_ready(self):
        self.begin()
        self.driver.execute_script('arguments[0].remove()', self.card)
        with self.assertRaises(ClickNotReady):
            self.observer.wait_clickable(self.record, .2)
        self.assertEqual(self.record['click_readiness']['reason'], 'detached')


class MotionAttemptTests(unittest.TestCase):
    def setUp(self):
        # Reuse the mocked crawler setup, not the other class's test methods.
        combined.CombinedAttemptTests.setUp(self)
        self.spider.optimizations.update(salary_prefilter=False,
            click_readiness={'stable_seconds': .2, 'timeout_seconds': 5})
        self.observer.begin_movement = Mock()
        self.observer.wait_clickable = Mock()

    def collect(self, cards):
        return list(self.spider.process_region(self.region, cards, ['']*len(cards), ['서울']*len(cards), 0))

    def test_first_target_moves_before_region_wait_without_common_anchor(self):
        anchor, first, second = Card(), Card(), Card()
        events = []
        self.observer.begin_movement.side_effect = lambda card, *args: events.append(('observe', card))
        old_execute = self.spider.driver.execute_script

        def execute(script, *args):
            if 'scrollIntoView' in script:
                events.append(('scroll', args[0]))
            return old_execute(script, *args)

        def sleep(seconds, name):
            self.clock.sleep(seconds, name)
            events.append((name, seconds))

        self.spider.driver.execute_script = execute
        self.observer.sleep = sleep
        self.observer.wait_clickable.side_effect = lambda *args: events.append(('ready', None))
        first.click.side_effect = lambda: events.append(('click', first))
        second.click.side_effect = lambda: events.append(('click', second))
        self.region['sleep_before'] = (2, 2)
        result = list(self.spider.process_region(self.region, [anchor, first, second], ['', '', ''],
                                                 ['부산', '서울', '서울'], 0))
        self.assertEqual(len(result), 2)
        self.assertEqual(events[:3], [('observe', first), ('scroll', first), ('region_wait', 2)])
        self.assertEqual([value for name, value in events if name == 'scroll'], [first, second])
        self.assertEqual([a['region_first_candidate'] for a in self.observer.stats['attempts']], [True, False])
        anchor.click.assert_not_called()

    def test_extra_movement_wait_is_absorbed_and_next_click_cannot_catch_up(self):
        delays = iter([0, 3, 0])
        self.observer.wait_clickable.side_effect = lambda *args: self.clock.sleep(next(delays), 'ready')
        self.assertEqual(len(self.collect([Card(), Card(), Card()])), 3)
        gaps = [a['click_gap_seconds'] for a in self.observer.stats['attempts']]
        self.assertIsNone(gaps[0])
        self.assertAlmostEqual(gaps[1], 5.2)
        self.assertAlmostEqual(gaps[2], 2.2)

    def test_unready_target_never_clicks_retries_once_then_continues(self):
        self.observer.wait_clickable.side_effect = [ClickNotReady('moving'), ClickNotReady('obstructed'), None]
        bad, good = Card(), Card()
        self.assertEqual(len(self.collect([bad, good])), 1)
        bad.click.assert_not_called()
        good.click.assert_called_once()
        self.assertEqual(self.observer.stats['counts']['click_not_ready'], 2)
        self.assertEqual(self.observer.stats['counts']['final_failed'], 1)
        self.assertEqual(self.observer.begin_movement.call_count, 3)

    def test_first_target_label_survives_failure_before_region_wait(self):
        self.observer.begin_movement.side_effect = [WebDriverException(), WebDriverException(), None]
        self.assertEqual(len(self.collect([Card(), Card()])), 1)
        self.assertEqual([a['region_first_candidate'] for a in self.observer.stats['attempts']],
                         [True, True, False])

    def test_server_limit_during_readiness_stops_before_click_or_retry(self):
        self.observer.wait_clickable.side_effect = ServerUnavailable('429')
        card = Card()
        with self.assertRaises(ServerUnavailable):
            self.collect([card])
        card.click.assert_not_called()
        self.assertEqual(self.observer.stats['counts']['retries'], 0)


class MotionPublicationTests(unittest.TestCase):
    def test_verified_items_require_position_readiness_evidence(self):
        items, stats = valid_run()
        stats['optimizations'] = {'click_readiness': {'stable_seconds': .2, 'timeout_seconds': 5}}
        with self.assertRaises(ValueError):
            validate(items, stats, 'current')
        for attempt in stats['attempts']:
            attempt['click_readiness'] = {'ok': True}
        validate(items, stats, 'current')
        changed = deepcopy(stats)
        changed['attempts'][0]['click_readiness']['ok'] = False
        with self.assertRaises(ValueError):
            validate(items, changed, 'current')


if __name__ == '__main__':
    unittest.main()
