"""Explicit live smoke test: python tests/live_probe.py (no output publication)."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.observation import Observation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scrolls', type=int, default=0)
    parser.add_argument('--region')
    parser.add_argument('--window-size', default=None)
    parser.add_argument('--limit', type=int, default=8)
    args = parser.parse_args()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    if args.window_size:
        options.add_argument('--window-size=' + args.window_size)
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(options=options)
    request_kinds = Counter()
    original_get_log = driver.get_log

    def classified_log(kind):
        messages = original_get_log(kind)
        if kind == 'performance':
            for entry in messages:
                message = json.loads(entry['message'])['message']
                if message['method'] == 'Network.requestWillBeSent':
                    params = message['params']
                    category = observer.category(params['request']['url'])
                    if category in ('detail', 'list'):
                        request_kinds[(category, params['request']['method'], params.get('type'))] += 1
        return messages

    driver.get_log = classified_log
    observer = Observation(driver, 'https://ildao.com/recruit')
    try:
        driver.get('https://ildao.com/recruit')
        observer.sleep(5, 'initial_wait')
        observer.begin_collection()
        cards = driver.find_elements(By.CSS_SELECTOR, 'div.scrollsection > div.box.pointer')
        for _ in range(args.scrolls):
            cards[-1].location_once_scrolled_into_view
            observer.sleep(4, 'scroll_wait')
            cards = driver.find_elements(By.CSS_SELECTOR, 'div.scrollsection > div.box.pointer')
        if args.region:
            overview = driver.execute_script('return __recruObserver.overview().cards')
            first = 0
            for index, entry in enumerate(overview):
                if first == 0 and not any(word in entry['simple'] for word in ('D-', '간편지원', '상시')):
                    first = index
            cards = [card for index, card in enumerate(cards) if index >= first and
                     args.region in overview[index]['site'] and '간편지원' not in overview[index]['simple']]
        print('cards', len(cards), flush=True)
        for number, card in enumerate(cards[:args.limit]):
            card.location_once_scrolled_into_view
            observer.sleep(3, 'click_wait')
            record = observer.arm(card, 'smoke', False)
            card.click()
            observer.sleep(.5, 'post_click_wait')
            try:
                raw = observer.read()
            except Exception as error:
                snapshot = driver.execute_script('return window.__recruObserver.snapshot()')
                print('failure', number, type(error).__name__, str(error).splitlines()[0],
                      {key: value for key, value in snapshot.items() if key != 'raw'}, flush=True)
                if snapshot.get('ok'):
                    elements = driver.find_elements(By.CSS_SELECTOR, '#detail_info div.ft11.col_blu02')
                    for index, element in enumerate(elements):
                        old, new = element.text, snapshot['raw']['etcs'][index]
                        if old != new:
                            masked = lambda value: ''.join(character if character.isspace() else 'X' for character in value)
                            ancestors = driver.execute_script('''
                                let el=arguments[0], result=[];
                                while(el){const s=getComputedStyle(el),r=el.getBoundingClientRect();
                                result.push({tag:el.tagName,cls:el.className,display:s.display,visibility:s.visibility,
                                opacity:s.opacity,overflow:s.overflow,whiteSpace:s.whiteSpace,rect:[r.x,r.y,r.width,r.height]});el=el.parentElement}
                                return result''', element)
                            print('text-difference', {'old': masked(old), 'new': masked(new), 'ancestors': ancestors}, flush=True)
                raise SystemExit(1) from None
            observer.drain()
            observer.finish_attempt(record, 'verified')
            print('verified', number, 'image', bool(raw['imageURL']), 'ready_seconds', record.get('ready_seconds'), flush=True)
        print(json.dumps({'counts': observer.stats['counts'], 'diagnostics': observer.stats['diagnostics'],
                          'linked_requests': sum('attempt' in r for r in observer.requests)}, ensure_ascii=False))
        print('request_kinds', [{'category': category, 'method': method, 'type': kind, 'count': count}
                                 for (category, method, kind), count in request_kinds.items()])
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
