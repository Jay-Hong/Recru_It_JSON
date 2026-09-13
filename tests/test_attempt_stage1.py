"""Item recovery versus whole-run failures, with no site or browser requests."""

from collections import Counter
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

from selenium.common.exceptions import WebDriverException

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import (
    EvidenceUnavailable, FormatMismatch, Observation, ObservationUnavailable, ServerUnavailable,
)
from recru_it.spiders.recru_it import Recru_It_Spider


class Driver:
    healthy = True
    pending = False

    def execute_cdp_cmd(self, *args):
        return {}

    def get_log(self, *args):
        return []

    def execute_script(self, script, *args):
        if 'health()' in script:
            return {'available': self.healthy, 'pendingDetail': self.pending}
        if 'summary(' in script:
            return {'attempt': None, 'requests': [], 'diagnosticErrors': 0}
        return False


class Card:
    location_once_scrolled_into_view = {'x': 0, 'y': 0}

    def __init__(self, failures=()):
        self.click = Mock(side_effect=[*failures, None])


class AttemptTests(unittest.TestCase):
    def setUp(self):
        self.spider = Recru_It_Spider.__new__(Recru_It_Spider)
        self.spider.driver = Driver()
        self.observation = Observation(self.spider.driver, 'https://ildao.com/recruit')
        self.spider.observation = self.observation
        self.spider._item_regions = {}
        self.spider.get_job_detail = Mock(return_value=('verified',) * 11)
        self.observation.read = Mock(return_value={'verified': True})
        self.region = {'name': '서울', 'keywords': ['서울'], 'sleep_before': (0, 0), 'sleep_between': (1, 1)}
        self.sleeps = []
        self.observation.sleep = lambda seconds, name: self.sleeps.append((seconds, name))

    def collect(self, cards):
        return list(self.spider.process_region(self.region, cards, [''] * len(cards), ['서울'] * len(cards), 0))

    def test_item_browser_error_retries_once_and_continues_to_next_item(self):
        bad = Card([WebDriverException('private payload'), WebDriverException('private payload')])
        good = Card()
        items = self.collect([bad, good])
        self.assertEqual(len(items), 1)
        self.assertEqual(bad.click.call_count, 2)
        self.assertEqual(good.click.call_count, 1)
        self.assertTrue(self.observation.stats['regions']['서울']['complete'])
        self.assertEqual(self.observation.stats['counts']['final_failed'], 1)
        self.assertEqual([a['outcome'] for a in self.observation.stats['attempts']],
                         ['browser_error', 'browser_error', 'verified'])
        self.assertNotIn('private payload', str(self.observation.stats))
        self.assertEqual(self.sleeps.count((1, 'click_wait')), 3)
        self.assertIn((.5, 'post_click_wait'), self.sleeps)

    def test_arm_failure_is_an_item_failure_and_never_clicks_that_attempt(self):
        real_arm = self.observation.arm
        failures = iter([True, True, False])

        def arm(*args, **kwargs):
            if next(failures):
                raise EvidenceUnavailable('cannot_arm_observation')
            return real_arm(*args, **kwargs)

        self.observation.arm = arm
        bad, good = Card(), Card()
        self.assertEqual(len(self.collect([bad, good])), 1)
        bad.click.assert_not_called()
        self.assertEqual(self.observation.stats['counts']['evidence_unavailable'], 2)

    def test_format_failure_is_never_exported_and_does_not_abort_next_item(self):
        self.observation.read.side_effect = [FormatMismatch('detail'), FormatMismatch('detail'), {'verified': True}]
        bad, good = Card([None]), Card()
        self.assertEqual(len(self.collect([bad, good])), 1)
        self.spider.get_job_detail.assert_called_once_with({'verified': True})
        self.assertEqual(self.observation.stats['counts']['format_mismatch'], 2)
        self.assertEqual(self.observation.stats['counts']['final_failed'], 1)

    def test_dead_browser_or_missing_page_observer_stops_without_retry(self):
        self.spider.driver.healthy = False
        card = Card()
        with self.assertRaises(ObservationUnavailable):
            self.collect([card, Card()])
        card.click.assert_not_called()
        self.assertFalse(self.observation.stats['regions']['서울']['complete'])
        self.assertEqual(self.observation.stats['counts']['retries'], 0)

    def test_server_limit_stops_without_retry(self):
        self.observation.read.side_effect = ServerUnavailable('source unavailable')
        card, next_card = Card(), Card()
        with self.assertRaises(ServerUnavailable):
            self.collect([card, next_card])
        card.click.assert_called_once()
        next_card.click.assert_not_called()
        self.assertFalse(self.observation.stats['regions']['서울']['complete'])

    def test_programming_error_remains_a_whole_run_failure(self):
        self.observation.read.side_effect = TypeError('implementation defect')
        with self.assertRaises(TypeError):
            self.collect([Card()])
        self.assertEqual(self.observation.stats['attempts'][0]['outcome'], 'unexpected_error')
        self.assertFalse(self.observation.stats['regions']['서울']['complete'])

    def test_pending_response_waits_before_arming_without_another_click(self):
        with patch.object(self.observation, 'require_observer', side_effect=[
                {'pendingDetail': True}, {'pendingDetail': False}]):
            record = self.observation.arm(Card(), '서울', False)
        self.assertEqual(record['number'], 1)
        self.assertIn((.1, 'previous_request_poll'), self.sleeps)
        with patch.object(self.observation, 'require_observer', return_value={'pendingDetail': True}):
            with self.assertRaises(EvidenceUnavailable):
                self.observation.arm(Card(), '서울', True, timeout=0)


class LegacyComparisonTests(unittest.TestCase):
    def test_equal_before_after_snapshots_do_not_authorize_different_legacy_text(self):
        driver = Driver()
        observation = Observation(driver, 'https://ildao.com/recruit')
        raw = {'detail': 'verified snapshot'}
        driver.execute_script = Mock(side_effect=[{'detail': '#body'}, {'ok': True, 'raw': raw}])
        driver.find_elements = Mock(return_value=[Mock(text='transient different body')])
        with self.assertRaises(FormatMismatch):
            observation.compare_legacy(raw)
        self.assertEqual(observation.stats['format_mismatches'], Counter(detail=1))


if __name__ == '__main__':
    unittest.main()
