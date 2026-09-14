"""Boundary, recovery, and publication tests without contacting the site."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

from selenium.common.exceptions import ElementClickInterceptedException

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import EvidenceUnavailable, Observation, ObservationUnavailable, ServerUnavailable
from recru_it.pacing import StartInterval, salary_exclusion
from recru_it.spiders.recru_it import Recru_It_Spider
from recru_it.validate_run import validate
from test_attempt_stage1 import Card, Driver
from test_stage1 import valid_run


class Clock:
    now = 0

    def __call__(self):
        return self.now

    def sleep(self, seconds, name):
        self.now += seconds


class PacingTests(unittest.TestCase):
    def test_processing_is_absorbed_and_overdue_requests_never_catch_up(self):
        clock = Clock()
        pace = StartInterval((1.6, 2.8), clock.sleep, 'test', clock=clock, sample=lambda *args: 2.2)
        self.assertIsNone(pace.start())
        clock.now += .7
        self.assertAlmostEqual(pace.start(), 2.2)
        clock.now += 8
        self.assertAlmostEqual(pace.start(), 8)
        self.assertAlmostEqual(pace.start(), 2.2)

    def test_invalid_intervals_are_rejected(self):
        for interval in [(0, 2), (3, 2), (-1, 2), (1, float('inf')), (float('nan'), 2)]:
            with self.subTest(interval=interval), self.assertRaises(ValueError):
                StartInterval(interval, Mock(), 'test')


class SalaryTests(unittest.TestCase):
    def test_safe_boundary_values_and_payment_units(self):
        for unit, reason in [('1', 'low_daily_pay'), ('3', 'low_monthly_pay')]:
            for price, pay in [('100000', '10만'), ('149999', '14.9999만'), ('140,000', '14만 이상'),
                               ('120000', '12 ~ 18만')]:
                with self.subTest(unit=unit, price=price):
                    self.assertEqual(salary_exclusion({'priceDiv': unit, 'price': price, 'pay': pay}), reason)

    def test_ambiguous_mismatched_and_out_of_range_values_are_collected(self):
        entries = [None, {}, {'priceDiv': '2'}, {'priceDiv': '4'},
                   {'priceDiv': '1', 'price': '100000', 'pay': None}]
        entries += [{'priceDiv': '1', 'price': price, 'pay': pay} for price, pay in [
            ('99999', '9.9999만'), ('150000', '15만'), ('1400000', '140만'), ('13000', '1.3만'),
            ('140000', '15만'), ('140000', '14 ~ 10만'), ('140000', '14만?'),
            ('14,0000', '14만'), ('-140000', '14만'), ('', '14만'), ('140000.0', '14만')]]
        for card in entries:
            with self.subTest(card=card):
                self.assertIsNone(salary_exclusion(card))


class CombinedAttemptTests(unittest.TestCase):
    def setUp(self):
        self.spider = Recru_It_Spider.__new__(Recru_It_Spider)
        self.spider.driver = Driver()
        self.observer = self.spider.observation = Observation(self.spider.driver, 'https://ildao.com/recruit')
        self.spider._item_regions = {}
        self.spider.optimizations = {'salary_prefilter': True, 'salary_audit_rate': .2}
        self.observer.stats['prefilter'] = Counter()
        self.observer.salary_card = Mock(return_value={'priceDiv': '1', 'price': '120000', 'pay': '12만'})
        self.observer.read = Mock(return_value={'verified': True})
        self.spider.get_job_detail = Mock(return_value=('value', '서울', 'type', '일급 12만원', *([''] * 7)))
        self.clock = Clock()
        self.observer.sleep = self.clock.sleep
        self.spider.click_pacer = StartInterval((1.6, 2.8), self.clock.sleep, 'click_wait',
                                              clock=self.clock, sample=lambda *args: 2.2)
        self.region = {'name': '서울', 'keywords': ['서울'], 'sleep_before': (0, 0), 'sleep_between': (1, 1)}

    def collect(self, cards):
        with patch('recru_it.spiders.recru_it.random.random', return_value=.9):
            return list(self.spider.process_region(self.region, cards, [''] * len(cards), ['서울'] * len(cards), 0))

    def test_audit_is_verified_and_other_exclusions_do_not_click_or_enter_pipeline(self):
        first, skipped = Card(), Card()
        items = self.collect([first, skipped])
        self.assertEqual(len(items), 1)
        self.assertEqual(self.observer.stats['regions']['서울']['candidates'], 2)
        self.assertEqual(self.observer.stats['regions']['서울']['prefiltered'], 1)
        self.assertEqual(self.observer.stats['prefilter']['audit_checked'], 1)
        skipped.click.assert_not_called()
        self.observer.read.assert_called_once()

    def test_mismatched_audit_stops_before_an_unchecked_card_is_skipped(self):
        self.spider.get_job_detail.return_value = ('value', '서울', 'type', '일급 18만원', *([''] * 7))
        with self.assertRaises(ObservationUnavailable):
            self.collect([Card(), Card()])
        self.assertEqual(self.observer.stats['prefilter']['audit_mismatch'], 1)
        self.assertFalse(self.observer.stats['regions']['서울']['complete'])

    def test_missing_salary_evidence_falls_back_to_verified_collection(self):
        self.observer.salary_card.side_effect = EvidenceUnavailable('no salary evidence')
        self.assertEqual(len(self.collect([Card()])), 1)
        self.assertEqual(self.observer.stats['prefilter']['unavailable'], 1)
        self.assertEqual(self.observer.stats['prefilter']['skipped'], 0)

    def test_intercept_retry_and_next_card_use_the_same_start_interval(self):
        self.spider.optimizations['salary_prefilter'] = False
        self.assertEqual(len(self.collect([Card([ElementClickInterceptedException()]), Card()])), 2)
        self.assertEqual([a['click_gap_seconds'] for a in self.observer.stats['attempts']], [None, 2.2, 2.2])
        self.assertEqual(self.observer.stats['counts']['click_intercepted'], 1)

    def test_all_skipped_region_has_no_region_wait_or_click(self):
        self.observer.stats['prefilter']['eligible'] = 1  # An earlier region provided the first audit.
        self.assertEqual(self.collect([Card()]), [])
        self.assertEqual(self.clock.now, 0)
        self.observer.read.assert_not_called()
        self.assertTrue(self.observer.stats['regions']['서울']['complete'])

    def test_switches_disable_all_three_changes(self):
        with patch('recru_it.spiders.recru_it.CRAWL_CONFIG', {'optimizations': {
                'salary_prefilter': False, 'click_interval': None, 'scroll_interval': None}}):
            self.spider.configure_optimizations()
        self.assertIsNone(self.spider.click_pacer)
        self.assertIsNone(self.spider.scroll_pacer)
        self.collect([Card()])
        self.observer.salary_card.assert_not_called()
        self.assertEqual(self.clock.now, 1.5)


class ListReadinessTests(unittest.TestCase):
    def setUp(self):
        self.observer = Observation(Driver(), 'https://ildao.com/recruit')
        self.clock = Clock()
        self.observer.sleep = self.clock.sleep
        self.before = {'count': 15, 'modelCount': 15, 'pending': False, 'events': 0, 'complete': False}

    def wait(self, states, **kwargs):
        self.observer.list_state = Mock(side_effect=states)
        with patch('recru_it.observation.time.monotonic', self.clock):
            return self.observer.wait_list(self.before, **kwargs)

    def test_growth_waits_for_both_response_and_rendered_list(self):
        state, outcome, _ = self.wait([
            {**self.before, 'pending': True},
            {**self.before, 'modelCount': 30},
            {**self.before, 'modelCount': 30, 'count': 30, 'events': 1}])
        self.assertEqual(outcome, 'grown')
        self.assertEqual(state['count'], 30)
        self.assertAlmostEqual(self.clock.now, .2)

    def test_no_growth_is_not_end_but_first_no_request_can_warm_up(self):
        self.observer.list_state = Mock(return_value=self.before)
        with patch('recru_it.observation.time.monotonic', self.clock):
            with self.assertRaises(EvidenceUnavailable):
                self.observer.wait_list(self.before, timeout=.3)
            _, outcome, _ = self.observer.wait_list(self.before, first=True)
        self.assertEqual(outcome, 'initial_no_request')

    def test_explicit_end_and_server_limit(self):
        _, outcome, _ = self.wait([{**self.before, 'complete': True, 'events': 1}])
        self.assertEqual(outcome, 'complete')
        with self.assertRaises(ServerUnavailable):
            self.wait([ServerUnavailable('429')])

    def test_stalled_list_gets_one_recheck_without_a_second_scroll(self):
        spider = Recru_It_Spider.__new__(Recru_It_Spider)
        spider.observation = self.observer
        spider.driver = Driver()
        spider.scroll_pacer = Mock()
        self.observer.list_state = Mock(return_value=self.before)
        self.observer.wait_list = Mock(side_effect=EvidenceUnavailable('stalled'))
        with self.assertRaises(ObservationUnavailable):
            spider.scroll_list([Card()], 3)
        self.assertEqual(self.observer.wait_list.call_count, 2)
        spider.scroll_pacer.start.assert_called_once()
        self.assertEqual(self.observer.stats['list_collection']['completed'], 0)


class CombinedPublicationTests(unittest.TestCase):
    def test_skipped_items_require_a_complete_consistent_audit(self):
        items, stats = valid_run()
        stats['regions']['서울'].update(candidates=54, prefiltered=4)
        stats['optimizations'] = {'salary_prefilter': True}
        stats['prefilter'] = {'skipped': 4, 'low_daily_pay': 4, 'eligible': 5,
                              'audit_selected': 1, 'audit_checked': 1}
        validate(items, stats, 'current')
        for change in [{'audit_mismatch': 1}, {'audit_failed': 1}, {'audit_checked': 0},
                       {'eligible': 4}, {'low_daily_pay': 3}, {'skipped': 3}]:
            changed = deepcopy(stats)
            changed['prefilter'].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate(items, changed, 'current')

    def test_unfinished_scroll_cannot_publish_even_when_item_count_is_large(self):
        items, stats = valid_run()
        stats['optimizations'] = {'scroll_interval': [1.5, 2.5]}
        stats['list_collection'] = {'planned': 2, 'completed': 1, 'ended': False}
        stats['scrolls'] = [{'outcome': 'grown'}]
        with self.assertRaises(ValueError):
            validate(items, stats, 'current')
        stats['list_collection']['ended'] = True
        validate(items, stats, 'current')
