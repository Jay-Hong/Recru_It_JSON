"""Archive Actions statistics by declared code revision; never run the crawler."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import statistics
import subprocess
from urllib.parse import urlencode
import zipfile


ROOT = Path(__file__).resolve().parents[1]
REPO = 'Jay-Hong/Recru_It_JSON'
WORKFLOW = '.github/workflows/main.yml'
TESTED_CODE = '34ad3b154c07f043a89ebcd69eda51a48c7c6809'
SOURCE_PATHS = (WORKFLOW, 'requirements.txt', 'recru_it/scrapy.cfg', 'recru_it/recru_it')
RUN_KEYS = ('id', 'run_attempt', 'head_sha', 'head_branch', 'event', 'path',
            'status', 'conclusion', 'created_at', 'html_url')


def api(path, pages=False):
    command = ['gh', 'api', f'repos/{REPO}/{path}']
    if pages:
        command += ['--paginate', '--slurp']
    return json.loads(subprocess.check_output(command))


def signature(commit):
    return {path: subprocess.check_output(
        ['git', 'rev-parse', f'{commit}:{path}'], cwd=ROOT, text=True
    ).strip() for path in SOURCE_PATHS}


def cohorts_from_specs(specs):
    cohorts = {'stage1': signature(TESTED_CODE)}
    for spec in specs:
        label, separator, commit = spec.partition('=')
        if not separator or not re.fullmatch(r'[a-z][a-z0-9_-]*', label) or not commit:
            raise ValueError('Use --cohort label=commit')
        if label in cohorts:
            raise ValueError(f'Duplicate cohort label: {label}')
        value = signature(commit)
        if value in cohorts.values():
            raise ValueError(f'Cohort has the same runtime code as an existing cohort: {label}')
        cohorts[label] = value
    return cohorts


def identify_cohort(commit, cohorts):
    value = signature(commit)
    return next((label for label, expected in cohorts.items() if value == expected), None)


def immutable_write(path, data):
    """A repeated download must agree with the preserved evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f'Archived evidence changed: {path}')
    else:
        with path.open('xb') as stream:
            stream.write(data)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def distribution(values):
    ordered = sorted(value for value in values if value is not None)
    if not ordered:
        return {'count': 0, 'median': None, 'p95': None, 'max': None}
    return {'count': len(ordered), 'median': statistics.median(ordered),
            'p95': ordered[int((len(ordered) - 1) * .95)], 'max': ordered[-1]}


def duration(start, end):
    if not start or not end:
        return None
    return (datetime.fromisoformat(end.replace('Z', '+00:00')) -
            datetime.fromisoformat(start.replace('Z', '+00:00'))).total_seconds()


def summarize(run, stats, jobs, code_matches, reference=False, cohort='stage1'):
    row = {key: run[key] for key in RUN_KEYS}
    row.update(reference=reference, code_matches=code_matches, cohort=cohort, review=[], comparable=False)
    build = next((job for job in jobs if job['name'] == 'build'), None)
    row['job_seconds'] = duration(build['started_at'], build['completed_at']) if build else None
    execution = next((step for step in build['steps'] if step['name'] == 'Execution'), None) if build else None
    row['execution_seconds'] = duration(execution['started_at'], execution['completed_at']) if execution else None
    if stats is None:
        row['review'].append('statistics_unavailable')
        return row
    if not isinstance(stats, dict) or stats.get('schema') != 1 or stats.get('run_id') != f"{run['id']}-{run['run_attempt']}":
        row['review'].append('statistics_identity_or_schema_mismatch')
        return row
    counts, regions = stats['counts'], stats['regions']
    candidates = sum(region['candidates'] for region in regions.values())
    verified = sum(region['verified'] for region in regions.values())
    failed = sum(region['failed'] for region in regions.values())
    row.update(candidates=candidates, verified=verified, final_failed=failed,
               saved=stats['saved'], dropped=stats['dropped'], counts=counts,
               regions=regions, drop_reasons=stats['drop_reasons'],
               scrolls=len(stats['scrolls']), cards=stats['card_comparison']['count'],
               elapsed_seconds=stats['elapsed_seconds'], seconds=stats['seconds'],
               outcomes=dict(Counter(attempt['outcome'] for attempt in stats['attempts'])),
               diagnostics=stats['diagnostics'], format_mismatches=stats['format_mismatches'],
               network=stats['network'])
    row['ready_seconds'] = distribution(attempt.get('ready_seconds') for attempt in stats['attempts']
                                        if attempt['outcome'] == 'verified')
    posts = [request for request in stats['network_requests']
             if request['phase'] == 'collection' and request['category'] == 'detail'
             and request['method'] == 'POST']
    row['detail_response_seconds'] = distribution(request.get('response_seconds') for request in posts)
    # First/retry attempt timers include their waits and checks. Do not add those again.
    attempt_seconds = sum(stats['seconds'].get(key, 0) for key in ('first_attempt', 'retry'))
    row['attempt_seconds_per_candidate'] = attempt_seconds / candidates if candidates else None
    row['scroll_seconds_per_scroll'] = statistics.mean(s['seconds'] for s in stats['scrolls']) if stats['scrolls'] else None
    accounting = (len(regions) == 17 and all(
        r['complete'] is True and r['candidates'] == r['verified'] + r['failed']
        and r['verified'] + r.get('manual', 0) == r['saved'] + r['dropped']
        for r in regions.values())
        and verified == counts.get('verified', 0)
        and failed == counts.get('final_failed', 0)
        and stats['saved'] + stats['dropped'] == verified + counts.get('manual', 0)
        and sum(stats['drop_reasons'].values()) == stats['dropped']
        and row['outcomes'].get('verified', 0) == verified)
    if not accounting or not stats['complete'] or stats['close_reason'] != 'finished':
        row['review'].append('incomplete_or_inconsistent_statistics')
    if failed or stats['format_mismatches']:
        row['review'].append('item_failures_or_format_mismatches')
    if any(stats['diagnostics'].values()):
        row['review'].append('diagnostic_gaps')
    if stats['spider_errors'] or counts.get('server_unavailable', 0):
        row['review'].append('crawler_or_source_error')
    row['comparable'] = bool(
        not reference and run['event'] == 'schedule' and run['head_branch'] == 'master'
        and run['path'] == WORKFLOW and run['run_attempt'] == 1 and code_matches
        and run['status'] == 'completed' and run['conclusion'] == 'success'
        and build and build['conclusion'] == 'success'
        and execution and execution['conclusion'] == 'success' and accounting
        and stats['complete'] and stats['close_reason'] == 'finished'
        and not stats['spider_errors'] and not counts.get('server_unavailable', 0)
        and not any(stats['diagnostics'].values()))
    return row


def collect(run, output, cohorts, reference=False):
    folder = output / f"{run['id']}-{run['run_attempt']}"
    try:
        cohort = identify_cohort(run['head_sha'], cohorts)
    except subprocess.CalledProcessError:
        cohort = None  # Unknown source is visible, but cannot count as a baseline.
    matches = cohort is not None
    jobs = []
    if run['status'] == 'completed':
        pages = api(f"actions/runs/{run['id']}/attempts/{run['run_attempt']}/jobs?per_page=100", pages=True)
        for page in pages:
            for job in page['jobs']:
                jobs.append({key: job[key] for key in ('name', 'started_at', 'completed_at', 'conclusion', 'steps')})
        immutable_write(folder / 'run.json', encoded({key: run[key] for key in RUN_KEYS}))
        immutable_write(folder / 'jobs.json', encoded(jobs))
    stats_path = folder / 'recru-stats.json'
    archive_error = None
    if stats_path.exists():
        data = stats_path.read_bytes()
        manifest = json.loads((folder / 'artifact.json').read_text())
        if hashlib.sha256(data).hexdigest() != manifest['stats_sha256']:
            raise ValueError(f'Archived statistics checksum mismatch: {stats_path}')
    elif run['status'] == 'completed':
        pages = api(f"actions/runs/{run['id']}/artifacts?per_page=100", pages=True)
        artifacts = [a for page in pages for a in page['artifacts']
                     if a['name'] == f"recru-stats-{run['id']}-{run['run_attempt']}"]
        if len(artifacts) == 1 and not artifacts[0]['expired']:
            artifact = artifacts[0]
            blob = subprocess.check_output(['gh', 'api', f"repos/{REPO}/actions/artifacts/{artifact['id']}/zip"])
            with zipfile.ZipFile(io.BytesIO(blob)) as archive:
                # Read the known file directly; never extract arbitrary archive paths.
                data = archive.read('recru-stats.json')
            manifest = {key: artifact[key] for key in ('id', 'name', 'expires_at')}
            manifest.update(stats_sha256=hashlib.sha256(data).hexdigest(),
                            zip_sha256=hashlib.sha256(blob).hexdigest())
            immutable_write(folder / 'artifact.json', encoded(manifest))
            immutable_write(stats_path, data)
        else:
            archive_error = 'artifact_missing_expired_or_ambiguous'
    try:
        stats = json.loads(stats_path.read_text()) if stats_path.exists() else None
        row = summarize(run, stats, jobs, matches, reference, cohort)
    except (ValueError, KeyError, TypeError) as error:
        row = summarize(run, None, jobs, matches, reference, cohort)
        row['review'].append('invalid_statistics_' + type(error).__name__)
    if archive_error:
        row['review'].append(archive_error)
    return row


def report(rows):
    regular = [row for row in rows if not row['reference']]
    comparable = sum(row['comparable'] for row in regular)
    grouped = dict(Counter(row['cohort'] for row in regular if row['comparable']))
    lines = ['# 단계별 수집 기록', '',
             f'조회 시각: {datetime.now(timezone.utc).isoformat()}', '',
             f'정기 실행 {len(regular)}회 / 비교 가능한 최초 시도 {comparable}회 (목표 3~5회).',
             f'단계별 정기 비교 횟수: {json.dumps(grouped, ensure_ascii=False)}. 서로 다른 단계의 횟수는 합쳐 판단하지 않는다.',
             '횟수만으로 다음 단계를 승인하지 않는다. 실패·지역별 누락·진단 누락도 함께 검토한다.', '',
             '| 실행 | 단계 | 구분 | 상태 | 작업 초 | 대상/검증/저장 | 같은 단계 비교 가능 | 검토 사항 |',
             '| --- | --- | --- | --- | ---: | --- | --- | --- |']
    for row in rows:
        values = '/'.join(str(row.get(key, '—')) for key in ('candidates', 'verified', 'saved'))
        label = '시험 참고' if row['reference'] else f"정기 (시도 {row['run_attempt']})"
        notes = list(row['review'])
        if not row['code_matches']:
            notes.append('source_changed_or_unavailable')
        lines.append(f"| [{row['id']}]({row['html_url']}) | {row['cohort'] or 'unknown'} | {label} | {row['conclusion'] or row['status']} | "
                     f"{row['job_seconds']} | {values} | {row['comparable']} | {', '.join(notes) or '없음'} |")
    lines += ['', '세부 수치와 지역별 집계는 summary.json에 있다. 원본 통계는 실행 ID·시도 번호별로 보관한다.',
              '실행 전체 시간이 아닌 작업 시작~완료 시간을 사용하며 대기열 시간은 제외한다.',
              '최초/재시도 시간에는 대기·검증·텍스트 비교가 포함되므로 세부 시간과 더하지 않는다.',
              '준비 시간은 브라우저 클릭 기준 관측치이며, 고정 대기를 줄였을 때의 오독 건수가 아니다.',
              '응답 지연은 수집 중 상세 POST 기준이고 OPTIONS는 요청 수에 별도로 포함된다.',
              '통계 점검은 결과 JSON을 다시 검증한 것이 아니다. 반영 성공은 해당 Actions 작업의 결과로 확인한다.',
              '이 도구는 호출할 때만 조회한다. 자동 감시·Actions 실행·수집 속도 변경은 수행하지 않는다.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Archive directory outside the repository')
    parser.add_argument('--since', default='2026-09-14')
    parser.add_argument('--reference-run', type=int, action='append', default=[])
    parser.add_argument('--cohort', action='append', default=[], metavar='LABEL=COMMIT',
                        help='Additional known runtime revision; group it separately from stage1')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error('--output must be outside the repository')
    subprocess.run(['git', 'fetch', 'origin'], cwd=ROOT, check=True)
    cohorts = cohorts_from_specs(args.cohort)
    query = urlencode({'branch': 'master', 'event': 'schedule', 'created': '>=' + args.since, 'per_page': 100})
    pages = api('actions/workflows/main.yml/runs?' + query, pages=True)
    runs = {run['id']: run for page in pages for run in page['workflow_runs']}
    rows = [collect(run, output, cohorts) for run in sorted(runs.values(), key=lambda r: r['id'])]
    for run_id in dict.fromkeys(args.reference_run):
        if run_id not in runs:
            rows.append(collect(api(f'actions/runs/{run_id}'), output, cohorts, reference=True))
    output.mkdir(parents=True, exist_ok=True)
    for name, data in [('summary.json', encoded(rows)), ('summary.md', report(rows).encode())]:
        temporary = output / (name + '.tmp')
        temporary.write_bytes(data)
        temporary.replace(output / name)
    print(f"Scheduled runs: {len(runs)}; comparable: {sum(row['comparable'] for row in rows)}")
    print(output / 'summary.md')


if __name__ == '__main__':
    main()
