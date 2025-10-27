# Scrapy settings for ildao_test_with_selenium project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "recru_it"

SPIDER_MODULES = ["recru_it.spiders"]
NEWSPIDER_MODULE = "recru_it.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "ildao_test_with_selenium (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "ildao_test_with_selenium.middlewares.IldaoTestWithSeleniumSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "ildao_test_with_selenium.middlewares.IldaoTestWithSeleniumDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "recru_it.pipelines.Recru_It_Pipeline": 300,
    "recru_it.pipelines.DuplicatesPipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# 아래 수동 추가 함
FEED_URI = 'recru_result.json'
FEED_FORMAT = 'json'
FEED_EXPORT_INDENT = 4

# 크롤링 설정
CRAWL_CONFIG = {
    'scroll_range': (39, 52),           # 스크롤 반복 횟수 (min, max)
    'initial_sleep': (2, 13),           # 초기 페이지 로드 대기 시간 (초)

    'regions': [
        {
            'name': '서울',
            'keywords': ['서울'],
            'exclude_keywords': [],
            'item_limit': None,         # None = 제한 없음
            'sleep_before': (2, 5),     # 지역 크롤링 전 대기 (초)
            'sleep_between': (1, 6),    # 각 아이템 클릭 전 대기 (초)
        },
        {
            'name': '부산',
            'keywords': ['부산'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 17),
            'sleep_between': (1, 4),
        },
        {
            'name': '경기',
            'keywords': ['경기'],
            'exclude_keywords': [],
            'item_limit': 450,          # 경기는 450개 제한
            'sleep_before': (3, 23),
            'sleep_between': (1, 3),
        },
        {
            'name': '인천',
            'keywords': ['인천'],
            'exclude_keywords': [],
            'item_limit': 450,          # 인천은 450개 제한
            'sleep_before': (3, 5),
            'sleep_between': (1, 3),
        },
        {
            'name': '충남',
            'keywords': ['충남'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 7),
            'sleep_between': (1, 3),
        },
        {
            'name': '충북',
            'keywords': ['충북'],
            'exclude_keywords': [],
            'item_limit': 450,          # 충북은 450개 제한
            'sleep_before': (3, 7),
            'sleep_between': (1, 4),
        },
        {
            'name': '대전',
            'keywords': ['대전'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 7),
            'sleep_between': (1, 4),
        },
        {
            'name': '세종',
            'keywords': ['세종'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 7),
            'sleep_between': (1, 4),
        },
        {
            'name': '전남',
            'keywords': ['전남'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 17),
            'sleep_between': (1, 4),
        },
        {
            'name': '광주',
            'keywords': ['광주'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 7),
            'sleep_between': (1, 4),
        },
        {
            'name': '전북',
            'keywords': ['전북'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 7),
            'sleep_between': (1, 4),
        },
        {
            'name': '경남',
            'keywords': ['경남'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 15),
            'sleep_between': (1, 3),
        },
        {
            'name': '울산',
            'keywords': ['울산'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 7),
            'sleep_between': (1, 3),
        },
        {
            'name': '경북',
            'keywords': ['경북'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 17),
            'sleep_between': (1, 3),
        },
        {
            'name': '대구',
            'keywords': ['대구'],
            'exclude_keywords': ['부산'],  # "부산 해운대구" 제외
            'item_limit': None,
            'sleep_before': (3, 7),
            'sleep_between': (1, 3),
        },
        {
            'name': '강원',
            'keywords': ['강원'],
            'exclude_keywords': [],
            'item_limit': None,
            'sleep_before': (3, 17),
            'sleep_between': (1, 6),
        },
        {
            'name': '그외',
            'keywords': [],  # 빈 리스트 = 나머지 모든 지역
            'exclude_keywords': ['서울', '부산', '경기', '인천', '충남', '충북',
                                '대전', '세종', '전남', '광주', '전북', '경남',
                                '울산', '경북', '대구', '강원'],
            'item_limit': None,
            'sleep_before': (3, 7),
            'sleep_between': (1, 7),
        },
    ]
}