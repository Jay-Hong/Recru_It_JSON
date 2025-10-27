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
    'scroll_range': (50, 53),           # 스크롤 반복 횟수 (min, max)
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
            'sleep_before': (3, 14),
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

# 지역별 수동 추가 채용정보
# 각 지역의 크롤링 결과 맨 앞에 추가됩니다
MANUAL_JOBS_BY_REGION = {
    '서울': [
        # {
        #     'title': '[예제] 서울 강남 비계 작업자 모집',
        #     'site': '서울 강남구',
        #     'type': '비계/동바리',
        #     'pay': '일급 18만원 이상',
        #     'etc1': '숙식제공',
        #     'etc2': '4대보험',
        #     'etc3': '장기근무',
        #     'numpeople': '0명',
        #     'phone': '010-0000-0000',
        #     'detail': '강남역 인근 아파트 신축 현장\n경력 3년 이상 우대\n출퇴근 가능자',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
    ],
    '부산': [
        # 25/12/22 추가 | 26/01/24 삭제
        # {
        #     'title': '시스템동바리 팀원 구합니다',
        #     'site': '서울 성동구',
        #     'type': '비계/동바리',
        #     'pay': '일급 18만 ~ 23만원',
        #     'etc1': '숙식제공',
        #     'etc2': '출퇴근가능',
        #     'etc3': '장기근무',
        #     'numpeople': '00명',
        #     'phone': '010-9110-7515',
        #     'detail': '안녕하세요 시스템 동바리 팀원 구합니다.\n\n초보 18만원 부터 시작해 경력자 분들은 일하시는 것 보고 단가 맞춰드립니다.\n\n현장은 주로 고양에 있으며 출퇴근, 숙소 생활 다 가능하고 숙소는 화정역 부근에 있습니다.\n\n도박, 중독, 인성 안 좋으신 분들은 팀 분위기를 망치기에 받지 않습니다.\n\n일은 하시면 금방 배우고 적응하니 다른 궁금하신 것 있으시면 문자 남겨주세요 전화드리겠습니다.\n\n준비물: 신분증, 건설기초교육이수증, 안전화',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
    ],
    '경기': [
        # 25/05/01 추가 | 25/05/10 삭제
        {
            'title': '평택 삼성 소방배관공 모집 (일비지급)',
            'site': '경기 평택시',
            'type': '배관',
            'pay': '일급 15.5만 ~ 20만원',
            'etc1': '출퇴근가능',
            'etc2': '4대보험',
            'etc3': '장기근무',
            'numpeople': '8명',
            'phone': '010-3249-8191',
            'detail': '평택 삼성 소방배관 인원 충원 합니다.\n준기공1명, 조공 8명 급구\n초보상관 없이 성실한분 환영^^\n\n준기공20만, 조공15.5 일비3만 + 연장시 4만',
            'imageURL': '',
            'time': '',
            'sponsored': ''
        },
        # 25/05/01 추가 | 25/05/10 삭제 - 전화번호 중목으로 안나옴
        {
            'title': '평택 포승공단 소방배관 조공 8명 인원모집 (일비4만)',
            'site': '경기 평택시',
            'type': '배관',
            'pay': '일급 15.5만원',
            'etc1': '일비4만',
            'etc2': '4대보험',
            'etc3': '장기근무',
            'numpeople': '8명',
            'phone': '010-3249-8191',
            'detail': '평택 포승공단 소방배관 조공 8명 인원모집합니다\n연장 주 3회 진행중입니다.\n\n배관 구릅타입\n\n연락처: 010-3249-8191\n문자 남겨주시면 연락드리겠습니다.',
            'imageURL': '',
            'time': '',
            'sponsored': ''
        },
        # 25/04/08 추가 | 25/04/22 삭제
        # {
        #     'title': '고덕 P4 양중 인원 모집',
        #     'site': '경기 평택시',
        #     'type': '양중',
        #     'pay': '일급 16만원',
        #     'etc1': '숙식제공',
        #     'etc2': '4대보험',
        #     'etc3': '장기근무',
        #     'numpeople': '3명',
        #     'phone': '010-8295-9767',
        #     'detail': '주 2회 연장 7시부터5시 휴식 시간 많음\n아령 5키로 들수 있으면 아무나 할수있는 일\n지원 바랍니다',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 25/04/07 추가 | 25/04/21 삭제
        # {
        #     'title': '평택 삼성 케미컬 및 셋업 신규자 팀원모집',
        #     'site': '경기 평택시',
        #     'type': '배관',
        #     'pay': '협의 후 결정',
        #     'etc1': '숙식제공',
        #     'etc2': '4대보험',
        #     'etc3': '장기근무',
        #     'numpeople': '3~4명',
        #     'phone': '010-2492-5024',
        #     'detail': '평일 근무 시간 및 주말은 연락이 힘드니 꼭 문자 남겨 주세요.\n\n1. [업체:진영]케미컬 배관 (물산) 보조공 또는 준기공 모집\n근무 시간 아침 7시~저녁5시\n휴게 시간 10시30분~11시부터 1시~2시 사이\n본인 실력에 따라 일급 협의 가능! 공수 많을 예정\n추후 3차 이전 가능\n물산 숙소 제공 가능\n\n2.[업체:세븐테크]셋업 (전자) 보조공 또는 준기공&기공\n근무 시간 아침 9시30분~저녁5시\n휴게 시간 10시30분~1시~2시 사이\n본인 실력에 따라 일급 협의 가능!\n워라벨 중요한 분은 셋업 추천!!\n⭐️만일 주말 출근이 있다면 금융 치료 가능!! 출근만 해도 0.5공수 추가⭐️\n\n덥고 추운 길에서 하는게 아닌 현장 내부에서 하는 업무로 먼지 및 밖의 온도와 전혀 상관이 없습니다 :)',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 25/04/07 추가 | 25/04/21 삭제
        # {
        #     'title': '추락망 설치',
        #     'site': '경기 평택시',
        #     'type': '기타',
        #     'pay': '일급 22만원',
        #     'etc1': '장기근무',
        #     'etc2': '단기근무',
        #     'etc3': '출퇴근가능',
        #     'numpeople': '2명',
        #     'phone': '010-5836-7163',
        #     'detail': 'P5 154KV 추락망 설치\nTL 로 작업합니다\n교육  건강검진 1일\n다음날 홍체 등록후 입문\n아침 점심 제공',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 25/03/24 추가 | 25/04/11 삭제
        # {
        #     'title': '금속인테리어 기공 직원모집합니다',
        #     'site': '경기 남양주시',
        #     'type': '금속',
        #     'pay': '협의 후 결정',
        #     'etc1': '숙식제공',
        #     'etc2': '4대보험',
        #     'etc3': '장기근무',
        #     'numpeople': '1명',
        #     'phone': '010-5597-4333',
        #     'detail': '금속인테리어 기공 직원하실분 구합니다\n일잘하시는분 대우 잘해드리겠습니다\n사대보험 유 퇴직금 유\n고정일당가능 일잘하시고 마음잘맞으면 최저 일수도 챙겨줄의향있음 어중이떠중이 연락말고 확실한분 연락주세요',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 25/03/22 추가 | 25/04/07 삭제
        # {
        #     'title': '배관헬퍼 모집합니다',
        #     'site': '경기 안성시',
        #     'type': '배관',
        #     'pay': '일급 15만원',
        #     'etc1': '숙식제공',
        #     'etc2': '4대보험',
        #     'etc3': '장기근무',
        #     'numpeople': '8명',
        #     'phone': '010-9557-8155',
        #     'detail': '안성 배터리 공장에서 배관헬퍼 모집합니다\n4월초들어가며 연장및 야간진행합니다',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 25/03/20 추가 | 25/04/07 삭제
        # {
        #     'title': '고덕 덕트 조공,유도원 구합니다',
        #     'site': '경기 평택시',
        #     'type': '덕트',
        #     'pay': '일급 15.5만 ~ 17만원',
        #     'etc1': '4대보험',
        #     'etc2': '장기근무',
        #     'etc3': '출퇴근가능',
        #     'numpeople': '6명',
        #     'phone': '010-2392-4608',
        #     'detail': '덕트 조공4명, 유도원2명 구합니다!!\n조공 16.5~17, 유도원 15.5~16\n고덕 p4 복합동 (동방)\n\n재밌게 일 하시면서 일 배우실분 연락주세요!\n찔러보시는분 사절합니다.\n동반입사 가능, 출퇴근 가능하신분으로 구합니다\n숙소x,식비x\n지금 바빠서 주3~4회 연장합니다.\n근태 좋고 열심히 하실분 구해요!!',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 25/03/11 추가 | 25/04/07 삭제
        # {
        #     'title': '용인 하이닉스 조공,기공,유도원모집',
        #     'site': '경기 용인시 원삼면',
        #     'type': '방화마감',
        #     'pay': '일급 15만 ~ 17만원',
        #     'etc1': '숙식제공',
        #     'etc2': '4대보험',
        #     'etc3': '장기근무',
        #     'numpeople': '8명',
        #     'phone': '010-8436-1767',
        #     'detail': '❤용인 하이닉스 조공,기공,유도원모집❤\n\n📌 현장 : 용인 1기\n📌 업체 : 중원\n📌 공정 : 방화마감\n📌 단가 : 기공 - 200,000~협의\n    출퇴근 조공 - 170,000 (식사포함)\n    숙소 조공 - 160,000 (식사포함)\n    유도원 - 150,000 (일비 10,000 / 식사X)\n    4대보험 필수\n\n⭐ 근태 안좋으신분은 정말정말 사양 합니다 ⭐\n   공기 상당히 깁니다 / 일 어렵지 않습니다\n\n⭐ 010 8436 1767 ⭐\n\n🔥 팀장 직접 구인 🔥\n\n* 전화연결 잘 못받는경우가 많아 문자로 아래내용과 같이 보내주시면 연락드리겠습니다\n성명:\n나이:\n현장경력(이전현장명):\n연락처:\n지원현장:\n\n양식적어서 문자주시면 보다 빨리 연락드리겠습니다',
        #     'imageURL': 'https://gi.esmplus.com/hjpyooo/%EB%B0%A9%ED%99%94%EB%A7%88%EA%B0%90.jpeg',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 25/03/25 추가 | 25/04/07 삭제
        # {
        #     'title': '평택 고덕 포설 기공 구인합니다',
        #     'site': '경기 평택시',
        #     'type': '포설',
        #     'pay': '일급 17만원 이상',
        #     'etc1': '4대보험',
        #     'etc2': '장기근무',
        #     'etc3': '단기근무',
        #     'numpeople': '5명',
        #     'phone': '010-2589-2457',
        #     'detail': '*평택 P4 ph4*\n전기 포설팀\n\n광고X 팀장직접구인\n\n조공은 마감했습니다.\n\n철야근무\n\n철야 근무투입 이라서\n★★건강★★ 이상없는분\n지원부탁드립니다.\n(서류에서 다 짤려요.....)\n\n조공마감\n    기공 경력자 구인\n단가 170,000 부터 그 이상 협의\n\n2공수 주5일 토,일 휴무\n\n준비물: 신분증 통장사본\n        기초안전보건교육 이수증(1년이상)\n        본인명의 통장\n\n010-2589-2457\n문자, 전화 아무거나\n편하게 연락 주세요~',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 25/03/00 추가 | 25/03/00 삭제
        # {
        #     'title': '제목',
        #     'site': '경기 ㅇㅇ시',
        #     'type': ' ',
        #     'pay': '일급 15만원',
        #     'etc1': '숙식제공',
        #     'etc2': '4대보험',
        #     'etc3': '장기근무',
        #     'numpeople': '0명',
        #     'phone': '010-0000-0000',
        #     'detail': ' ',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
    ],
    '인천': [],
    '충남': [
        # 25/02/10 추가 | 25/02/28 삭제
        # {
        #     'title': '제목',
        #     'site': '충남 ㅇㅇ',
        #     'type': ' ',
        #     'pay': '일급 17만원 이상',
        #     'etc1': '4대보험',
        #     'etc2': '장기근무',
        #     'etc3': '출퇴근가능',
        #     'numpeople': '0명',
        #     'phone': '010-0000-0000',
        #     'detail': ' ',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
    ],
    '충북': [
        # 26/03/12 추가 | 26/03/22 삭제
        # {
        #     'title': '청주 SK하이닉스 M8현장 조공모집합니다',
        #     'site': '충북 청주시',
        #     'type': '포설/철거',
        #     'pay': '일급 15만원',
        #     'etc1': '4대보험',
        #     'etc2': '장기근무',
        #     'etc3': '출퇴근가능',
        #     'numpeople': '3명',
        #     'phone': '010-9990-0282',
        #     'detail': '급여 15만원 (일비1만원)\n\n출퇴근자 우선시 채용하며,\n근태좋으신분만 지원해주세요\n팀분위기 완전 좋습니다.\n\n주 업무 : 케이블 포설 및 철거\n근무 형태 : 주 6일 연장 및 주간 30공수\n입사 날짜 : 2026.03.16 월요일\n\n근무시간\n07:00 ~ 17:30 주간근무\n07:00 ~ 19:30 연장근무\n07:00 ~ 22:00 야간근무\n점심시간2시간 / 15:00 ~ 15:30 휴식\n\n* 전화연결 잘 못받는경우가 많아 문자로 아래내용과 같이 보 내주시면 연락드리겠습니다.\n성명:\n나이:\n현장경력(이전현장명):\n연락처:',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
        # 26/03/12 추가 | 26/03/31 삭제
        # {
        #     'title': '제목',
        #     'site': '충북 ㅇㅇ시',
        #     'type': ' ',
        #     'pay': ' ',
        #     'etc1': '4대보험',
        #     'etc2': '장기근무',
        #     'etc3': '출퇴근가능',
        #     'numpeople': ' ',
        #     'phone': '010-0000-0000',
        #     'detail': '\n[ 청주 SK 하이닉스 M15X PJT ]\n\n출 퇴 가능하신 분\n\n■회사명 : 우일계전공업\n■현장: p4\n■공종 : 전기 ( 케이블 포설)\n■근무시간 : 07:30-17:00,(연장)19:30\n■경력 : 조공 및 준조공\n■채용 인원 : 2명\n■성별 : 남 (20대 초~30대 후반)\n⬛단가 : 150000~155000\n■근무형태 : 주6일 (연장 주 2~3회)\n\n■ 담당 팀장 : 010-8743-3213\n문자 메세지로 연락 부탁드립니다.\n\n성실하신분,근태 좋으신분 많은 지원 부탁드립니다👍👍',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
    ],
    '대전': [],
    '세종': [],
    '전남': [],
    '광주': [],
    '전북': [],
    '경남': [],
    '울산': [
        # 26/01/24 삭제
        # {
        #     'title': ' ',
        #     'site': '울산',
        #     'type': ' ',
        #     'pay': '일급 15만 ~ 18만원',
        #     'etc1': '숙식제공',
        #     'etc2': '4대보험',
        #     'etc3': '장기근무',
        #     'numpeople': ' ',
        #     'phone': '010-0000-0000',
        #     'detail': ' ',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
    ],
    '경북': [],
    '대구': [
        # 25/02/10 추가 | 25/02/28 삭제
        # {
        #     'title': '제목',
        #     'site': '대구',
        #     'type': ' ',
        #     'pay': ' ',
        #     'etc1': '4대보험',
        #     'etc2': '장기근무',
        #     'etc3': '출퇴근가능',
        #     'numpeople': ' ',
        #     'phone': '010-0000-0000',
        #     'detail': ' ',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
    ],
    '강원': [],
    '그외': [
    # 25/03/26 추가 | 25/04/07 삭제
        # {
        #     'title': '금속 인테리어팀 인원 모집',
        #     'site': '전국',
        #     'type': '금속',
        #     'pay': '일급 15만원',
        #     'etc1': '숙식제공',
        #     'etc2': '장기근무',
        #     'etc3': '',
        #     'numpeople': '2명',
        #     'phone': '010-3445-9103',
        #     'detail': '조공 구합니다.\n평균 연령 30대인 젊은 팀입니다.\n오래 끈기있게 일하면서 배우실분 연락주세요.\n\n숙식 제공하며, 현재는 충남 공주 공사중입니다.\n현장일 특성상 지방가는 일 있으니 염두하고 연락주세요.\n일하고 있어서 전화못받을수도있으니 문자남겨주세요.\n안전화, 기초이수증 있어야합니다.',
        #     'imageURL': '',
        #     'time': '',
        #     'sponsored': ''
        # },
    ],
}