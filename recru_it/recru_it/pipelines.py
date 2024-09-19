# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re

ob = '오'
dab = '다'
ilb = '일'
pattern_day10_13 = re.compile('일급 1[0-3]')
pattern_month10_13 = re.compile('월급 1[0-3]')
pattern_odail = re.compile(ilb+dab+ob)
pattern_day10_15 = re.compile('일급 1[0-5]')
pattern_month10_15 = re.compile('월급 1[0-5]')
pattern_system = re.compile('비계/동바리')
pattern_nego = re.compile('협의')
pattern_null = re.compile('null')

class Recru_It_Pipeline:
    def process_item(self, item, spider):
        if len(pattern_day10_13.findall(item['pay'])) > 0:  # '일급 10 ~ 13' 들어가면 다 뺌
            raise DropItem('\n\nDrop 일급 10 ~ 13 ! 🚯\n')
        elif len(pattern_month10_13.findall(item['pay'])) > 0:  # '월급 10 ~ 13' 들어가면 다 뺌
            raise DropItem('\n\nDrop 월급 10 ~ 13 ! 🚯\n')
        # elif item['title'].find('155555') != -1:    # str.find('문자열') 찾았으면 0 ~ 찾은 첫번째 인댁스 / 못찾았으면 -1 반환
        elif len(pattern_odail.findall(item['title'])) > 0: # 바로위 주석부분과 같은기능
            raise DropItem('\n\nDrop detail : 155555 🚯\n')
        elif len(pattern_odail.findall(item['detail'])) > 0:
            raise DropItem('\n\nDrop detail : 155555 🚯\n')
        elif len(item['detail']) < 32: # detail 32자 미만은 빼
            raise DropItem('\n\nDrop detail : 32자 미만 🚯\n')
        elif len(item['title']) < 6: # title 6자 미만은 빼
            raise DropItem('\n\nDrop title : 6자 미만 🚯\n')
        elif (len(pattern_day10_15.findall(item['pay'])) > 0 or len(pattern_month10_15.findall(item['pay'])) > 0) and len(pattern_system.findall(item['type'])) > 0 and item['site'].find('부산') == -1 and item['site'].find('서울') == -1:
            raise DropItem('\n\nDrop 비계/동바리 이면서 단가 15이하 (부산, 서울 제외) 🚯\n')
        elif len(pattern_nego.findall(item['pay'])) > 0 and len(pattern_system.findall(item['type'])) > 0 and item['site'].find('부산') == -1 and item['site'].find('서울') == -1:
            raise DropItem('\n\nDrop 비계/동바리 이면서 협의 (부산, 서울 제외) 🚯 \n')
        elif len(pattern_null.findall(item['site'])) > 0:   # site 에 null 이 들어가면 빼
            raise DropItem('\n\nDrop site : null 🚯\n')
        elif len(re.compile('title to drop1').findall(item['title'])) > 0: # tem
            raise DropItem('\n\nDrop detail : title to drop 🚯\n')
        elif len(re.compile('title to drop2').findall(item['title'])) > 0: # tem
            raise DropItem('\n\nDrop detail : title to drop 🚯\n')
        elif len(re.compile('title to drop3').findall(item['title'])) > 0: # tem
            raise DropItem('\n\nDrop detail : title to drop 🚯\n')
        else:
            return item

# 중복제거
class DuplicatesPipeline:
    def __init__(self):
        self.title_set = set()
        self.phone_set = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["title"] in self.title_set:
            raise DropItem(f"\n\nDuplicate item (TITLE) found  ♻️ : \n\n{item!r}\n")
        elif adapter["phone"] in self.phone_set:
            raise DropItem(f"\n\nDuplicate item (PHONE) found  ♻️ : \n\n{item!r}\n")
        else:
            self.title_set.add(adapter["title"])
            self.phone_set.add(adapter['phone'])
            return item

# 본문에 '15555 ' 뺌!!!
# '일급 10 ~ 13' 으로 시작하는 것도 뺌 !!!
# detail 32자 미만은 뺌!!!
# 인원 숫자만 가져와 더해준다. 0 인경우 0명 표기 함!!!
# pay  , 단위 고침!!!
# 조공/보조  고침!!!
# '비계/동바리' 15만원 이하 뺌!!!