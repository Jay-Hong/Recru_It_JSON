#~/Documents/Recru_It_JSON/recru_it/recru_it/spiders/recru_it.py

from datetime import date, timedelta
import random, re, scrapy, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from recru_it.items import Recru_It_Item
from recru_it.spiders.constants import LANG, USER_AGENTS, WINDOW_SIZES
from recru_it.settings import CRAWL_CONFIG, MANUAL_JOBS_BY_REGION

class Recru_It_Spider(scrapy.Spider):
    name = "recru_it";recru_it = "ecruit";dotdcom = "o.com/r";db = "lda"
    allowed_domains = ["i"+db+"o.com"]
    start_urls = ["https://i"+db+dotdcom+recru_it]

    one_day = timedelta(days=1)
    one_week = timedelta(weeks=1)
    today = date.today()
    yesterday = today - one_day
    theday_before_10weeks = today - (10 * one_week)

    def __init__(self):
        headlessoptions = webdriver.ChromeOptions()
        headlessoptions.add_argument('headless')
        headlessoptions.add_argument(random.choice(LANG))
        headlessoptions.add_argument(random.choice(WINDOW_SIZES))
        headlessoptions.add_argument(f"User-Agent: {random.choice(USER_AGENTS)}")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=headlessoptions)
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def _matches_region(self, site_text, keywords, exclude_keywords):
        """지역이 키워드와 매칭되는지 확인"""
        # 제외 키워드 체크 (예: 대구 검색 시 "부산 해운대구" 제외)
        for exclude in exclude_keywords:
            if site_text.find(exclude) >= 0:
                return False

        # 키워드가 비어있으면 (그외 지역) True
        if not keywords:
            return True

        # 키워드 매칭
        for keyword in keywords:
            if site_text.find(keyword) >= 0:
                return True

        return False

    def process_region(self, region_config, ildao_items, simple_text_items,
                       site_text_items, first_no_simple):
        """특정 지역의 아이템들을 크롤링하는 공통 함수"""
        region_name = region_config['name']
        keywords = region_config['keywords']
        exclude_keywords = region_config.get('exclude_keywords', [])
        item_limit = region_config.get('item_limit', None)
        sleep_before = region_config['sleep_before']
        sleep_between = region_config['sleep_between']

        # 1. 먼저 해당 지역의 수동 아이템 추가 (크롤링 결과 맨 앞에 위치)
        if region_name in MANUAL_JOBS_BY_REGION:
            for job_data in MANUAL_JOBS_BY_REGION[region_name]:
                job_item = Recru_It_Item()
                for key, value in job_data.items():
                    job_item[key] = value
                yield job_item

        # 2. 그 다음 크롤링 아이템 추가
        print(f"중단가기  : {ildao_items[first_no_simple].location_once_scrolled_into_view}")
        time.sleep(random.randint(*sleep_before))

        for index, job_item in enumerate(ildao_items):
            # 제한 조건 체크
            if item_limit and index >= item_limit:
                continue
            if index < first_no_simple:
                continue
            if simple_text_items[index].find('간편지원') != -1:
                continue

            # 지역 필터링
            if not self._matches_region(site_text_items[index], keywords, exclude_keywords):
                continue

            try:
                job_item.location_once_scrolled_into_view
                time.sleep(random.randint(*sleep_between))
                job_item.click()
                time.sleep(.5)

                title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL = self.get_job_detail()

                if True:
                    job_item = Recru_It_Item()
                    job_item['title'] = title
                    job_item['site'] = site
                    job_item['type'] = type
                    job_item['pay'] = pay
                    job_item['etc1'] = etc1
                    job_item['etc2'] = etc2
                    job_item['etc3'] = etc3
                    job_item['numpeople'] = numpeople
                    job_item['phone'] = phone
                    job_item['detail'] = detail
                    job_item['imageURL'] = imageURL
                    job_item['time'] = ''
                    job_item['sponsored'] = ''
                    yield job_item

            except Exception as e:
                print(f"\n\n - - - - - - - - 예외처리 됨 !! ( {region_name} ) - - - - - - - - \n\n{e}\n\n")

    def parse(self, response):
        # 설정 값 가져오기
        scroll_range = CRAWL_CONFIG['scroll_range']
        initial_sleep = CRAWL_CONFIG['initial_sleep']

        self.driver.get(response.url)
        time.sleep(random.randint(*initial_sleep))

        # ildao_items 가져오기
        ildao_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer")

        # 새벽시간에 조금씩만 가져오자 (가져오는양 봐가면 점점~ 줄여)
        # for i in range(random.randint(47, 59)):
        for i in range(random.randint(*scroll_range)):
            try:
                print(f"목록가져오기{i} : {ildao_items[-1].location_once_scrolled_into_view}")
            except Exception as e:
                print(f"\n\n - - - - - - - - 목록가져오기 예외처리 됨 !! - - - - - - - - \n\n{e}\n\n")
                time.sleep(random.randint(3, 6))   # time.sleep(2.2)
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

        # 지역별 크롤링
        for region_config in CRAWL_CONFIG['regions']:
            yield from self.process_region(
                region_config,
                ildao_items,
                simple_text_items,
                site_text_items,
                first_no_simple
            )

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
        detail = re.sub('잇', '있',re.sub('업슴', '없음',re.sub('잇슴', '있음', detail_pre1)))
    
        imageURL_sel = '';imageURL = ''
        try:
            imageURL_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info > div > div > div > div > img")
        except Exception as e:
            imageURL = ''
        else:
            imageURL = imageURL_sel.get_attribute('src')

        #  time_sel 에 들어오는 값 들 ⬇️ 2024/04/27현재 기준
        #  ⓵ "상시 모집"    👉 "02/17" (10주전) <- 오래된거 걸러지게
        #  ⓶ "38분 전"     👉 "04/27" (오늘)
        #  ⓷ "6시간 전"     👉 "04/27" (오늘)
        #  ⓸ "NEW"         👉 "04/26" (어제)
        #  ⓹ "등록 : 04-24" 👉 "04/24"  형태로 만들어준다
        #  ⓺ 혹시 모르는 그외  👉 "04/26" (어제) 예상치 못한 값이 들어와도 일단 어제로 세팅해 출력해준다 (웹 스타일 바뀔경우)
        # time_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.ft12.RobotoM > div")
        # time_pre = re.sub('', '', time_sel.text)

        # if time_pre.find('상시') >= 0:  # ⓵
        #     time_pre = str(self.theday_before_10weeks.month) + '/' + str(self.theday_before_10weeks.day)
        # elif time_pre.find('분 전') >= 0 or time_pre.find('시간 전') > 0:  # ⓶ ⓷
        #     time_pre = str(self.today.month) + '/' + str(self.today.day)
        # elif time_pre.find('NEW') >= 0:  # ⓸
        #     time_pre = str(self.yesterday.month) + '/' + str(self.yesterday.day)
        # elif time_pre.find('등록') >= 0:  # ⓹
        #     time_pre = re.sub('등록 : ', '', time_pre)
        #     time_pre = re.sub('-', '/', time_pre).lstrip('0')
        # else:  # ⓺  GitHub Action 에서 관련값 가져오지 못함으로 이부분만 실행됨 👉 일단 빈칸으로 놔두자
        #     time_pre = str(self.yesterday.month) + '/' + str(self.yesterday.day) # 임시로 실행되도록
        #     # time_pre = ''
        # time_ = re.sub('', '', time_pre)


        # Change title
        title = re.sub('old', 'new', title)
        
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
        detail = re.sub('\n\n연락 :', '\n', detail)
        detail = re.sub('old', 'new', detail)
        detail = re.sub('old', 'new', detail)

        detail = re.sub('old', 'new', detail)

        detail = re.sub('연라바랍니다', '연락바랍니다', detail)
        detail = re.sub(' 그합니다', ' 구합니다', detail)
        detail = re.sub('인테링어', '인테리어', detail)
        detail = re.sub('모심니다', '모십니다', detail)
        detail = re.sub('아님니다', '아닙니다', detail)
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


        return title, site, type, pay, etc1, etc2, etc3, numpeople, phone, detail, imageURL #, time_