from selenium import webdriver;import scrapy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re; import time; import random
from recru_it.items import Recru_It_Item
#~/Documents/Recru_It_JSON/recru_it/recru_it/spiders/recru_it.py
class Recru_It_Spider(scrapy.Spider):
    name = "recru_it";recru_it = "ecruit";dotdcom = "o.com/r";db = "lda"
    allowed_domains = ["i"+db+"o.com"]
    start_urls = ["https://i"+db+dotdcom+recru_it]
    USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.12 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15e148 Kakaotalk 9.5.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15e148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/71.0.3578.89 Mobile/15E148 Safari/605.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/94.0.4606.52 Mobile/15e148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG-SM-G950N/KSU3CRJ1 Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/8.2 Chrome/63.0.3239.111 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; SM-A908N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S918) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S911) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S916) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S901) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S906) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S908) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/537.36 (KHTML, like Gecko, Mediapartners-Google) Chrome/117.0.5938.132 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.6',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0 LikeWise/100.6.4765.6',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84',
        'Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.95 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 CVManaged',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 AVG/117.0.0.0',

        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/108.0.5359.112 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/537.36 (KHTML, like Gecko; Mediapartners-Google) Chrome/117.0.5938.132 Mobile Safari/537.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/117.0.5938.117 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 11; moto g 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.167 Mobile Safari/537.36 OPR/77.5.4095.7517',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/285.0.570543384 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/118.0 Firefox/118.0',
        'Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G780F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 9; JAT-L41) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G390F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G990B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G780G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G780G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/20.0 Chrome/106.0.5249.126 Mobile Safari/537.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/117.0.5938.117 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/284.0.569260749 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.4 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/114.0.5735.99 Mobile/15E148 Safari/604.',
        'Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.167 Mobile Safari/537.36 OPR/77.4.4095.7489',
        'Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 10; moto e(6i) Build/QOH30.280-26) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.3',
        'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.167 Mobile Safari/537.36 OPR/77.4.4095.7489',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 EdgA/116.0.1938.75',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/117.0.5938.117 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/118.0 Firefox/118.0',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-A325F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.0) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SCG02) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-A715F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/118.0.5993.69 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/117.0.5938.117 Mobile/15E148 Safari/604.1'
    ]
    
    WINDOW_SIZES = [
        'window-size=3440x1440', 'window-size=3440x1363', 'window-size=3860x1670', 'window-size=1940x1090', 'window-size=1600x900', 'window-size=3020x1340', 'window-size=3620x1800', 'window-size=2900x1460', 'window-size=1380x1260', 'window-size=2310x1200', 'disable-gpu'
    ]

    LANG = [
        'lang=ko_KR', 'lang=en_US', 'lang=ko_KR', 'lang=ja_JP', 'lang=ko_KR', 'lang=zh-CN', 'lang=ko_KR'
    ]

    def __init__(self):
        headlessoptions = webdriver.ChromeOptions()
        headlessoptions.add_argument('headless')
        headlessoptions.add_argument(random.choice(Recru_It_Spider.LANG))
        headlessoptions.add_argument(random.choice(Recru_It_Spider.WINDOW_SIZES))
        headlessoptions.add_argument(f"User-Agent: {random.choice(Recru_It_Spider.USER_AGENTS)}")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=headlessoptions)
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(random.randint(2, 7)) # time.sleep(2)

        # ildao_items 가져오기
        ildao_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer")

        for i in range(random.randint(78, 84)):
            try:
                print(f"목록가져오기{i} : {ildao_items[-1].location_once_scrolled_into_view}")
            except Exception as e:
                print(f"\n\n - - - - - - - - 목록가져오기 예외처리 됨 !! - - - - - - - - \n\n{e}\n\n")
                time.sleep(random.randint(3, 5))   # time.sleep(2.2)
            else:
                time.sleep(random.randint(3, 5))    # time.sleep(2.2)
                ildao_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer")

        first_no_simple = 0
        simple_text_items = list(); site_text_items = list(); pay_text_items = list()
        simple_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer div.scrap_wrap.ft12.col_ora01")
        site_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer div.sub_info.foot div.ft12")
        pay_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer div.sub_info.foot > div > div")
        
        num_of_item = 0
        for simple_item, site_item, pay_item in zip(simple_items, site_items, pay_items):
            simple_text_items.append(simple_item.text.split('\n')[0])
            site_text_items.append(re.sub( 'location_on', '', re.sub('\n', '', site_item.text)))
            # site_text_items.append(site_item.text.split('\n')[1])     # 지역이 표시되지 않은 경우가 한번 있었는데 오류 남 ⬆️ 위 코드로 수정
            pay_text_items.append(pay_item.text)
            # simple_temp = simple_item.text.split('\n')[0]; site_temp = site_item.text.split('\n')[1]
            # print(f"\n{num_of_item} : {simple_temp}\t/\t{site_temp}\t/\t{pay_item.text}\t\n")
            num_of_item += 1

        # 첫번째 '간편지원'이 아닌 값을 'first_no_simple'에 저장
        for index, simple_text_item in enumerate(simple_text_items):    # '간편지원' 이 아닌 첫번재 값 구함
            if first_no_simple == 0 and simple_text_item.find('D-') == -1 and simple_text_item.find('간편지원') == -1 and simple_text_item.find('상시') == -1:
                first_no_simple = index

        print(f"\nfirst_no_simple : [{first_no_simple}]\n") # 간편지원 아닌 index 출력

        pattern_10_16 = re.compile('1[0-6]')
        pattern_14_16 = re.compile('1[4-6]')
        pattern_15_16 = re.compile('1[5-6]')

        pattern_16_19 = re.compile('1[6-9]')
        pattern_20_29 = re.compile('2[0-9]')

        # job_item = Recru_It_Item()
        # job_item['title'] = '';job_item['site'] = '';job_item['type'] = '';job_item['pay'] = ''
        # job_item['etc1'] = '';job_item['etc2'] = '';job_item['etc3'] = ''
        # job_item['numpeople'] = '0 명';job_item['phone'] = '';job_item['detail'] = ''
        # job_item['imageURL'] = '';job_item['time'] = '';job_item['sponsored'] = ''
        # yield job_item

        # job_item = Recru_It_Item()
        # job_item['title'] = '기계설비 기공 조공 모집합니다';job_item['site'] = '경기 평택시';job_item['type'] = '설비';job_item['pay'] = '일급 16만 ~ 20만원'
        # job_item['etc1'] = '숙식제공';job_item['etc2'] = '';job_item['etc3'] = ''
        # job_item['numpeople'] = '1 명';job_item['phone'] = '010-6430-7390';job_item['detail'] = '현재 개발중인 평택화양지구 현장입니다.\n현장인근에서 숙식가능하시고(2인1실) 조공,준기공,기공 상관없이 모집합니다\n급여는 협의가능하고 본인의 실력은 가감없이 있는그대로 말씀해주시면 감사하겠습니다\n경력이 짧아도 괜찮으니 성실하게 근속가능하신분 연락부탁드립니다'
        # job_item['imageURL'] = '';job_item['time'] = '';job_item['sponsored'] = ''
        # yield job_item

        # 서울 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(2, 5))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 6));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 서울 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 서울 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(2, 5))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 6));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (서울 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 서울 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 6))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (서울 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # job_item = Recru_It_Item()
        # job_item['title'] = 'HM시스템 (시스템동바리/비계 설치및해체 작업) 초보자가능';job_item['site'] = '부산';job_item['type'] = '비계/동바리';job_item['pay'] = '일급 16만원 이상'
        # job_item['etc1'] = '숙식제공';job_item['etc2'] = '4대보험';job_item['etc3'] = '장기근무'
        # job_item['numpeople'] = '상시';job_item['phone'] = '010-8739-1790';job_item['detail'] = '근무요일 : 월/화/수/목/금/토\n- 근무시간 : 07:00 ~ 16:30\n- 근무기간 : 1년이상\n- 급여 : 일급 : 160,000원 (초보 일당 16만원/기능공 협의)\n지원양식\n- 이름 :\n- 생년월일 :\n- 사는곳 :\n- 휴대폰번호 :\n- 경력 :\n- 안전교육이수증(사진) :\n\n문자로 보내주시면 검토후 전화드리도록하겠습니다'
        # job_item['imageURL'] = '';job_item['time'] = '';job_item['sponsored'] = ''
        # yield job_item
        
        # 부산 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 17))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('부산') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 부산 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 부산 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 17))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('부산') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (부산 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 부산 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('부산') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (부산 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # 경기 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 23))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경기') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 경기 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 경기 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 23))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경기') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (경기 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 경기 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 5))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경기') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (경기 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 인천 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 5))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('인천') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 인천 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 인천 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 5))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('인천') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (인천 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 인천 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 5))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('인천') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (인천 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 충남 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충남') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 충남 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 충남 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충남') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (충남 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 충남 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충남') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (충남 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 충북 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충북') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 충북 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 충북 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충북') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (충북 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 충북 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충북') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (충북 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 대전 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대전') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 대전 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 대전 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대전') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (대전 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 대전 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대전') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (대전 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 세종 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('세종') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 세종 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 세종 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('세종') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (세종 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 세종 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('세종') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (세종 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 전남 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 17))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전남') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 전남 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 전남 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 17))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전남') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (전남 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 전남 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전남') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (전남 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 광주 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('광주') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 광주 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 광주 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('광주') >= 0 and site_text_items[index].find('경기') == -1 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (광주 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 광주 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('광주') >= 0 and site_text_items[index].find('경기') == -1 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (광주 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 전북 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전북') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 전북 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 전북 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전북') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (전북 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 전북 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전북') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (전북 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 경남 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 15))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경남') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 경남 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 경남 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 17))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경남') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (경남 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 경남 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경남') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (경남 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        

        # 2025/02/23 등록 2025/03/12일 해지 ⬅️ 열흘정도 후 삭제 하자
        # job_item = Recru_It_Item()
        # job_item['title'] = '울산 S-Oil 전기 조공 구함';job_item['site'] = '울산 울주군';job_item['type'] = '전기';job_item['pay'] = '일급 15만원'
        # job_item['etc1'] = '4대보험';job_item['etc2'] = '출퇴근가능';job_item['etc3'] = ''
        # job_item['numpeople'] = '0 명';job_item['phone'] = '010-9299-9087';job_item['detail'] = '울산 S-Oil현장 전기 조공구합니다\n문자 주시면 전화드리겠습니다'
        # job_item['imageURL'] = '';job_item['time'] = '';job_item['sponsored'] = ''
        # yield job_item

        # 울산 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('울산') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 울산 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 울산 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('울산') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (울산 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 울산 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('울산') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (울산 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 경북 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 17))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경북') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 경북 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 경북 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 17))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경북') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (경북 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 경북 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경북') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (경북 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 대구 전체 (부산 해운대구X)
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대구') >= 0 and site_text_items[index].find('부산') == -1:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 대구 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 대구 16만 ~ 29만원 (부산 해운대구X)
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대구') >= 0 and site_text_items[index].find('부산') == -1 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (대구 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 대구 16만 ~ 29만원 이외 & 협의 (부산 해운대구X)
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대구') >= 0 and site_text_items[index].find('부산') == -1 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 3));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (대구 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 강원 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 17))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('강원') >= 0:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 5));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 강원 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 강원 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 17))   # time.sleep(2)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('강원') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 5));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (강원 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 강원 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 11))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('강원') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (강원 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass
        
        # 그외지역 전체
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') == -1 and site_text_items[index].find('부산') == -1 and site_text_items[index].find('경기') == -1 and site_text_items[index].find('인천') == -1 and site_text_items[index].find('충남') == -1 and site_text_items[index].find('충북') == -1 and site_text_items[index].find('대전') == -1 and site_text_items[index].find('세종') == -1 and site_text_items[index].find('전남') == -1 and site_text_items[index].find('광주') == -1 and site_text_items[index].find('전북') == -1 and site_text_items[index].find('경남') == -1 and site_text_items[index].find('울산') == -1 and site_text_items[index].find('경북') == -1 and site_text_items[index].find('대구') == -1 and site_text_items[index].find('강원') == -1:
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 5));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! ( 그외 ) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # # 그외지역 16만 ~ 29만원
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') == -1 and site_text_items[index].find('부산') == -1 and site_text_items[index].find('경기') == -1 and site_text_items[index].find('인천') == -1 and site_text_items[index].find('충남') == -1 and site_text_items[index].find('충북') == -1 and site_text_items[index].find('대전') == -1 and site_text_items[index].find('세종') == -1 and site_text_items[index].find('전남') == -1 and site_text_items[index].find('광주') == -1 and site_text_items[index].find('전북') == -1 and site_text_items[index].find('경남') == -1 and site_text_items[index].find('울산') == -1 and site_text_items[index].find('경북') == -1 and site_text_items[index].find('대구') == -1 and site_text_items[index].find('강원') == -1 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 5));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (그외 ⬆️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # # 그외지역 16만 ~ 29만원 이외 & 협의
        # print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        # time.sleep(random.randint(3, 7))   # time.sleep(3)
        # for index, job_item in enumerate(ildao_items):
        #     if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') == -1 and site_text_items[index].find('부산') == -1 and site_text_items[index].find('경기') == -1 and site_text_items[index].find('인천') == -1 and site_text_items[index].find('충남') == -1 and site_text_items[index].find('충북') == -1 and site_text_items[index].find('대전') == -1 and site_text_items[index].find('세종') == -1 and site_text_items[index].find('전남') == -1 and site_text_items[index].find('광주') == -1 and site_text_items[index].find('전북') == -1 and site_text_items[index].find('경남') == -1 and site_text_items[index].find('울산') == -1 and site_text_items[index].find('경북') == -1 and site_text_items[index].find('대구') == -1 and site_text_items[index].find('강원') == -1 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
        #         try:
        #             job_item.location_once_scrolled_into_view
        #             time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
        #             title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
        #             job_item = Recru_It_Item()
        #             job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
        #             job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
        #             job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
        #             job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
        #             yield job_item
        #         except Exception as e:
        #             print(f"\n\n - - - - - - - - 예외처리 됨 !! (그외 ⬇️) - - - - - - - - \n\n{e}\n\n")
        #         else:
        #             pass

        # 2025/04/07 등록 2025/04/16일 해지 ⬅️ 일주일정도 후 삭제 하자
        # job_item = Recru_It_Item()
        # job_item['title'] = '[구직] 20대 동바리 포설 전기 곰방 가능';job_item['site'] = '전국';job_item['type'] = '동바리 포설 전기 곰방 등';job_item['pay'] = '협의 후 결정'
        # job_item['etc1'] = '';job_item['etc2'] = '';job_item['etc3'] = ''
        # job_item['numpeople'] = '3 명';job_item['phone'] = '010-2556-1441';job_item['detail'] = '단기로 두달 하고 빠지겠습니다\n하지만 일주일 하고 도망가는 20~30대보다는 일 잘하고 확실하다고 생각합니다\n동바리 포설 전기 개장 곰방 다 해봤습니다\n일 꾸준히 있고 연장야간 풀 가능합니다\n써주십쇼'
        # job_item['imageURL'] = '';job_item['time'] = '';job_item['sponsored'] = ''
        # yield job_item


        time.sleep(random.randint(3, 30))
        print(f"\n\n\n총 아이템 수 : [{num_of_item}]\n")
        print(f"\nfirst_no_simple : [{first_no_simple}]\n") # 간편지원 아닌 index 출력
        print(f"\n # # # # # # # # # # # # # # # # # # # # # #   정상종료   # # # # # # # # # # # # # # # # # # # # # #\n\n")
        self.driver.quit()
        pass

    # 본문 가져오기
    def get_job_detail(self):
        pattern_da_dot = re.compile('다\.')
        pattern_dot_num = re.compile('\.[0-9]')
        title_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.ft5.NotoSansM")
        title_pre1 = re.sub('[^a-zA-Z0-9가-힣一-龥_\s\(\)\[\]\-\~\/\,\.\ㆍ\&\%]', ' ', title_sel.text)
        title_pre2 = title_pre1.strip(' _-~/,.ㆍ&%').lstrip(')]').rstrip('([').upper()
        pattern_da_dot_num = pattern_da_dot.findall(title_pre2) + pattern_dot_num.findall(title_pre2)
        if len(pattern_da_dot_num) == 0:    # '다.' , '.숫자' 가 없을때만 '.' 삭제
            title_pre2 = re.sub('\.', ' ', title_pre2)
        title = re.sub('\s{2,9}', ' ', title_pre2)

        site_sel = self.driver.find_element(By.CSS_SELECTOR, "div.time.ft11.col_gra04.NotoSansL")
        site_pre = re.sub('[a-z]+_[a-z]+\s', '', site_sel.text) # "location_on " 없애기
        site = re.sub('세종 세종', '세종시', site_pre)

        type_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.ft11 div.ft10")
        type_pre = re.sub('조공/잡부', '조공/보조', type_sel.text)
        type = re.sub('시스템/비계', '비계/동바리', type_pre)

        pay_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.col_blu02.ft10 > div")
        pay_pre1 = re.sub('\n', ' ', re.sub('0 원', '0원', pay_sel.text))
        pay_pre2 = re.sub('0,000', '만', pay_pre1)
        if pay_pre2.find(',000') == -1:
            pay = re.sub(',', '', pay_pre2)
        else:
            pay = re.sub('', '', pay_pre2)

        etcs_sel = self.driver.find_elements(By.CSS_SELECTOR, "#detail_info div.ft11.col_blu02")

        etc1 = '';etc2 = '';etc3 = ''
        etc_set = set()
        for etc in etcs_sel:
            etc_set.add(etc.text.strip(','))

        if '숙식제공' in etc_set:
            etc1 = '숙식제공'
            if '4대보험' in etc_set:
                etc2 = '4대보험'
                if '출퇴근가능' in etc_set:
                    etc3 = '출퇴근가능'
                elif '장기근무' in etc_set:
                    etc3 = '장기근무'
            elif '출퇴근가능' in etc_set:
                etc2 = '출퇴근가능'
                if '장기근무' in etc_set:
                    etc3 = '장기근무'
            elif '장기근무' in etc_set:
                etc2 = '장기근무'
        elif '4대보험' in etc_set:
            etc1 = '4대보험'
            if '출퇴근가능' in etc_set:
                etc2 = '출퇴근가능'
                if '장기근무' in etc_set:
                        etc3 = '장기근무'
            elif '장기근무' in etc_set:
                etc2 = '장기근무'
        elif '출퇴근가능' in etc_set:
            etc1 = '출퇴근가능'
            if '장기근무' in etc_set:
                etc2 = '장기근무'
        elif '' in etc_set:
            etc1 = '장기근무'

        numpeople_int = 0;numpeople_pre = 0
        num_pattern = re.compile('[0-9]')
        numpeople_sel_list = self.driver.find_elements(By.CSS_SELECTOR, "#detail_info div.ft11 div.ft10[style='display: flex;']")
        for numpeople_sel in numpeople_sel_list:
            if len(num_pattern.findall(numpeople_sel.text)) > 0:    # 숫자가 들어있는 문자열만 가져온다
                numpeople_int = re.sub('[^0-9]', '', numpeople_sel.text)    # 숫자를 제외한 문자 삭제
                #print(f"numpeople_int : {numpeople_int}")
                numpeople_pre += int(numpeople_int)                 # 초보+조공+준공+기공 = 총인원
        numpeople = f"{numpeople_pre}명"

        phone_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.ft11 div.ft10.RobotoM")
        phone = re.sub('', '', phone_sel.text)

        detail_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info p.ft10.lin_h2")
        detail_pre1 = re.sub('\n\n\n\n+', '\n\n\n', detail_sel.text)
        # detail_pre2 = re.sub(' *\*\) *', '\n• ', re.sub(' *\*\] *', '\n• ', detail_pre1)) # 특정 소개소 detail 작성 양식 때문에 바꿔줌 '*]타일용접' (나중에 없애도 됨)
        # detail_pre3 = re.sub(' *\#\)', '◎', re.sub(' *\#\]', '◎', detail_pre2))
        # detail_pre4 = re.sub(' *\@\)', '◎', re.sub(' *\@\]', '◎', detail_pre3))
        # detail_pre5 = re.sub('잇', '있',re.sub('업슴', '없음',re.sub('잇슴', '있음', detail_pre4)))
        # detail_pre6 = re.sub('\n\n\n+', '\n\n',re.sub('//', '/',re.sub('\n {1,9}', '/', detail_pre5)))
        # if detail_pre6.find('• ') != -1:
        #     detail = re.sub('', '', detail_pre6)
        # else:
        #     detail = re.sub('', '', detail_pre1)
        detail = re.sub('잇', '있',re.sub('업슴', '없음',re.sub('잇슴', '있음', detail_pre1)))
        # detail = re.sub('', '', detail_pre1)
    
        imageURL_sel = '';imageURL = ''
        try:
            imageURL_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info > div > div > div > div > img")
        except Exception as e:
            imageURL = ''
        else:
            imageURL = imageURL_sel.get_attribute('src')


        # Change title
        title = re.sub('old', 'new', title)
        
        title = re.sub('가산역디지털단지데이터센터-전기포설전공5명19만부터-숙식4대유-28~45세연장주2회-동반불가', '가산역디지털단지 데이터센터 전기포설전공 19만부터 28~45세 연장주2회', title)
        title = re.sub('사당역6시30분출발금속준기공1명19만-출4대무-30~55세', '금속 준기공1명 출퇴근 4대무 30~55세 (사당역6시30분출발)', title)
        title = re.sub('\(주급/출퇴\)개봉동타이어뱅크외장판넬작업자모집합니다', '개봉동 타이어뱅크 외장판넬 작업자 모집합니다', title)
        title = re.sub('시스템 동바리 /비계 직원채용 신규자16만 부터', '시스템 동바리/비계 직원채용 신규자16만 부터', title)
        title = re.sub('강남일원동삼성의료원', '강남 일원동 삼성의료원', title)
        title = re.sub('상성동 소방전기', '삼성동 소방전기', title)
        title = re.sub('삼성동준기공', '삼성동 준기공', title)
        title = re.sub('미국미시건주', '미국 미시건주', title)
        title = re.sub('010 5792 6048', '', title)
        title = re.sub('old', 'new', title)
        title = re.sub('old', 'new', title)
        title = re.sub('old', 'new', title)
        title = re.sub('old', 'new', title)
        
        title = re.sub('old', 'new', title)

        title = re.sub('현댕실스테이트', '현대힐스테이트', title)
        title = re.sub('금속인데리어', '금속인테리어', title)
        title = re.sub('금속인톄리어', '금속인테리어', title)
        title = re.sub('인테링어', '인테리어', title)
        title = re.sub('모심니다', '모십니다', title)
        title = re.sub('끈기잇고', '끈기있고', title)
        title = re.sub('평택고덛', '평택고덕', title)
        title = re.sub('쥰전공', '준전공', title)
        title = re.sub('펴자재', '폐자재', title)
        title = re.sub('페자재', '폐자재', title)
        title = re.sub('폐기뮬', '폐기물', title)
        title = re.sub('은폄구', '은평구', title)
        title = re.sub('구이동', '구의동', title)
        title = re.sub('실네', '실내', title)
        title = re.sub('old', 'new', title)
        title = re.sub('old', 'new', title)

        title = re.sub('old', 'new', title)


        # Change detail
        detail = re.sub('old', 'new', detail)
        
        #   '.', ',', '/' 은 '\'를 앞에 붙여주지 않아도 인식하고 처리됨
        #   특수문자앞에는 꼭 '\*' 이런식으로 '\'붙여야 한다 오류나거나 제대로 인식하지 못한다
        #   찾는 문자열에서만 ')' 앞에 \ 붙여 '\)' 해주고 고칠 문자열에서는 그냥 ')' 해준다 '\)' 해주면 '\\)' 이런식으로 출력 됨
        #   괄호 '(' ')' 입력시에는 '\(', '\)' 꼭 이렇게 해줘야 한다. 안그럼 unbalanced parenthesis 에러 or 괄호 인식 못해 제대로 못찾음
        detail = re.sub(' F4\)\n\n문의', ' F4)', detail)
        detail = re.sub('나이 : \*\*\*부터 42까지 \n팀은 젊은층으로 이루어져있으며 평균 \*\*\* 초중반입니다.', '나이 : 팀은 젋은층으로 이루어져있으며 평균 30대 초중반입니다.', detail)
        detail = re.sub('\n\#조공 \#기공 \#고압 \#준전공 \#전기 \#트레이 \#강제 \#포설  \#전선관 \#풀링\#소방전기 \#가설 \#소방전선관 \#경기도 \#여주 \#포스코', '', detail)
        detail = re.sub('함께 손맞쳐 재밌게일하실분 어렵게생각마시고전화주세요', '함께 손맞춰 재밌게일하실분\n어렵게생각마시고 전화주세요', detail)
        detail = re.sub('근무시간 0700 \~ 1600', '근무시간 07:00 ~ 16:00', detail)
        detail = re.sub('반장님들을기다립니나\~', '반장님들을 기다립니다', detail)
        detail = re.sub('연락드릴겠읍니다', '연락드리겠습니다', detail)
        detail = re.sub('\n\n담당자 : 안용식부장', '', detail)
        detail = re.sub('도면 보시보', '도면 보시고', detail)
        detail = re.sub('근면성실이', '근면성실히', detail)
        detail = re.sub('보내주싱션', '보내주시면', detail)
        detail = re.sub('\n전화번호 \n', '\n', detail)
        detail = re.sub('220000원', '22만원', detail)
        detail = re.sub('\n 번으로 ', '\n', detail)
        
        detail = re.sub('old', 'new', detail)
        detail = re.sub('old', 'new', detail)
        detail = re.sub('old', 'new', detail)

        #   ‼️ 본문맨위 ‼️ \n #소개수수료없음 ⬇️
        detail = re.sub(' *#소개수수료없음\n', '소개수수료 없음', detail)        
        detail = re.sub(' *‼️ *', '', detail)  # ‼️ 없애기 (" *" : 앞뒤로 빈칸이 없거나 한번이상 반복) - 앞뒤 빈칸있으면 같이 지운다
        detail = re.sub(' *♦️ *', '', detail)  # ♦️ 없애기 (" *" : 앞뒤로 빈칸이 없거나 한번이상 반복) - 앞뒤 빈칸있으면 같이 지운다
        detail = re.sub('❤', '', detail)  # ❤ 없애기

        detail = re.sub('old', 'new', detail)
        detail = re.sub('old', 'new', detail)
        detail = re.sub('old', 'new', detail)

        detail = re.sub('old', 'new', detail)

        detail = re.sub('\n\n담당자 연락처 \:\n담당자 \: \n부재시 \:', '', detail)
        detail = re.sub('\n연락처 :\n담당자 : 김규동차장', '', detail)
        detail = re.sub('연락처 : 한울 시스템 김팀장 \n', '', detail)
        detail = re.sub('■ 연락처 : (팀장)\n', 'new', detail)
        detail = re.sub('\n연락처 \: \#건설현장', '', detail)
        detail = re.sub('연락처 : (작성요망)\n', '', detail)
        detail = re.sub('연락처 \: 홍팀장 \n', '', detail)
        detail = re.sub('■ 지원 / 연락처\n', '', detail)
        detail = re.sub('■연락처 \: \n\n', '', detail)
        detail = re.sub('✅ 연락처 \n\n', '', detail)
        detail = re.sub('연락처 \(\)\n', '', detail)
        detail = re.sub('연락처 \:  \n', '', detail)
        detail = re.sub('담당자 \: \n', '', detail)
        detail = re.sub('연락처 \: \n', '', detail)
        detail = re.sub('연락처\:  \n', '', detail)
        detail = re.sub('연락처 \:\n', '', detail)
        detail = re.sub('연락처\: \n', '', detail)
        detail = re.sub('연락처\:\n', '', detail)
        detail = re.sub('old', 'new', detail)
        detail = re.sub('old', 'new', detail)

        detail = re.sub('old', 'new', detail)

        detail = re.sub('연라바랍니다', '연락바랍니다', detail)
        detail = re.sub(' 그합니다', ' 구합니다', detail)
        detail = re.sub('인테링어', '인테리어', detail)
        detail = re.sub('모심니다', '모십니다', detail)
        detail = re.sub('입니드', '입니다', detail)
        detail = re.sub('읍니다', '습니다', detail)
        detail = re.sub('쥰전공', '준전공', detail)
        detail = re.sub('펴자재', '폐자재', detail)
        detail = re.sub('페자재', '폐자재', detail)
        detail = re.sub('폐기뮬', '폐기물', detail)
        detail = re.sub('은폄구', '은평구', detail)
        detail = re.sub('구이동', '구의동', detail)
        detail = re.sub('0뷴', '0분', detail)
        detail = re.sub('old', 'new', detail)
        detail = re.sub('old', 'new', detail)

        detail = re.sub('old', 'new', detail)

# 2025/04/07 등록  "20대 구직" ⬅️ 일주일정도 후 삭제 (4월13일 이후)

        # Change pay
        pay = re.sub('old', 'new', pay)

        pay = re.sub('145,000 ~ 145,000원', '145,000원', pay)
        pay = re.sub('142,000 ~ 142,000원', '142,000원', pay)
        pay = re.sub('400만 ~ 50만원', '400만 ~ 500만원', pay)
        pay = re.sub(' ~ 1 원', '원 이상', pay)
        pay = re.sub(' ~ 2 원', '원 이상', pay)
        pay = re.sub(' ~ 00원', '원', pay)
        pay = re.sub('old', 'new', pay)
        pay = re.sub('old', 'new', pay)

        pay = re.sub('old', 'new', pay)


        return title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL