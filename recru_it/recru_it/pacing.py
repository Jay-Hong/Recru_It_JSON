"""Sequential start intervals, a deliberately narrow list salary predicate, and its audit."""

from collections import Counter
from decimal import Decimal
import math
import random
import re
import time


class StartInterval:
    def __init__(self, interval, sleep, name, clock=time.monotonic, sample=random.uniform):
        low, high = interval
        if not (math.isfinite(low) and math.isfinite(high) and 0 < low <= high):
            raise ValueError('invalid start interval')
        self.interval, self.sleep, self.name = interval, sleep, name
        self.clock, self.sample = clock, sample
        self.next_start = None
        self.last_start = None

    def wait(self):
        if self.next_start is not None:
            remaining = self.next_start - self.clock()
            if remaining > 0:
                self.sleep(remaining, self.name)

    def mark_start(self):
        now = self.clock()
        gap = None if self.last_start is None else now - self.last_start
        self.last_start = now
        # Schedule from the actual start, never from an overdue deadline.
        self.next_start = now + self.sample(*self.interval)
        return gap

    def start(self):
        self.wait()
        return self.mark_start()


def salary_exclusion(card):
    """Unknown units, ambiguous formats, and values outside 100k..149,999 pass."""
    if not isinstance(card, dict):
        return None
    unit = card.get('priceDiv')
    if unit not in ('1', '3'):
        return None
    price = str(card.get('price', ''))
    if not re.fullmatch(r'(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)', price):
        return None
    amount = int(price.replace(',', ''))
    # Require the displayed list amount to agree with the card's numeric field.
    pay = card.get('pay')
    if not isinstance(pay, str):
        return None
    match = re.fullmatch(r'(\d+(?:\.\d+)?)(?:만(?: 이상)?|\s*~\s*(\d+(?:\.\d+)?)만)', pay.strip())
    if not match or Decimal(match[1]) * 10000 != amount or not 100000 <= amount < 150000:
        return None
    if match[2] and Decimal(match[2]) < Decimal(match[1]):
        return None
    return 'low_daily_pay' if unit == '1' else 'low_monthly_pay'


SALARY_REASONS = ('low_daily_pay', 'low_monthly_pay')
SALARY_AUDIT_VERSION = 2
AUDIT_COUNTERS = ('eligible', 'skipped', 'audit_selected', 'audit_checked', 'audit_failed',
                  'audit_mismatch', 'audit_replacements', 'audit_replacement_pending')


class SalaryAudit:
    """Per-reason audit ledger. An unverifiable audit is owed by the next card of that reason."""

    def __init__(self, stats, rate):
        stats['salary_audit_version'] = SALARY_AUDIT_VERSION
        self.total = stats['prefilter'] = Counter()
        self.reasons = stats['prefilter_by_reason'] = {
            reason: Counter(audit_replacement_pending=0) for reason in SALARY_REASONS}
        self.events = stats['prefilter_events'] = []
        self.rate = rate

    def _add(self, reason, key, amount=1):
        self.reasons[reason][key] += amount
        self.total[key] += amount

    def select(self, reason, region, draw):
        state = self.reasons[reason]
        if state['audit_replacement_pending']:
            selection = 'replacement'
        elif not state['audit_checked']:
            selection = 'initial'
        else:
            selection = 'random' if draw() < self.rate else 'skip'
        event = {'n': len(self.events) + 1, 'reason': reason, 'region': region,
                 'selection': selection, 'outcome': None}
        self.events.append(event)
        self._add(reason, 'eligible')
        if selection == 'skip':
            self._add(reason, 'skipped')
            self.total[reason] += 1
            event['outcome'] = 'skipped'
        else:
            self._add(reason, 'audit_selected')
            if selection == 'replacement':
                self._add(reason, 'audit_replacements')
                self._add(reason, 'audit_replacement_pending', -1)
        return event

    def finish(self, event, outcome):
        if event['outcome'] is not None or outcome not in ('checked', 'failed', 'mismatch'):
            raise ValueError('invalid salary audit outcome')
        event['outcome'] = outcome
        self._add(event['reason'], {'checked': 'audit_checked', 'failed': 'audit_failed',
                                    'mismatch': 'audit_mismatch'}[outcome])
        if outcome == 'failed':
            self._add(event['reason'], 'audit_replacement_pending')


def _counter_values(source, keys):
    if not isinstance(source, dict):
        return None
    values = {key: source.get(key, 0) for key in keys}
    return values if all(type(value) is int and value >= 0 for value in values.values()) else None


def _replay(events, regions):
    """Recompute counters from the event order; None when the order breaks a selection rule."""
    if not isinstance(events, list):
        return None
    reasons = {reason: dict.fromkeys(AUDIT_COUNTERS, 0) for reason in SALARY_REASONS}
    region_skips = dict.fromkeys(regions, 0)
    for number, event in enumerate(events, 1):
        if (not isinstance(event, dict) or event.get('n') != number
                or event.get('reason') not in reasons or event.get('region') not in region_skips):
            return None
        state = reasons[event['reason']]
        selection, outcome = event.get('selection'), event.get('outcome')
        expected = (('replacement',) if state['audit_replacement_pending'] else
                    ('initial',) if not state['audit_checked'] else ('random', 'skip'))
        if selection not in expected:
            return None
        state['eligible'] += 1
        if selection == 'skip':
            if outcome != 'skipped':
                return None
            state['skipped'] += 1
            region_skips[event['region']] += 1
            continue
        state['audit_selected'] += 1
        if selection == 'replacement':
            state['audit_replacements'] += 1
            state['audit_replacement_pending'] = 0
        if outcome == 'checked':
            state['audit_checked'] += 1
        elif outcome == 'failed':
            state['audit_failed'] += 1
            state['audit_replacement_pending'] = 1
        else:
            return None  # A mismatch aborts the run; an unfinished audit never completed.
    return reasons, region_skips


def salary_audit_problems(stats):
    """Shared publication rule for salary prefilter accounting. Returns problem strings."""
    regions = stats.get('regions')
    if not isinstance(regions, dict) or not all(isinstance(region, dict) for region in regions.values()):
        return ['salary prefilter statistics are malformed']
    prefiltered = {name: region.get('prefiltered', 0) for name, region in regions.items()}
    options = stats.get('optimizations', {})
    if not all(type(value) is int and value >= 0 for value in prefiltered.values()) or not isinstance(options, dict):
        return ['salary prefilter statistics are malformed']
    skipped = sum(prefiltered.values())
    if not options.get('salary_prefilter'):
        return ['salary exclusions without enabled prefilter'] if skipped else []
    if stats.get('salary_audit_version') != SALARY_AUDIT_VERSION:
        return ['unsupported salary audit statistics']
    total = _counter_values(stats.get('prefilter'), AUDIT_COUNTERS + SALARY_REASONS)
    by_reason = stats.get('prefilter_by_reason')
    reasons = ({reason: _counter_values(by_reason.get(reason), AUDIT_COUNTERS) for reason in SALARY_REASONS}
               if isinstance(by_reason, dict) and set(by_reason) == set(SALARY_REASONS) else None)
    failed = stats.get('counts', {}).get('final_failed', 0) if isinstance(stats.get('counts'), dict) else None
    if total is None or reasons is None or None in reasons.values() or type(failed) is not int:
        return ['salary prefilter statistics are malformed']
    problems = []
    for reason, state in reasons.items():
        # Every unverifiable audit is either replaced or still pending at the end of the run.
        if (state['eligible'] != state['skipped'] + state['audit_selected']
                or state['audit_selected'] != state['audit_checked'] + state['audit_failed']
                or state['audit_failed'] != state['audit_replacements'] + state['audit_replacement_pending']
                or state['audit_replacement_pending'] > 1 or state['audit_mismatch']
                or (state['skipped'] and not state['audit_checked'])
                or total[reason] != state['skipped']):
            problems.append(f'salary audit for {reason} did not pass')
    if (any(total[key] != sum(state[key] for state in reasons.values()) for key in AUDIT_COUNTERS)
            or total['skipped'] != skipped or total['audit_failed'] > failed):
        problems.append('salary prefilter totals do not match')
    replayed = _replay(stats.get('prefilter_events'), regions)
    if replayed is None or replayed[0] != reasons or replayed[1] != prefiltered:
        problems.append('salary audit events do not match the selection rules')
    return problems
