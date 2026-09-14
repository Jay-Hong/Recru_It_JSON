from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.collect_stage1_baseline import (
    WORKFLOW, cohorts_from_specs, collect, identify_cohort, immutable_write, report, summarize,
)


def sample():
    run = dict(id=123, run_attempt=1, head_sha='source', head_branch='master',
               event='schedule', path=WORKFLOW, status='completed', conclusion='success',
               created_at='2026-09-15T01:00:00Z', html_url='https://example.invalid/run/123')
    regions = {str(index): dict(candidates=0, verified=0, failed=0, saved=0,
                               dropped=0, complete=True) for index in range(17)}
    regions['0'].update(candidates=51, verified=50, failed=1, saved=50)
    request = dict(phase='collection', category='detail', method='POST', response_seconds=.2)
    stats = dict(schema=1, run_id='123-1', complete=True, close_reason='finished',
                 regions=regions, counts=dict(verified=50, final_failed=1),
                 saved=50, dropped=0, drop_reasons={}, card_comparison=dict(count=100),
                 scrolls=[dict(seconds=4)], elapsed_seconds=120,
                 seconds=dict(first_attempt=100, retry=2, click_wait=80, legacy_comparison=10),
                 attempts=[dict(outcome='verified', ready_seconds=.3) for _ in range(50)] +
                          [dict(outcome='verification_failed')],
                 diagnostics={}, format_mismatches={}, spider_errors=0,
                 network={}, network_requests=[request, dict(request, method='OPTIONS', response_seconds=10),
                                               dict(request, phase='initial', response_seconds=20)])
    jobs = [dict(name='build', started_at='2026-09-15T01:00:10Z',
                 completed_at='2026-09-15T01:01:15Z', conclusion='success',
                 steps=[dict(name='Execution', started_at='2026-09-15T01:00:20Z',
                             completed_at='2026-09-15T01:01:10Z', conclusion='success')])]
    return run, stats, jobs


class BaselineReportTests(unittest.TestCase):
    def test_reference_is_not_a_scheduled_baseline(self):
        run, stats, jobs = sample()
        self.assertTrue(summarize(run, stats, jobs, True)['comparable'])
        self.assertFalse(summarize(run, stats, jobs, True, reference=True)['comparable'])

    def test_other_workflow_rerun_and_changed_code_are_not_counted(self):
        run, stats, jobs = sample()
        for changes in [dict(event='dynamic'), dict(head_branch='test'),
                        dict(path='other.yml'), dict(run_attempt=2), dict(conclusion='failure')]:
            with self.subTest(changes=changes):
                candidate = dict(run, **changes)
                current = dict(stats, run_id=f"123-{candidate['run_attempt']}")
                self.assertFalse(summarize(candidate, current, jobs, True)['comparable'])
        self.assertFalse(summarize(run, stats, jobs, False)['comparable'])

    def test_missing_and_stale_statistics_remain_visible(self):
        run, stats, jobs = sample()
        for value in [None, [], dict(stats, run_id='another-run'), dict(stats, schema=99)]:
            row = summarize(run, value, jobs, True)
            self.assertFalse(row['comparable'])
            self.assertTrue(row['review'])
            self.assertIn('123', report([row]))

    def test_partial_losses_are_reviewed_without_inventing_a_failure_threshold(self):
        run, stats, jobs = sample()
        row = summarize(run, stats, jobs, True)
        self.assertTrue(row['comparable'])
        self.assertEqual(row['final_failed'], 1)
        self.assertIn('item_failures_or_format_mismatches', row['review'])

    def test_incomplete_inconsistent_or_unobserved_runs_do_not_count(self):
        run, stats, jobs = sample()
        incomplete = deepcopy(stats)
        incomplete['regions']['16']['complete'] = False
        for value in [incomplete, dict(stats, complete=False), dict(stats, saved=49),
                      dict(stats, spider_errors=1), dict(stats, diagnostics={'network_log_missing': 1})]:
            self.assertFalse(summarize(run, value, jobs, True)['comparable'])

    def test_metrics_exclude_queue_time_and_do_not_double_count_timers(self):
        run, stats, jobs = sample()
        row = summarize(run, stats, jobs, True)
        self.assertEqual(row['job_seconds'], 65)
        self.assertEqual(row['execution_seconds'], 50)
        self.assertEqual(row['attempt_seconds_per_candidate'], 2)
        self.assertEqual(row['detail_response_seconds']['count'], 1)
        self.assertEqual(row['detail_response_seconds']['median'], .2)

    def test_prefilter_is_separate_from_collected_candidate_cost_and_requires_audit(self):
        run, stats, jobs = sample()
        stats['regions']['0'].update(candidates=61, prefiltered=10)
        stats['prefilter'] = {'skipped': 10, 'audit_selected': 2, 'audit_checked': 2}
        row = summarize(run, stats, jobs, True, cohort='combined')
        self.assertTrue(row['comparable'])
        self.assertEqual(row['prefiltered'], 10)
        self.assertEqual(row['attempt_seconds_per_collected_candidate'], 2)
        self.assertLess(row['attempt_seconds_per_candidate'], 2)
        stats['prefilter']['audit_checked'] = 1
        self.assertFalse(summarize(run, stats, jobs, True)['comparable'])

    def test_missing_collection_step_and_unverified_readiness_do_not_count(self):
        run, stats, jobs = sample()
        stats['attempts'][-1]['ready_seconds'] = 20
        jobs[0]['steps'] = []
        row = summarize(run, stats, jobs, True)
        self.assertFalse(row['comparable'])
        self.assertEqual(row['ready_seconds']['count'], 50)
        self.assertEqual(row['ready_seconds']['max'], .3)

    def test_empty_run_list_is_not_a_completed_baseline(self):
        self.assertIn('정기 실행 0회 / 비교 가능한 최초 시도 0회', report([]))

    def test_original_archive_cannot_be_silently_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'run/stats.json'
            immutable_write(path, b'original')
            immutable_write(path, b'original')
            with self.assertRaises(ValueError):
                immutable_write(path, b'different')
            self.assertEqual(path.read_bytes(), b'original')

    def test_expired_missing_artifact_is_reported_not_dropped(self):
        run, _, jobs = sample()
        pages = [[dict(jobs=jobs)], [dict(artifacts=[dict(name='recru-stats-123-1', expired=True)])]]
        with tempfile.TemporaryDirectory() as folder, patch(
                'scripts.collect_stage1_baseline.signature', return_value={}), patch(
                'scripts.collect_stage1_baseline.api', side_effect=pages):
            row = collect(run, Path(folder), {'stage1': {}})
            self.assertFalse(row['comparable'])
            self.assertIn('artifact_missing_expired_or_ambiguous', row['review'])

    def test_cached_statistics_are_verified_and_reused_without_artifact_download(self):
        run, stats, jobs = sample()
        with tempfile.TemporaryDirectory() as folder, patch(
                'scripts.collect_stage1_baseline.signature', return_value={}), patch(
                'scripts.collect_stage1_baseline.api', return_value=[dict(jobs=jobs)]) as api:
            root = Path(folder)
            data = json.dumps(stats).encode()
            immutable_write(root / '123-1/recru-stats.json', data)
            immutable_write(root / '123-1/artifact.json', json.dumps(
                dict(stats_sha256=hashlib.sha256(data).hexdigest())).encode())
            self.assertTrue(collect(run, root, {'stage1': {}})['comparable'])
            api.assert_called_once()
            (root / '123-1/recru-stats.json').write_bytes(b'corrupted')
            with self.assertRaises(ValueError):
                collect(run, root, {'stage1': {}})

    def test_only_declared_runtime_revisions_match_a_cohort(self):
        cohorts = {'stage1': {'code': 'old'}, 'stage2-waits': {'code': 'new'}}
        with patch('scripts.collect_stage1_baseline.signature', return_value={'code': 'new'}):
            self.assertEqual(identify_cohort('any-result-commit', cohorts), 'stage2-waits')
        with patch('scripts.collect_stage1_baseline.signature', return_value={'code': 'unexpected'}):
            self.assertIsNone(identify_cohort('unknown-source', cohorts))

    def test_cohort_labels_cannot_replace_or_alias_the_baseline(self):
        with patch('scripts.collect_stage1_baseline.signature', return_value={'code': 'same'}):
            for spec in ['stage1=changed', 'duplicate=same', 'missing-separator', 'bad|label=commit']:
                with self.subTest(spec=spec), self.assertRaises(ValueError):
                    cohorts_from_specs([spec])

    def test_reports_keep_stage_counts_separate(self):
        run, stats, jobs = sample()
        first = summarize(run, stats, jobs, True, cohort='stage1')
        second = summarize(run, stats, jobs, True, cohort='stage2-waits')
        output = report([first, second])
        self.assertIn('"stage1": 1', output)
        self.assertIn('"stage2-waits": 1', output)
        self.assertIn('서로 다른 단계의 횟수는 합쳐 판단하지 않는다', output)


if __name__ == '__main__':
    unittest.main()
