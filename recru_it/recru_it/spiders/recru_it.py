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
        'window-size=1940x1090', 'window-size=1600x900', 'window-size=3020x1340', 'window-size=3620x1800', 'window-size=2900x1460', 'window-size=1380x1260', 'window-size=2310x1200', 'disable-gpu'
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
        time.sleep(random.randint(7, 15)) # time.sleep(2)

        # ildao_items 가져오기
        ildao_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer")

        for i in range(79):
            try:
                print(f"목록가져오기{i} : {ildao_items[-1].location_once_scrolled_into_view}")
            except Exception as e:
                print(f"\n\n - - - - - - - - 목록가져오기 예외처리 됨 !! - - - - - - - - \n\n{e}\n\n")
                time.sleep(random.randint(3, 7))   # time.sleep(2.2)
            else:
                time.sleep(random.randint(3, 7))    # time.sleep(2.2)
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
        # job_item['title'] = 'title';job_item['site'] = 'site';job_item['type'] = 'type';job_item['pay'] = 'pay'
        # job_item['etc1'] = 'etc1';job_item['etc2'] = 'etc2';job_item['etc3'] = 'etc3'
        # job_item['numpeople'] = 'numpeople';job_item['phone'] = 'phone';job_item['detail'] = 'detail'
        # job_item['imageURL'] = 'imageURL';job_item['time'] = '';job_item['sponsored'] = ''
        # yield job_item

        job_item = Recru_It_Item()
        job_item['title'] = '화성 삼성전자 안전관리사 모집';job_item['site'] = '경기 화성시';job_item['type'] = '안전';job_item['pay'] = '일급 15만원'
        job_item['etc1'] = '4대보험';job_item['etc2'] = '';job_item['etc3'] = ''
        job_item['numpeople'] = '0 명';job_item['phone'] = '010-4641-0618';job_item['detail'] = '화성 삼성전자에서 안전 이모님 구합니다\n연락주세요 일 끊길일 없이 지속근무 가능합니다\n55세이하'
        job_item['imageURL'] = 'imageURL';job_item['time'] = '';job_item['sponsored'] = ''
        yield job_item

        job_item = Recru_It_Item()
        job_item['title'] = '평택 삼성전자 조공 모집';job_item['site'] = '경기 평택시';job_item['type'] = '배관';job_item['pay'] = '일급 15만원'
        job_item['etc1'] = '4대보험';job_item['etc2'] = '';job_item['etc3'] = ''
        job_item['numpeople'] = '0 명';job_item['phone'] = '010-4641-0618';job_item['detail'] = '배관 조공 모집합니다.        \n연락주세요\n               '
        job_item['imageURL'] = 'imageURL';job_item['time'] = '';job_item['sponsored'] = ''
        yield job_item
        
        # 서울 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 13));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (서울 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 서울 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (서울 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 부산 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('부산') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 11));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (부산 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 부산 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('부산') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (부산 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 경기 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경기') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 8));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (경기 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 경기 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경기') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (경기 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 인천 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('인천') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (인천 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 인천 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('인천') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (인천 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 충남 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충남') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 8));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (충남 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 충남 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충남') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (충남 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 충북 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충북') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (충북 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 충북 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('충북') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (충북 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 대전 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대전') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (대전 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 대전 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대전') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (대전 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 세종 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('세종') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (세종 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 세종 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('세종') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (세종 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 전남 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전남') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 11));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (전남 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 전남 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전남') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 6));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (전남 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 광주 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('광주') >= 0 and site_text_items[index].find('경기') == -1 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (광주 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 광주 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('광주') >= 0 and site_text_items[index].find('경기') == -1 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (광주 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 전북 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전북') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (전북 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 전북 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('전북') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (전북 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 경남 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경남') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (경남 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 경남 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경남') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (경남 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 울산 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('울산') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (울산 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 울산 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('울산') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (울산 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 경북 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경북') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (경북 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 경북 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('경북') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (경북 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 대구 16만 ~ 29만원 (부산 해운대구X)
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대구') >= 0 and site_text_items[index].find('부산') == -1 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 12));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (대구 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 대구 16만 ~ 29만원 이외 & 협의 (부산 해운대구X)
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('대구') >= 0 and site_text_items[index].find('부산') == -1 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 7));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (대구 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 강원 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 70))   # time.sleep(2)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('강원') >= 0 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 15));job_item.click();time.sleep(.5)  # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (강원 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 강원 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 16))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('강원') >= 0 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 8));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (강원 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass
        
        # 그외지역 16만 ~ 29만원
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') == -1 and site_text_items[index].find('부산') == -1 and site_text_items[index].find('경기') == -1 and site_text_items[index].find('인천') == -1 and site_text_items[index].find('충남') == -1 and site_text_items[index].find('충북') == -1 and site_text_items[index].find('대전') == -1 and site_text_items[index].find('세종') == -1 and site_text_items[index].find('전남') == -1 and site_text_items[index].find('광주') == -1 and site_text_items[index].find('전북') == -1 and site_text_items[index].find('경남') == -1 and site_text_items[index].find('울산') == -1 and site_text_items[index].find('경북') == -1 and site_text_items[index].find('대구') == -1 and site_text_items[index].find('강원') == -1 and pay_text_items[index].find('협의') == -1 and (len(pattern_16_19.findall(pay_text_items[index])) > 0 or len(pattern_20_29.findall(pay_text_items[index])) > 0):
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
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (그외 ⬆️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        # 그외지역 16만 ~ 29만원 이외 & 협의
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(3, 7))   # time.sleep(3)
        for index, job_item in enumerate(ildao_items):
            if index >= first_no_simple and simple_text_items[index].find('간편지원') == -1 and site_text_items[index].find('서울') == -1 and site_text_items[index].find('부산') == -1 and site_text_items[index].find('경기') == -1 and site_text_items[index].find('인천') == -1 and site_text_items[index].find('충남') == -1 and site_text_items[index].find('충북') == -1 and site_text_items[index].find('대전') == -1 and site_text_items[index].find('세종') == -1 and site_text_items[index].find('전남') == -1 and site_text_items[index].find('광주') == -1 and site_text_items[index].find('전북') == -1 and site_text_items[index].find('경남') == -1 and site_text_items[index].find('울산') == -1 and site_text_items[index].find('경북') == -1 and site_text_items[index].find('대구') == -1 and site_text_items[index].find('강원') == -1 and (pay_text_items[index].find('협의') >= 0 or (len(pattern_16_19.findall(pay_text_items[index])) == 0 and len(pattern_20_29.findall(pay_text_items[index])) == 0)):
                try:
                    job_item.location_once_scrolled_into_view
                    time.sleep(random.randint(1, 4));job_item.click();time.sleep(.5)   # time.sleep(1);job_item.click();time.sleep(.5)
                    title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()
                    job_item = Recru_It_Item()
                    job_item['title'] = title;job_item['site'] = site;job_item['type'] = type;job_item['pay'] = pay
                    job_item['etc1'] = etc1;job_item['etc2'] = etc2;job_item['etc3'] = etc3 #print(etc_set)
                    job_item['numpeople'] = numpeople;job_item['phone'] = phone;job_item['detail'] = detail
                    job_item['imageURL'] = imageURL;job_item['time'] = '';job_item['sponsored'] = ''
                    yield job_item
                except Exception as e:
                    print(f"\n\n - - - - - - - - 예외처리 됨 !! (그외 ⬇️) - - - - - - - - \n\n{e}\n\n")
                else:
                    pass

        time.sleep(random.randint(7, 200))  # time.sleep(random.randint(3, 30))
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
        detail_pre2 = re.sub(' *\*\) *', '\n• ', re.sub(' *\*\] *', '\n• ', detail_pre1)) # 특정 소개소 detail 작성 양식 때문에 바꿔줌 '*]타일용접' (나중에 없애도 됨)
        detail_pre3 = re.sub(' *\#\)', '◎', re.sub(' *\#\]', '◎', detail_pre2))
        detail_pre4 = re.sub(' *\@\)', '◎', re.sub(' *\@\]', '◎', detail_pre3))
        detail_pre5 = re.sub('잇', '있',re.sub('업슴', '없음',re.sub('잇슴', '있음', detail_pre4)))
        detail_pre6 = re.sub('\n\n\n+', '\n\n',re.sub('//', '/',re.sub('\n {1,9}', '/', detail_pre5)))
        if detail_pre6.find('• ') != -1:
            detail = re.sub('', '', detail_pre6)
        else:
            detail = re.sub('', '', detail_pre1)
    
        imageURL_sel = '';imageURL = ''
        try:
            imageURL_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info > div > div > div > div > img")
        except Exception as e:
            imageURL = ''
        else:
            imageURL = imageURL_sel.get_attribute('src')

        # tem title
        title = re.sub('팀윤구합니다', '팀원 구합니다', title)
        title = re.sub('인제모집', '인재모집', title)
        title = re.sub('구인중ㆍ숙식ㆍ출퇴근', '구인중 숙식/출퇴근', title)
        title = re.sub('함게일할직원분을', '함께일할 직원분', title)
        title = re.sub('건설현장포설하실분모집합니다(물량팀이라지방이동근무도가능하신분지원바랍니다)', '건설현장 포설하실분 모집 (물량팀 지역이동이동근무 가능하신분)', title)
        title = re.sub('title_or', 'title_ne', title)
        

        # tem tail
        detail = re.sub(' ㆍ일꾸준 ㆍ월급정확ㆍ4대보험도 가능ㆍ현장', '\n일꾸준, 월급정확, 4대보험도 가능\n현장', detail)
        detail = re.sub('인제모집중', '인재모집중', detail)
        detail = re.sub('\n 전기, 통신을 주로 하며 장비사용으로 크게 힘든 부분은 없습니다.\n\n 일당 16만원 3.3% 공제 후 월급으로 지급.\n\n 1.타지역 출장 가능하신분\n \n 2.숙소 생활 가능하신분\n\n 3.주말 근무 가능하신분(일정에 따라 근무)\n\n 4. 6개월 이상 근무 가능하신분\n\n경력자인 경우 협의 후 일당 조정 가능합니다.\n', '전기, 통신을 주로 하며 장비사용으로 크게 힘든 부분은 없습니다.\n일당 16만원 3.3% 공제 후 월급으로 지급.\n\n 1.타지역 출장 가능하신분\n 2.숙소 생활 가능하신분\n 3.주말 근무 가능하신분(일정에 따라 근무)\n 4. 6개월 이상 근무 가능하신분\n\n경력자인 경우 협의 후 일당 조정 가능합니다.', detail)
        detail = re.sub('성실하게.즐겁게.오랫동안 함께 일할수 있는분이면 좋겠습니다 저또한 좋은조건에서 즐겁게 일할 수 있도록 힘쓰겠습니다 ', '\n성실하게 즐겁게 오랫동안 함께 일할수 있는분이면 좋겠습니다.\n저또한 좋은조건에서 즐겁게 일할 수 있도록 힘쓰겠습니다.\n', detail)
        detail = re.sub('detail_or', 'detail_ne', detail)

        # tem pay
        pay = re.sub('18만 ~ 00원', '18만원', pay)
        pay = re.sub('일급 15만 ~ 2 원', '일급 15만원 이상', pay)
        pay = re.sub('pay_or', 'pay_ne', pay)
        return title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL