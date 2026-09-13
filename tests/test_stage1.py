from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from selenium.common.exceptions import WebDriverException

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import Observation, ServerUnavailable, request_sequence, rolling_max
from recru_it.settings import CRAWL_CONFIG
from recru_it.validate_run import report_quality, validate


def valid_run():
    item = dict.fromkeys(('title', 'site', 'type', 'pay', 'etc1', 'etc2', 'etc3', 'numpeople',
                         'phone', 'detail', 'imageURL', 'time', 'sponsored'), '')
    regions = {region['name']: {'complete': True, 'candidates': 0, 'verified': 0, 'failed': 0, 'saved': 0, 'dropped': 0}
               for region in CRAWL_CONFIG['regions']}
    regions['서울'].update(candidates=50, verified=50, saved=50)
    stats = {'schema': 1, 'run_id': 'current', 'complete': True, 'close_reason': 'finished',
             'regions': regions, 'counts': {'verified': 50, 'format_comparisons': 50},
             'saved': 50, 'dropped': 0, 'spider_errors': 0, 'format_mismatches': {},
             'card_comparison': {'count': 60, 'mismatches': {}},
             'drop_reasons': {},
             'attempts': [{'outcome': 'verified'} for _ in range(50)]}
    return [dict(item) for _ in range(50)], stats


class PublicationTests(unittest.TestCase):
    def test_quality_warning_is_nonblocking_and_contains_only_counts(self):
        for failed, formats in ((0, 0), (1, 0), (0, 1), (1, 2)):
            with self.subTest(failed=failed, formats=formats):
                items, stats = valid_run()
                stats['regions']['서울'].update(candidates=50 + failed, failed=failed)
                stats['counts']['final_failed'] = failed
                stats['attempts'].extend([{'outcome': 'format_mismatch'} for _ in range(formats)])
                stats['format_mismatches'] = {'detail': formats} if formats else {}
                stats['unrelated_site_data'] = 'private-fixture-data'
                validate(items, stats, 'current')
                output = io.StringIO()
                with patch.dict(os.environ, {'GITHUB_ACTIONS': 'true'}), redirect_stdout(output):
                    report_quality(stats)
                self.assertEqual('::warning ' in output.getvalue(), bool(failed or formats))
                self.assertNotIn('private-fixture-data', output.getvalue())

    def test_complete_run_and_filtered_empty_region_are_valid(self):
        items, stats = valid_run()
        validate(items, stats, 'current')

    def test_stale_missing_and_interrupted_runs_are_blocked(self):
        for change in ({'run_id': 'old'}, {'complete': False}, {'close_reason': 'shutdown'},
                       {'spider_errors': 1}, {'regions': {}}, {'saved': 51},
                       {'schema': 99}):
            with self.subTest(change=change):
                items, stats = valid_run()
                stats.update(change)
                with self.assertRaises(ValueError):
                    validate(items, stats, 'current')

    def test_unverified_item_cannot_be_counted_as_saved(self):
        items, stats = valid_run()
        stats['regions']['서울']['verified'] -= 1
        stats['regions']['서울']['failed'] += 1
        with self.assertRaises(ValueError):
            validate(items, stats, 'current')

    def test_missing_detailed_statistics_are_blocked(self):
        for key in ('attempts', 'card_comparison', 'format_mismatches', 'spider_errors'):
            with self.subTest(key=key):
                items, stats = valid_run()
                del stats[key]
                with self.assertRaises(ValueError):
                    validate(items, stats, 'current')

    def test_limited_final_miss_is_recorded_without_arbitrary_rate_gate(self):
        items, stats = valid_run()
        stats['regions']['서울']['candidates'] += 1
        stats['regions']['서울']['failed'] = 1
        stats['counts']['final_failed'] = 1
        validate(items, stats, 'current')

    def test_format_rejected_item_does_not_block_other_verified_items(self):
        items, stats = valid_run()
        stats['regions']['서울'].update(candidates=51, failed=1)
        stats['counts'].update(final_failed=1, format_mismatch=2, format_comparisons=52)
        stats['format_mismatches'] = {'detail': 2}
        stats['attempts'].extend([{'outcome': 'format_mismatch'} for _ in range(2)])
        validate(items, stats, 'current')
        # Counting either rejected snapshot as saved must still block publication.
        stats['saved'] += 1
        items.append(dict(items[0]))
        with self.assertRaises(ValueError):
            validate(items, stats, 'current')


class NetworkTests(unittest.TestCase):
    def test_post_and_preflight_are_counted_without_retrieving_bodies(self):
        class Driver:
            def execute_cdp_cmd(self, method, *args):
                if method == 'Network.getResponseBody':
                    raise AssertionError('Response bodies are unnecessary for verification')
                return {}

            def execute_script(self, *args):
                return False

            def get_log(self, *args):
                events = [
                    {'method': 'Network.requestWillBeSent', 'params': {'requestId': 'preflight',
                        'timestamp': 10, 'type': 'Other', 'request': {
                            'url': 'https://ildao.com/web/Jobinfo/getBoardJobDetail', 'method': 'OPTIONS'}}},
                    {'method': 'Network.loadingFinished', 'params': {
                        'requestId': 'preflight', 'timestamp': 10.1, 'encodedDataLength': 0}},
                    {'method': 'Network.requestWillBeSent', 'params': {'requestId': 'detail',
                        'timestamp': 10.2, 'type': 'XHR', 'request': {
                            'url': 'https://ildao.com/web/Jobinfo/getBoardJobDetail', 'method': 'POST'}}},
                    {'method': 'Network.loadingFinished', 'params': {
                        'requestId': 'detail', 'timestamp': 10.3, 'encodedDataLength': 100}}
                ]
                return [{'message': json.dumps({'message': event})} for event in events]

        observation = Observation(Driver(), 'https://ildao.com/recruit')
        observation.drain()
        self.assertEqual([r['method'] for r in observation.requests], ['OPTIONS', 'POST'])
        self.assertNotIn('body_available', observation.requests[1])

    def test_page_limit_response_stops_even_if_cdp_log_read_fails(self):
        class Driver:
            def execute_cdp_cmd(self, *args):
                return {}

            def get_log(self, *args):
                raise WebDriverException('diagnostic channel unavailable')

            def execute_script(self, *args):
                return True

        observation = Observation(Driver(), 'https://ildao.com/recruit')
        with self.assertRaises(ServerUnavailable):
            observation.drain()
        self.assertEqual(observation.stats['diagnostics']['network_log_missing'], 1)
        self.assertEqual(observation.stats['counts']['server_unavailable'], 1)

    def test_rolling_window_crosses_clock_minute_boundaries(self):
        self.assertEqual(rolling_max([59, 59.5, 60, 60.5]), 4)
        self.assertEqual(rolling_max([0, 60, 120]), 1)
        self.assertEqual(rolling_max([]), 0)
        self.assertEqual(rolling_max([12, 12, 12]), 3)

    def test_same_job_retry_uses_distinct_stack_marker(self):
        old = {'callFrames': [{'functionName': 'recru_request_1'}]}
        new = {'callFrames': [], 'parent': {'callFrames': [{'functionName': 'recru_request_2'}]}}
        self.assertEqual(request_sequence(old), 1)
        self.assertEqual(request_sequence(new), 2)
        self.assertIsNone(request_sequence({'callFrames': [{'functionName': 'unrelated'}]}))

    def test_429_stops_collection_without_retrying_or_logging_headers(self):
        class Driver:
            def execute_cdp_cmd(self, *args):
                return {}

            def execute_script(self, *args):
                return False

            def get_log(self, kind):
                events = [
                    {'method': 'Network.requestWillBeSent', 'params': {
                        'requestId': 'r1', 'timestamp': 1,
                        'request': {'url': 'https://ildao.com/web/Jobinfo/getBoardJobDetail'}}},
                    {'method': 'Network.responseReceived', 'params': {
                        'requestId': 'r1', 'timestamp': 1.1,
                        'response': {'status': 429, 'headers': {'Retry-After': '120', 'Private': 'do not retain'}}}}
                ]
                return [{'message': json.dumps({'message': event})} for event in events]
        observation = Observation(Driver(), 'https://ildao.com/recruit')
        with self.assertRaises(ServerUnavailable):
            observation.drain()
        self.assertEqual(observation.stats['counts']['server_unavailable'], 1)
        self.assertNotIn('do not retain', json.dumps(observation.requests))


if __name__ == '__main__':
    unittest.main()
