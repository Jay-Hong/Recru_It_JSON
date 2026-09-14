"""Publish gate. Run before copying results or committing any output files."""

import argparse
import json
import os
from pathlib import Path

from recru_it.settings import CRAWL_CONFIG


def validate(items, stats, run_id, minimum=50):
    problems = []
    required = {'schema', 'run_id', 'complete', 'close_reason', 'regions', 'counts',
                'saved', 'dropped', 'spider_errors', 'format_mismatches', 'attempts', 'card_comparison', 'drop_reasons'}
    if not isinstance(stats, dict) or not required.issubset(stats):
        raise ValueError('required run statistics are missing')
    if not run_id or stats.get('run_id') != run_id or stats.get('schema') != 1:
        problems.append('missing, stale, or unsupported run statistics')
    if stats.get('complete') is not True or stats.get('close_reason') != 'finished':
        problems.append('crawler did not complete')
    regions = stats.get('regions', {})
    if set(regions) != {region['name'] for region in CRAWL_CONFIG['regions']} or any(
            region.get('complete') is not True or
            region.get('candidates', -1) != region.get('verified', 0) + region.get('failed', 0) + region.get('prefiltered', 0) or
            region.get('verified', 0) + region.get('manual', 0) != region.get('saved', -1) + region.get('dropped', -1)
            for region in regions.values()):
        problems.append('incomplete region traversal or counts')
    if stats.get('spider_errors', 0) or stats.get('counts', {}).get('server_unavailable', 0):
        problems.append('crawler or source error')
    # A format mismatch rejects that snapshot; it does not reject other items
    # whose atomic values passed both identity and text-compatibility checks.
    counts = stats.get('counts', {})
    skipped = sum(region.get('prefiltered', 0) for region in regions.values())
    options = stats.get('optimizations', {})
    prefilter = stats.get('prefilter', {})
    if options.get('salary_prefilter'):
        if (skipped != prefilter.get('skipped', 0) or
                skipped != prefilter.get('low_daily_pay', 0) + prefilter.get('low_monthly_pay', 0) or
                prefilter.get('eligible', 0) != skipped + prefilter.get('audit_selected', 0) or
                prefilter.get('audit_selected', 0) != prefilter.get('audit_checked', 0) or
                prefilter.get('audit_failed', 0) or prefilter.get('audit_mismatch', 0) or
                (skipped and not prefilter.get('audit_checked', 0))):
            problems.append('salary prefilter counts or audit did not pass')
    elif skipped:
        problems.append('salary exclusions without enabled prefilter')
    if options.get('scroll_interval'):
        collection = stats.get('list_collection', {})
        if (not collection or collection.get('completed') != len(stats.get('scrolls', [])) or
                not (collection.get('ended') is True or collection.get('completed') == collection.get('planned')) or
                any(s.get('outcome') not in ('grown', 'complete', 'initial_no_request') for s in stats.get('scrolls', []))):
            problems.append('list collection did not complete')
    verified = sum(region.get('verified', 0) for region in regions.values())
    if counts.get('final_failed', 0) != sum(region.get('failed', 0) for region in regions.values()):
        problems.append('final failure counts do not match regions')
    attempts = stats['attempts']
    if not isinstance(attempts, list) or sum(attempt.get('outcome') == 'verified' for attempt in attempts) != verified:
        problems.append('attempt outcomes do not match verified items')
    comparison = stats['card_comparison']
    if not isinstance(comparison, dict) or comparison.get('count', 0) < 1 or comparison.get('mismatches') != {}:
        problems.append('card identity and column comparison did not pass')
    if counts.get('verified', 0) != verified or counts.get('format_comparisons', 0) < verified:
        problems.append('verified snapshot counts do not match')
    if stats.get('saved', 0) + stats.get('dropped', 0) != verified + counts.get('manual', 0):
        problems.append('pipeline counts do not match verified and manual items')
    if sum(stats['drop_reasons'].values()) != stats['dropped']:
        problems.append('filter reason counts do not match dropped items')
    if options.get('click_readiness') and any(
            (attempt.get('outcome') == 'verified' or 'click_started_seconds' in attempt) and
            attempt.get('click_readiness', {}).get('ok') is not True for attempt in attempts):
        problems.append('click without position readiness evidence')
    allowed_outcomes = {'verified', 'click_intercepted', 'click_not_ready', 'format_mismatch',
                        'evidence_unavailable', 'verification_failed', 'browser_error'}
    if any(attempt.get('outcome') not in allowed_outcomes for attempt in attempts):
        problems.append('unfinished or aborted click attempt')
    if not isinstance(items, list) or len(items) < minimum or len(items) != stats.get('saved'):
        problems.append('result count or type is invalid')
    elif any(not isinstance(item, dict) or set(item) != {
        'title', 'site', 'type', 'pay', 'etc1', 'etc2', 'etc3', 'numpeople',
        'phone', 'detail', 'imageURL', 'time', 'sponsored'
    } or any(not isinstance(value, str) for value in item.values()) for item in items):
        problems.append('result item schema is invalid')
    if problems:
        raise ValueError('; '.join(problems))


def report_quality(stats):
    """Make partial losses visible without changing the publication decision."""
    failed = stats['counts'].get('final_failed', 0)
    format_attempts = sum(attempt['outcome'] == 'format_mismatch' for attempt in stats['attempts'])
    if failed or format_attempts or stats['format_mismatches']:
        # Only aggregate numbers enter the workflow command, never site content.
        prefix = '::warning title=Collection quality::' if os.environ.get('GITHUB_ACTIONS') == 'true' else 'WARNING: '
        print(f'{prefix}Final failed items: {failed}; format mismatch attempts: {format_attempts}. '
              'Only verified snapshots are published; review the statistics artifact.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result', default='recru_result.json')
    parser.add_argument('--stats', default=os.environ.get('RECRU_STATS_PATH', 'recru_stats.json'))
    args = parser.parse_args()
    try:
        items = json.loads(Path(args.result).read_text(encoding='utf-8'))
        stats = json.loads(Path(args.stats).read_text(encoding='utf-8'))
        validate(items, stats, os.environ.get('RECRU_RUN_ID'))
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise SystemExit('Result publication blocked: ' + str(error)) from None
    print(f'Validated {len(items)} items and all regions for this run.')
    report_quality(stats)


if __name__ == '__main__':
    main()
