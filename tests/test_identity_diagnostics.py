"""Real XHR diagnostics against a local HTTP fixture; no recruitment-site traffic."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import sys
import threading
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import Observation, observer_source
from recru_it.validate_run import validate
from test_browser_stage1 import FIXTURE
from test_stage1 import valid_run


PRIVATE = 'private-body-and-error-message-fixture'
PAGE = re.sub(r'class FakeXHR.*?window.XMLHttpRequest = FakeXHR;', '', FIXTURE, flags=re.S)
PAGE = PAGE.replace("'new'", "'101'").replace("'old'", "'100'") + r'''
<script>
window.responseEvents = 0;
document.querySelector('.box.pointer').onclick = () => {
  const xhr = new XMLHttpRequest(); xhr.open('POST', '/web/Jobinfo/getBoardJobDetail');
  xhr.responseType = window.fixtureResponseType || '';
  xhr.onload = () => {
    responseEvents++;
    let reply;
    try { reply = xhr.responseType === 'json' ? xhr.response : JSON.parse(xhr.responseText); }
    catch (_) { reply = null; }
    window.appReceivedPrivateField = Boolean(reply && reply.message);
    if (reply && reply.rescode == 200 && reply.data && !window.keepModel) {
      vm.recuitDetail = {...currentModel, idx: reply.data.idx}; render();
    }
    if (window.clearModel) vm.recuitDetail = null;
    if (window.unreadableAfterLoad) window.failDiagnosticReads = true;
  };
  xhr.send(JSON.stringify({idx:vm.normalRecruList[0].idx}));
};
</script>
'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = PAGE.encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        self.server.posts.append((self.path, self.rfile.read(int(self.headers['Content-Length']))))
        data = self.server.payload
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_):
        pass


class IdentityDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1600,1000')
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.server.posts = []
        self.payload({'rescode': 200, 'data': {'idx': '101', 'phone': PRIVATE}, 'message': PRIVATE})
        self.driver.get(self.url)
        self.observation = Observation(self.driver, self.url)
        self.driver.execute_script(observer_source())
        self.card = self.driver.find_element(By.CSS_SELECTOR, '.box.pointer')

    def payload(self, body):
        self.server.payload = body if isinstance(body, bytes) else json.dumps(body).encode()

    def click(self, number=1, lose_network_log=False):
        record = self.observation.arm(self.card, '서울', number > 1)
        self.card.click()
        WebDriverWait(self.driver, 2, poll_frequency=.01).until(lambda driver: driver.execute_script(
            'return __recruObserver.summary().requests.some(r => r.done)'))
        self.observation.drain()
        snapshot = self.driver.execute_script('return __recruObserver.snapshot()')
        if lose_network_log:
            self.observation.requests = []
        self.observation.finish_attempt(record, 'verified' if snapshot['ok'] else 'verification_failed')
        self.assertEqual(len(record['detail_responses']), 1)
        self.assertNotIn(PRIVATE, json.dumps(self.observation.stats))
        return record, snapshot

    def test_normal_text_and_json_capture_metadata_without_changing_response_or_request(self):
        for response_type, code in [('', 200), ('json', '200')]:
            with self.subTest(response_type=response_type):
                self.payload({'rescode': code, 'data': {'idx': '101', 'content': PRIVATE}, 'message': PRIVATE})
                self.driver.execute_script('fixtureResponseType=arguments[0]', response_type)
                record, snapshot = self.click()
                self.assertTrue(snapshot['ok'], snapshot)
                self.assertEqual(record['job_id'], '101')
                self.assertEqual(record['identity'], {'state': 'matches', 'model_present': True,
                    'model_replaced': True, 'model_job_id': '101'})
                response = record['detail_responses'][0]
                self.assertEqual(response['job_id'], '101')
                self.assertIsNotNone(response['request_id'])
                self.assertEqual(response['response'], {'state': 'captured', 'rescode': 200,
                    'rescode_state': 'numeric', 'data_state': 'object', 'job_id': '101'})
                self.assertTrue(self.driver.execute_script('return appReceivedPrivateField'))
        self.assertEqual(len(self.server.posts), 2)
        self.assertTrue(all(json.loads(body) == {'idx': '101'} for _, body in self.server.posts))

    def test_business_error_and_empty_data_keep_previous_model_and_never_expose_message(self):
        self.payload({'rescode': 404, 'data': None, 'message': PRIVATE})
        record, snapshot = self.click()
        self.assertEqual(snapshot, {'ok': False, 'reason': 'identity'})
        self.assertEqual(record['identity'], {'state': 'unchanged', 'model_present': True,
            'model_replaced': False, 'model_job_id': '100'})
        self.assertEqual(record['detail_responses'][0]['response'], {'state': 'captured',
            'rescode': 404, 'rescode_state': 'numeric', 'data_state': 'null', 'job_id': None})

    def test_http_and_business_success_with_missing_data_are_not_treated_as_valid_detail(self):
        self.payload({'rescode': 200})
        record, snapshot = self.click()
        self.assertFalse(snapshot['ok'])
        self.assertEqual(record['identity']['state'], 'unchanged')
        self.assertEqual(record['detail_responses'][0]['response']['data_state'], 'missing')

    def test_missing_model_is_distinguished_from_unchanged_model(self):
        self.driver.execute_script('clearModel=true')
        record, snapshot = self.click()
        self.assertFalse(snapshot['ok'])
        self.assertEqual(record['identity'], {'state': 'missing', 'model_present': False,
            'model_replaced': False, 'model_job_id': None})

    def test_replaced_model_with_wrong_id_is_distinguished(self):
        self.payload({'rescode': 200, 'data': {'idx': '202'}})
        record, snapshot = self.click()
        self.assertFalse(snapshot['ok'])
        self.assertEqual(record['job_id'], '101')
        self.assertEqual(record['identity'], {'state': 'different_id', 'model_present': True,
            'model_replaced': True, 'model_job_id': '202'})
        self.assertEqual(record['detail_responses'][0]['response']['job_id'], '202')

    def test_same_job_retry_keeps_response_and_network_id_with_each_attempt(self):
        self.payload({'rescode': 404, 'data': None})
        first, _ = self.click()
        self.payload({'rescode': 200, 'data': {'idx': '101'}})
        second, snapshot = self.click(2)
        self.assertTrue(snapshot['ok'])
        self.assertEqual(first['job_id'], second['job_id'])
        before, after = first['detail_responses'][0], second['detail_responses'][0]
        self.assertNotEqual(before['sequence'], after['sequence'])
        self.assertNotEqual(before['request_id'], after['request_id'])
        self.assertEqual(before['response']['rescode'], 404)
        self.assertEqual(after['response']['rescode'], 200)
        self.assertEqual(len(self.server.posts), 2)

    def test_missing_network_log_preserves_browser_diagnostic_without_inventing_request_id(self):
        record, snapshot = self.click(lose_network_log=True)
        self.assertTrue(snapshot['ok'])
        self.assertIsNone(record['detail_responses'][0]['request_id'])
        self.assertEqual(record['detail_responses'][0]['response']['rescode'], 200)
        self.assertEqual(self.observation.stats['diagnostics']['request_link_missing'], 1)

    def test_invalid_and_empty_bodies_are_described_without_retaining_them(self):
        for payload, state in [(b'', 'empty'), (PRIVATE.encode(), 'invalid_json'), (b'[]', 'not_object')]:
            with self.subTest(state=state):
                self.payload(payload)
                record, snapshot = self.click()
                self.assertFalse(snapshot['ok'])
                self.assertEqual(record['detail_responses'][0]['response'], {'state': state})

    def test_data_shapes_and_non_numeric_codes_never_leak_values(self):
        self.driver.execute_script('keepModel=true')
        for data, state in [(None, 'null'), ({}, 'empty_object'), ([], 'empty_array'),
                            ([PRIVATE], 'array'), ('', 'empty_string'), (PRIVATE, 'string')]:
            with self.subTest(state=state):
                self.payload({'rescode': PRIVATE, 'data': data})
                record, _ = self.click()
                response = record['detail_responses'][0]['response']
                self.assertEqual(response['rescode_state'], 'unsupported')
                self.assertIsNone(response['rescode'])
                self.assertEqual(response['data_state'], state)

    def test_non_identifier_values_and_unsafe_numeric_ids_are_not_exported(self):
        for value in [PRIVATE, '101\nprivate', 9007199254740992]:
            with self.subTest(value_type=type(value).__name__):
                self.payload({'rescode': 200, 'data': {'idx': value}})
                record, snapshot = self.click()
                self.assertFalse(snapshot['ok'])
                self.assertIsNone(record['identity']['model_job_id'])
                self.assertIsNone(record['detail_responses'][0]['response']['job_id'])

    def test_large_diagnostic_body_does_not_change_successful_snapshot(self):
        self.payload({'rescode': 200, 'data': {'idx': '101'}, 'content': PRIVATE * 10000})
        record, snapshot = self.click()
        self.assertTrue(snapshot['ok'], snapshot)
        self.assertEqual(record['detail_responses'][0]['response'], {'state': 'too_large'})

    def test_body_read_failure_is_diagnostic_only_and_leaves_application_success_intact(self):
        self.driver.execute_script('''
            const original=Object.getOwnPropertyDescriptor(XMLHttpRequest.prototype,'responseText');
            Object.defineProperty(XMLHttpRequest.prototype,'responseText', {
              get() { if(window.failDiagnosticReads) throw Error('private diagnostic error');
                return original.get.call(this); }, configurable:true});
            unreadableAfterLoad=true;
        ''')
        record, snapshot = self.click()
        self.assertTrue(snapshot['ok'], snapshot)
        self.assertEqual(record['detail_responses'][0]['response'], {'state': 'unavailable'})
        self.assertEqual(self.observation.stats['diagnostics']['response_diagnostic_missing'], 1)
        self.assertNotIn('private diagnostic error', json.dumps(self.observation.stats))

    def test_list_responses_are_not_parsed_for_detail_diagnostics(self):
        self.driver.execute_async_script('''
            const done=arguments[0], xhr=new XMLHttpRequest();
            xhr.open('POST','/web/Jobinfo/getJobBoardList');
            xhr.onload=()=>{}; xhr.addEventListener('loadend',()=>done(true));
            xhr.send('{}');
        ''')
        records = self.driver.execute_script('return __recruObserver.summary(null).requests')
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['kind'], 'list')
        self.assertNotIn('response_diagnostic', records[0])
        self.assertNotIn('job_id', records[0])


class DiagnosticPublicationTests(unittest.TestCase):
    def test_missing_new_diagnostics_do_not_change_the_existing_publication_policy(self):
        items, stats = valid_run()
        stats['identity_diagnostics_version'] = 1
        stats['diagnostics'] = {'identity_diagnostic_missing': 1, 'response_diagnostic_missing': 1}
        validate(items, stats, 'current')


if __name__ == '__main__':
    unittest.main()
