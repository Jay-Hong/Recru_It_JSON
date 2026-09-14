"""Verified snapshots, list readiness, and aggregate diagnostics."""

from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
from importlib.resources import files
import json
import logging
import os
from pathlib import Path
import re
import time
from urllib.parse import urlsplit
import uuid

from selenium.common.exceptions import JavascriptException, WebDriverException
from selenium.webdriver.common.by import By


class VerificationError(Exception):
    pass


class EvidenceUnavailable(VerificationError):
    pass


class FormatMismatch(VerificationError):
    pass


class ServerUnavailable(Exception):
    """Stop this run without sending further crawler requests."""


class ObservationUnavailable(Exception):
    """The browser or page-wide evidence is unavailable; stop the run."""


class ClickNotReady(Exception):
    """The target did not settle at an unobstructed click point in time."""


def quiet_browser_logging():
    # WebDriver DEBUG includes full script results and performance-log payloads.
    # Keep crawler diagnostics enabled, but never log these transport payloads.
    for name in ('selenium', 'selenium.webdriver.remote.remote_connection',
                 'urllib3', 'urllib3.connectionpool'):
        logging.getLogger(name).setLevel(logging.WARNING)


def observer_source():
    # Use Selenium's bundled visibility rules, including ancestor overflow, rather
    # than maintaining another approximation of which text WebDriver exposes.
    displayed = files('selenium.webdriver.remote').joinpath('isDisplayed.js').read_text(encoding='utf-8')
    return 'window.__recruDisplayed = (' + displayed + ');\n' + Path(__file__).with_name('observer.js').read_text(encoding='utf-8')


def rolling_max(timestamps, seconds=60):
    """Maximum request starts in any half-open interval [t, t + seconds)."""
    ordered = sorted(timestamps)
    left = peak = 0
    for right, timestamp in enumerate(ordered):
        while ordered[left] <= timestamp - seconds:
            left += 1
        peak = max(peak, right - left + 1)
    return peak


def request_sequence(stack):
    while stack:
        for frame in stack.get('callFrames', []):
            match = re.fullmatch(r'recru_request_(\d+)', frame.get('functionName', ''))
            if match:
                return int(match.group(1))
        stack = stack.get('parent')
    return None


class Observation:
    def __init__(self, driver, source_url):
        quiet_browser_logging()
        self.driver = driver
        self.site_host = urlsplit(source_url).hostname
        self.started = time.monotonic()
        self.phase = 'initial'
        self.number = 0
        self.requests = []
        self.active_requests = {}
        self.stats = {
            'schema': 1, 'run_id': os.environ.get('RECRU_RUN_ID') or str(uuid.uuid4()),
            'started_at': datetime.now(timezone.utc).isoformat(),
            'complete': False, 'regions': {}, 'counts': Counter(),
            'seconds': defaultdict(float), 'attempts': [], 'scrolls': [],
            'diagnostics': Counter(), 'format_mismatches': Counter(),
            'drop_reasons': Counter(),
        }
        self.driver.execute_cdp_cmd('Network.enable', {})
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': observer_source()
        })

    @contextmanager
    def timed(self, name):
        started = time.monotonic()
        try:
            yield
        finally:
            self.stats['seconds'][name] += time.monotonic() - started

    def sleep(self, seconds, name):
        with self.timed(name):
            time.sleep(seconds)
        self.drain()

    def category(self, url):
        parsed = urlsplit(url)
        if parsed.scheme not in ('http', 'https'):
            return 'local'
        if parsed.hostname != self.site_host and not (parsed.hostname or '').endswith('.' + self.site_host):
            return 'external'
        if parsed.path == '/web/Jobinfo/getBoardJobDetail':
            return 'detail'
        if parsed.path == '/web/Jobinfo/getJobBoardList':
            return 'list'
        return 'other_site'

    def drain(self, stop_on_server_error=True):
        try:
            messages = self.driver.get_log('performance')
        except WebDriverException:
            self.stats['diagnostics']['network_log_missing'] += 1
            messages = []
        unavailable = False
        for entry in messages:
            message = json.loads(entry['message'])['message']
            method, params = message['method'], message['params']
            rid = params.get('requestId')
            if method == 'Network.requestWillBeSent':
                record = {
                    'request_id': rid, 'phase': self.phase,
                    'category': self.category(params['request']['url']),
                    'method': params['request'].get('method'), 'resource_type': params.get('type'),
                    'start': params['timestamp'], 'status': None, 'cached': False,
                    'sequence': request_sequence(params.get('initiator', {}).get('stack')),
                }
                if params.get('redirectResponse'):
                    record['redirect'] = True
                self.requests.append(record)
                self.active_requests[rid] = record
            elif rid in self.active_requests:
                record = self.active_requests[rid]
                if method == 'Network.requestServedFromCache':
                    record['cached'] = True
                elif method == 'Network.responseReceived':
                    response = params['response']
                    record.update(status=response['status'], response_seconds=params['timestamp'] - record['start'])
                    record['cached'] |= response.get('fromDiskCache', False) or response.get('fromServiceWorker', False)
                    if response['status'] in (429, 503) and record['category'] in ('detail', 'list', 'other_site'):
                        unavailable = True
                        self.stats['counts']['server_unavailable'] += 1
                        # We stop instead of retrying, including when Retry-After is present.
                        record['retry_after_present'] = any(key.lower() == 'retry-after' for key in response.get('headers', {}))
                elif method == 'Network.loadingFinished':
                    record['finished_seconds'] = params['timestamp'] - record['start']
                    record['bytes'] = params['encodedDataLength']
                elif method == 'Network.loadingFailed':
                    record['failed'] = True
        try:
            if self.driver.execute_script('return Boolean(window.__recruObserver && window.__recruObserver.unavailable())'):
                unavailable = True
                self.stats['counts']['server_unavailable'] = max(1, self.stats['counts']['server_unavailable'])
        except WebDriverException:
            # Missing diagnostics never relax the snapshot's identity/status checks.
            self.stats['diagnostics']['page_status_missing'] += 1
        if unavailable and stop_on_server_error:
            raise ServerUnavailable('Source returned 429 or 503; keeping the last validated result')

    def begin_collection(self):
        self.drain()
        self.phase = 'collection'

    def salary_card(self, card):
        try:
            return self.driver.execute_script('return window.__recruObserver.salaryCard(arguments[0])', card)
        except JavascriptException as error:
            self.require_observer()
            raise EvidenceUnavailable('salary_card_unavailable') from error

    def list_state(self):
        self.drain()
        try:
            return self.driver.execute_script('return window.__recruObserver.listState()')
        except WebDriverException as error:
            raise ObservationUnavailable('list_readiness_unavailable') from error

    def wait_list(self, before, first=False, timeout=5):
        started = time.monotonic()
        while True:
            state = self.list_state()
            elapsed = time.monotonic() - started
            settled = not state['pending'] and state['count'] == state['modelCount']
            if settled and (state['complete'] or state['count'] > before['count']):
                return state, 'complete' if state['complete'] else 'grown', elapsed
            # The first scroll can target a card already in view. This is a
            # warm-up only, never an end-of-list inference.
            if (first and elapsed >= 2.5 and settled and state['count'] == before['count']
                    and state['events'] == before['events']):
                return state, 'initial_no_request', elapsed
            if elapsed >= timeout:
                raise EvidenceUnavailable('list_did_not_settle_or_grow')
            self.sleep(.1, 'scroll_ready_wait')

    def compare_cards(self, simple, sites, pays):
        overview = self.driver.execute_script('return window.__recruObserver.overview()')
        self.stats['user_agent'] = overview['userAgent']
        cards = overview['cards']
        if not (len(cards) == len(simple) == len(sites) == len(pays)):
            raise EvidenceUnavailable('card_column_count')
        differences = Counter()
        for index, card in enumerate(cards):
            for name, expected in [('simple', simple[index]), ('site', sites[index]), ('pay', pays[index])]:
                if card[name] != expected:
                    differences[name] += 1
        self.stats['card_comparison'] = {'count': len(cards), 'mismatches': dict(differences),
                                         'payment_units': dict(Counter(card['priceDiv'] for card in cards))}
        if differences:
            raise EvidenceUnavailable('card_columns_differ')

    def start_attempt(self, region, retry):
        self.number += 1
        record = {'number': self.number, 'region': region, 'retry': retry, 'outcome': 'unfinished'}
        self.stats['attempts'].append(record)
        return record

    def require_observer(self):
        try:
            health = self.driver.execute_script(
                'return window.__recruObserver ? window.__recruObserver.health() : null')
        except WebDriverException as error:
            raise ObservationUnavailable('browser_health_unavailable') from error
        if not health or not health.get('available'):
            raise ObservationUnavailable('page_observer_unavailable')
        return health

    def arm(self, card, region, retry, record=None, timeout=3):
        if record is None:
            record = self.start_attempt(region, retry)
        self.drain()
        deadline = time.monotonic() + timeout
        with self.timed('previous_request_wait'):
            while self.require_observer()['pendingDetail']:
                if time.monotonic() >= deadline:
                    raise EvidenceUnavailable('previous_detail_pending')
                self.sleep(.1, 'previous_request_poll')
        try:
            self.driver.execute_script('return window.__recruObserver.arm(arguments[0], arguments[1])', card, record['number'])
        except JavascriptException as error:
            self.require_observer()
            raise EvidenceUnavailable('cannot_arm_observation') from error
        return record

    def begin_movement(self, card, record, stable_seconds):
        self.require_observer()
        self.driver.execute_script(
            'window.__recruObserver.beginMovement(arguments[0], arguments[1], arguments[2])',
            card, record['number'], stable_seconds)

    def wait_clickable(self, record, timeout):
        started = time.monotonic()
        try:
            while True:
                self.drain()
                state = self.driver.execute_script(
                    'return window.__recruObserver.movementStatus(arguments[0])', record['number'])
                record['click_readiness'] = state
                if state['ok']:
                    return
                if time.monotonic() - started >= timeout:
                    raise ClickNotReady(state['reason'])
                self.sleep(.05, 'click_ready_poll')
        finally:
            elapsed = time.monotonic() - started
            record['click_ready_wait_seconds'] = elapsed
            self.stats['seconds']['click_readiness_check'] += elapsed

    def read(self, timeout=3):
        """Read only when identity, request completion, and every field agree."""
        started = time.monotonic()
        last = {}
        while time.monotonic() - started < timeout:
            with self.timed('verification'):
                try:
                    last = self.driver.execute_script('return window.__recruObserver.snapshot()')
                except JavascriptException as error:
                    self.require_observer()
                    raise EvidenceUnavailable('snapshot_unavailable') from error
            if last['ok']:
                self.compare_legacy(last['raw'])
                return last['raw']
            if last.get('reason') == 'source_unavailable':
                self.stats['counts']['server_unavailable'] += 1
                raise ServerUnavailable('Source returned 429 or 503; keeping the last validated result')
            self.drain()
            with self.timed('verification_wait'):
                time.sleep(.1)
        raise VerificationError(last.get('reason', 'verification_timeout'))

    def compare_legacy(self, raw):
        """The legacy read is diagnostic only. Save the verified atomic snapshot."""
        with self.timed('legacy_comparison'):
            selectors = self.driver.execute_script('return window.__recruObserver.selectors')
            different = []
            for name, selector in selectors.items():
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if name in ('etcs', 'people'):
                    legacy = [element.text for element in elements]
                elif name == 'imageURL':
                    legacy = elements[0].get_attribute('src') if elements else ''
                else:
                    if not elements:
                        raise VerificationError('legacy_element_disappeared')
                    legacy = elements[0].text
                if raw[name] != legacy:
                    different.append(name)
            # Exclude comparisons made while another update changed the snapshot.
            after = self.driver.execute_script('return window.__recruObserver.snapshot()')
            if not after['ok'] or after['raw'] != raw:
                raise VerificationError('changed_during_comparison')
            self.stats['counts']['format_comparisons'] += 1
            if different:
                self.stats['format_mismatches'].update(different)
                raise FormatMismatch('legacy_text_differs: ' + ','.join(different))

    def finish_attempt(self, record, outcome):
        record['outcome'] = outcome
        self.stats['counts'][outcome] += 1
        try:
            page = self.driver.execute_script(
                'window.__recruObserver.stopMovement(arguments[0]); '
                'return window.__recruObserver.summary(arguments[0])', record['number'])
            if page['attempt'] and page['attempt']['number'] == record['number']:
                record['ready_seconds'] = page['attempt']['readySeconds']
                clicked = page['attempt'].get('clicked')
                if clicked is not None:
                    record['browser_click_seconds'] = clicked / 1000
            for browser_request in page['requests']:
                if browser_request['attempt'] == record['number']:
                    matches = [r for r in self.requests if r['sequence'] == browser_request['sequence']]
                    if len(matches) == 1:
                        matches[0]['attempt'] = record['number']
                    else:
                        self.stats['diagnostics']['request_link_missing'] += 1
            self.stats['diagnostics']['page_observer_errors'] = page['diagnosticErrors']
        except WebDriverException:
            self.stats['diagnostics']['page_summary_missing'] += 1

    def save(self, crawler_stats, reason):
        self.drain(stop_on_server_error=False)
        self.stats['close_reason'] = reason
        self.stats['elapsed_seconds'] = time.monotonic() - self.started
        self.stats['saved'] = crawler_stats.get('item_scraped_count', 0)
        self.stats['dropped'] = crawler_stats.get('item_dropped_count', 0)
        self.stats['spider_errors'] = crawler_stats.get('spider_exceptions/count', sum(
            value for key, value in crawler_stats.items()
            if key.startswith('spider_exceptions/') and key != 'spider_exceptions/count' and isinstance(value, int)
        ))
        grouped = defaultdict(list)
        for record in self.requests:
            if record['category'] != 'local':
                grouped[(record['phase'], record['category'])].append(record)
        network = {}
        for (phase, category), records in grouped.items():
            network.setdefault(phase, {})[category] = {
                'requests': len(records), 'cached': sum(r['cached'] for r in records),
                'rolling_60s_max': rolling_max([r['start'] for r in records]),
                'status': dict(Counter(str(r['status']) for r in records)),
                'methods': dict(Counter(str(r['method']) for r in records)),
            }
        # Both category peaks and the aggregate peak are needed: their peaks can occur at different times.
        network['collection_site_rolling_60s_max'] = rolling_max([
            r['start'] for r in self.requests if r['phase'] == 'collection' and r['category'] in ('detail', 'list', 'other_site')
        ])
        self.stats['network'] = network
        self.stats['network_requests'] = self.requests
        target = Path(os.environ.get('RECRU_STATS_PATH', 'recru_stats.json'))
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + '.tmp')
        temporary.write_text(json.dumps(self.stats, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(target)
