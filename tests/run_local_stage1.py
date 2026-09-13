"""Full, normally paced local crawl. Outputs stay in a separate temporary folder."""
from contextlib import redirect_stdout, redirect_stderr
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import uuid

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recru_it'))
from recru_it.spiders.recru_it import Recru_It_Spider
from recru_it.validate_run import validate


def main():
    target = Path(tempfile.mkdtemp(prefix='recru-stage1-'))
    os.environ['RECRU_RUN_ID'] = str(uuid.uuid4())
    os.environ['RECRU_STATS_PATH'] = str(target / 'stats.json')
    settings = Settings()
    settings.setmodule('recru_it.settings')
    settings.set('FEED_URI', None, priority='cmdline')
    settings.set('FEEDS', {str(target / 'result.json'): {'format': 'json', 'encoding': 'utf-8', 'indent': 4}}, priority='cmdline')
    # Keep the project's log level, matching Actions (Scrapy defaults to DEBUG).
    settings.set('LOG_FILE', str(target / 'crawl.log'), priority='cmdline')
    process = CrawlerProcess(settings)
    crawler = process.create_crawler(Recru_It_Spider)
    stopped = threading.Event()
    output = sys.stdout
    print('Local test folder:', target, flush=True)

    def progress():
        while not stopped.wait(45):
            observer = getattr(crawler.spider, 'observation', None)
            if observer:
                print(json.dumps({'elapsed_minutes': round((time.monotonic() - observer.started) / 60, 1),
                                  'scrolls': len(observer.stats['scrolls']), 'counts': dict(observer.stats['counts']),
                                  'completed_regions': sum(r['complete'] for r in observer.stats['regions'].values())}),
                      file=output, flush=True)

    threading.Thread(target=progress, daemon=True).start()
    try:
        with (target / 'console.log').open('w', encoding='utf-8') as log, redirect_stdout(log), redirect_stderr(log):
            process.crawl(crawler)
            process.start()
    finally:
        stopped.set()
    stats = json.loads((target / 'stats.json').read_text())
    items = json.loads((target / 'result.json').read_text())
    try:
        validate(items, stats, os.environ['RECRU_RUN_ID'])
    except ValueError as error:
        print('VALIDATION FAILED:', error)
        print(json.dumps({'counts': stats['counts'], 'format_mismatches': stats['format_mismatches'],
                          'diagnostics': stats['diagnostics']}, ensure_ascii=False))
        raise SystemExit(1) from None
    print(json.dumps({'validated': True, 'saved': len(items), 'seconds': stats['elapsed_seconds'],
                      'counts': stats['counts'], 'diagnostics': stats['diagnostics']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
