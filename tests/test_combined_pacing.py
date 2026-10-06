"""Boundary, recovery, and publication tests without contacting the site."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import EvidenceUnavailable, Observation, ObservationUnavailable, ServerUnavailable
from recru_it.pacing import SalaryAudit, StartInterval, salary_audit_problems, salary_exclusion
from recru_it.spiders.recru_it import Recru_It_Spider
from recru_it.validate_run import report_quality, validate
from test_attempt_stage1 import Card, Driver
from test_stage1 import valid_run


DAILY = {'priceDiv': '1', 'price': '120000', 'pay': '12만'}


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
        self.observer.stats['optimizations'] = self.spider.optimizations
        self.spider.salary_audit = SalaryAudit(self.observer.stats, .2)
        self.observer.salary_card = Mock(return_value=DAILY)
        self.observer.read = Mock(return_value={'verified': True})
        self.spider.get_job_detail = Mock(return_value=('value', '서울', 'type', '일급 12만원', *([''] * 7)))
        self.clock = Clock()
        self.observer.sleep = self.clock.sleep
        self.spider.click_pacer = StartInterval((1.6, 2.8), self.clock.sleep, 'click_wait',
                                              clock=self.clock, sample=lambda *args: 2.2)
        self.region = {'name': '서울', 'keywords': ['서울'], 'sleep_before': (0, 0), 'sleep_between': (1, 1)}

    def collect(self, cards, name='서울', draws=None):
        region = dict(self.region, name=name)
        draw = {'side_effect': draws} if draws else {'return_value': .9}
        with patch('recru_it.spiders.recru_it.random.random', **draw):
            return list(self.spider.process_region(region, cards, [''] * len(cards), ['서울'] * len(cards), 0))

    def ledger(self, reason='low_daily_pay'):
        return self.observer.stats['prefilter_by_reason'][reason]

    def selections(self):
        return [(event['selection'], event['outcome']) for event in self.observer.stats['prefilter_events']]

    def assert_publishable_ledger(self):
        self.assertEqual(salary_audit_problems(self.observer.stats), [])

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

    def test_stale_card_salary_read_is_unavailable_evidence_but_a_lost_page_stops(self):
        observer = Observation(Driver(), 'https://ildao.com/recruit')
        observer.driver.execute_script = Mock(side_effect=[StaleElementReferenceException('private'),
                                                           {'available': True}])
        with self.assertRaises(EvidenceUnavailable):
            observer.salary_card(Card())
        observer.driver.execute_script = Mock(side_effect=[StaleElementReferenceException('private'),
                                                           {'available': False}])
        with self.assertRaises(ObservationUnavailable):
            observer.salary_card(Card())

    def test_intercept_retry_and_next_card_use_the_same_start_interval(self):
        self.spider.optimizations['salary_prefilter'] = False
        self.assertEqual(len(self.collect([Card([ElementClickInterceptedException()]), Card()])), 2)
        self.assertEqual([a['click_gap_seconds'] for a in self.observer.stats['attempts']], [None, 2.2, 2.2])
        self.assertEqual(self.observer.stats['counts']['click_intercepted'], 1)

    def test_all_skipped_region_has_no_region_wait_or_click(self):
        self.collect([Card()], name='경기')  # An earlier region provided the first audit.
        self.observer.read.reset_mock()
        started = self.clock.now
        self.assertEqual(self.collect([Card()]), [])
        self.assertEqual(self.clock.now, started)
        self.observer.read.assert_not_called()
        self.assertTrue(self.observer.stats['regions']['서울']['complete'])
        self.assert_publishable_ledger()

    def test_unverifiable_audit_is_replaced_by_the_next_card_before_any_skip(self):
        failing, replacement, skipped = Card([ElementClickInterceptedException()] * 2), Card(), Card()
        self.assertEqual(len(self.collect([failing, replacement, skipped])), 1)
        self.assertEqual(self.selections(), [('initial', 'failed'), ('replacement', 'checked'), ('skip', 'skipped')])
        replacement.click.assert_called_once()
        skipped.click.assert_not_called()
        self.assertEqual(self.ledger()['audit_replacements'], 1)
        self.assertEqual(self.ledger()['audit_replacement_pending'], 0)
        self.assertEqual(self.observer.stats['regions']['서울']['failed'], 1)
        attempts = self.observer.stats['attempts']
        self.assertEqual([a['salary_audit'] for a in attempts], ['initial', 'initial', 'replacement'])
        self.assertEqual([a['salary_eligible_number'] for a in attempts], [1, 1, 2])
        self.assert_publishable_ledger()

    def test_consecutive_unverifiable_audits_keep_one_pending_replacement(self):
        cards = [Card([ElementClickInterceptedException()] * 2) for _ in range(2)] + [Card(), Card()]
        self.collect(cards)
        self.assertEqual(self.selections(), [('initial', 'failed'), ('replacement', 'failed'),
                                             ('replacement', 'checked'), ('skip', 'skipped')])
        self.assertEqual(self.ledger()['audit_failed'], 2)
        self.assertEqual(self.ledger()['audit_replacements'], 2)
        self.assert_publishable_ledger()

    def test_failed_random_audit_at_the_end_is_reported_as_pending(self):
        cards = [Card(), Card([ElementClickInterceptedException()] * 2)]
        self.collect(cards, draws=[.1])
        self.assertEqual(self.selections(), [('initial', 'checked'), ('random', 'failed')])
        self.assertEqual(self.ledger()['audit_replacement_pending'], 1)
        self.assert_publishable_ledger()
        self.observer.stats['attempts'] = [{'outcome': 'verified'}]
        output = io.StringIO()
        with redirect_stdout(output):
            report_quality(self.observer.stats)
        self.assertIn('unverifiable salary audits: 1 (replaced: 0, pending at end: 1)', output.getvalue())

    def test_replacement_debt_carries_into_the_next_region(self):
        self.collect([Card([ElementClickInterceptedException()] * 2)], name='경기')
        replacement = Card()
        self.collect([replacement])
        replacement.click.assert_called_once()
        self.assertEqual(self.selections(), [('initial', 'failed'), ('replacement', 'checked')])
        self.assertEqual([e['region'] for e in self.observer.stats['prefilter_events']], ['경기', '서울'])
        self.assert_publishable_ledger()

    def test_daily_and_monthly_audits_are_independent(self):
        monthly = {'priceDiv': '3', 'price': '120000', 'pay': '12만'}
        self.observer.salary_card.side_effect = [DAILY, monthly, monthly, DAILY]
        self.spider.get_job_detail.side_effect = [
            ('value', '서울', 'type', '월급 12만원', *([''] * 7)),
            ('value', '서울', 'type', '일급 12만원', *([''] * 7))]
        cards = [Card([ElementClickInterceptedException()] * 2), Card(), Card(), Card()]
        self.collect(cards)
        self.assertEqual([(e['reason'], e['selection'], e['outcome'])
                          for e in self.observer.stats['prefilter_events']], [
            ('low_daily_pay', 'initial', 'failed'), ('low_monthly_pay', 'initial', 'checked'),
            ('low_monthly_pay', 'skip', 'skipped'), ('low_daily_pay', 'replacement', 'checked')])
        self.assertEqual(self.observer.stats['prefilter']['low_monthly_pay'], 1)
        self.assertEqual(self.observer.stats['prefilter']['low_daily_pay'], 0)
        self.assert_publishable_ledger()

    def test_retry_success_is_a_checked_audit_without_replacement_debt(self):
        self.collect([Card([ElementClickInterceptedException()]), Card()])
        self.assertEqual(self.selections(), [('initial', 'checked'), ('skip', 'skipped')])
        self.assertEqual(self.ledger()['audit_failed'], 0)
        self.assert_publishable_ledger()

    def test_replacement_mismatch_still_stops_the_run(self):
        self.spider.get_job_detail.return_value = ('value', '서울', 'type', '일급 18만원', *([''] * 7))
        with self.assertRaises(ObservationUnavailable):
            self.collect([Card([ElementClickInterceptedException()] * 2), Card(), Card()])
        self.assertEqual(self.selections(), [('initial', 'failed'), ('replacement', 'mismatch')])
        self.assertEqual(self.observer.stats['prefilter']['audit_mismatch'], 1)
        self.assertTrue(salary_audit_problems(self.observer.stats))

    def test_runs_without_low_pay_cards_have_an_empty_publishable_ledger(self):
        self.observer.salary_card.return_value = {'priceDiv': '1', 'price': '180000', 'pay': '18만'}
        self.assertEqual(len(self.collect([Card(), Card()])), 2)
        self.assertEqual(self.observer.stats['prefilter_events'], [])
        self.assertEqual(self.observer.stats['salary_audit_version'], 2)
        self.assert_publishable_ledger()

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

    def test_growing_list_with_pending_requests_records_timeout_without_relaxing_readiness(self):
        state = {**self.before, 'count': 855, 'modelCount': 855, 'events': 56,
                 'pending': True, 'unexpected_payload': 'private-fixture'}
        self.observer.list_state = Mock(return_value=state)
        with patch('recru_it.observation.time.monotonic', self.clock):
            with self.assertRaises(EvidenceUnavailable):
                self.observer.wait_list(self.before, timeout=.3)
        record = self.observer.stats['list_timeouts'][0]
        self.assertEqual(record['before_count'], self.before['count'])
        self.assertGreaterEqual(record['seconds'], .3)
        self.assertEqual(record['state']['count'], 855)
        self.assertTrue(record['state']['pending'])
        self.assertFalse(record['state']['complete'])
        self.assertNotIn('private-fixture', str(self.observer.stats))

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


DAY = 'low_daily_pay'
# (reason, random draw when consulted, outcome of a selected audit)
REPLACED = [(DAY, None, 'failed'), (DAY, None, 'checked'), (DAY, .9, None), (DAY, .9, None),
            (DAY, .1, 'checked'), (DAY, .9, None)]
TRAILING = [(DAY, None, 'checked'), (DAY, .9, None), (DAY, .1, 'failed')]


def audited_run(plan):
    """A publishable run whose salary ledger is produced by the spider's SalaryAudit."""
    items, stats = valid_run()
    stats['optimizations'] = {'salary_prefilter': True}
    audit = SalaryAudit(stats, .2)
    for reason, draw, outcome in plan:
        event = audit.select(reason, '서울', lambda: draw)
        if event['outcome'] is None:
            audit.finish(event, outcome)
    failed, skipped = audit.total['audit_failed'], audit.total['skipped']
    stats['regions']['서울'].update(candidates=50 + failed + skipped, failed=failed, prefiltered=skipped)
    stats['counts']['final_failed'] = failed
    return items, stats


class CombinedPublicationTests(unittest.TestCase):
    def test_replaced_and_trailing_unverifiable_audits_can_publish(self):
        for plan in (REPLACED, TRAILING):
            items, stats = audited_run(plan)
            with self.subTest(plan=plan):
                validate(items, stats, 'current')
                validate(items, json.loads(json.dumps(stats, ensure_ascii=False)), 'current')

    def test_inconsistent_audit_counters_block_publication(self):
        def both(key, value):
            return lambda stats: (stats['prefilter_by_reason'][DAY].__setitem__(key, value),
                                  stats['prefilter'].__setitem__(key, value))
        def move_failure_out_of_final_failures(stats):
            stats['counts']['final_failed'] = 0
            stats['regions']['서울'].update(failed=0, candidates=stats['regions']['서울']['candidates'] - 1)
        changes = {
            'unreplaced failure': both('audit_replacements', 0),
            'mismatch': both('audit_mismatch', 1),
            'second pending': both('audit_replacement_pending', 2),
            'negative': both('eligible', -1),
            'boolean': both('audit_checked', True),
            'reason total': lambda stats: stats['prefilter'].__setitem__(DAY, 2),
            'aggregate': lambda stats: stats['prefilter'].__setitem__('skipped', 4),
            'aggregate failed': lambda stats: stats['prefilter'].__setitem__('audit_failed', 0),
            'aggregate pending': lambda stats: stats['prefilter'].__setitem__('audit_replacement_pending', 1),
            'aggregate checked': lambda stats: stats['prefilter'].__setitem__('audit_checked', 3),
            'aggregate replacements': lambda stats: stats['prefilter'].__setitem__('audit_replacements', 0),
            'audit failure not counted as a final failure': move_failure_out_of_final_failures,
        }
        for name, change in changes.items():
            items, stats = audited_run(REPLACED)
            change(stats)
            with self.subTest(name), self.assertRaises(ValueError):
                validate(items, stats, 'current')

    def test_event_order_must_follow_the_selection_rules(self):
        def skip_while_replacement_is_owed(stats):
            events = stats['prefilter_events']
            events[1], events[2] = events[2], events[1]
            for number, event in enumerate(events, 1):
                event['n'] = number
        changes = {
            'skip while owed': skip_while_replacement_is_owed,
            'unfinished audit': lambda stats: stats['prefilter_events'][-2].__setitem__('outcome', None),
            'mismatch event': lambda stats: stats['prefilter_events'][1].__setitem__('outcome', 'mismatch'),
            'skip with audit outcome': lambda stats: stats['prefilter_events'][2].__setitem__('outcome', 'checked'),
            'unfinished skip': lambda stats: stats['prefilter_events'][2].__setitem__('outcome', None),
            'number gap': lambda stats: stats['prefilter_events'][0].__setitem__('n', 5),
            'unknown region': lambda stats: stats['prefilter_events'][2].__setitem__('region', '없음'),
            'other region': lambda stats: stats['prefilter_events'][2].__setitem__('region', '경기'),
            'random without check': lambda stats: stats['prefilter_events'][1].__setitem__('selection', 'random'),
            'missing events': lambda stats: stats.pop('prefilter_events'),
            'events not a list': lambda stats: stats.__setitem__('prefilter_events', {}),
        }
        for name, change in changes.items():
            items, stats = audited_run(REPLACED)
            change(stats)
            with self.subTest(name), self.assertRaises(ValueError):
                validate(items, stats, 'current')

    def test_skip_without_a_checked_audit_blocks_publication(self):
        items, stats = valid_run()
        stats['optimizations'] = {'salary_prefilter': True}
        SalaryAudit(stats, .2)
        stats['prefilter_by_reason'][DAY].update(eligible=1, skipped=1)
        stats['prefilter'].update(eligible=1, skipped=1, low_daily_pay=1)
        stats['prefilter_events'].append({'n': 1, 'reason': DAY, 'region': '서울',
                                          'selection': 'skip', 'outcome': 'skipped'})
        stats['regions']['서울'].update(candidates=51, prefiltered=1)
        with self.assertRaises(ValueError):
            validate(items, stats, 'current')

    def test_old_missing_or_disabled_audit_statistics_cannot_explain_skips(self):
        changes = {
            'old version': lambda stats: stats.pop('salary_audit_version'),
            'other version': lambda stats: stats.__setitem__('salary_audit_version', 1),
            'missing reasons': lambda stats: stats.pop('prefilter_by_reason'),
            'extra reason': lambda stats: stats['prefilter_by_reason'].__setitem__('weekly', {}),
            'disabled': lambda stats: stats['optimizations'].__setitem__('salary_prefilter', False),
        }
        for name, change in changes.items():
            items, stats = audited_run(REPLACED)
            change(stats)
            with self.subTest(name), self.assertRaises(ValueError):
                validate(items, stats, 'current')

    def test_unfinished_scroll_cannot_publish_even_when_item_count_is_large(self):
        items, stats = valid_run()
        stats['optimizations'] = {'scroll_interval': [1.5, 2.5]}
        stats['list_collection'] = {'planned': 2, 'completed': 1, 'ended': False}
        stats['scrolls'] = [{'outcome': 'grown'}]
        with self.assertRaises(ValueError):
            validate(items, stats, 'current')
        stats['list_collection']['ended'] = True
        validate(items, stats, 'current')
