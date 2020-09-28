from bs4 import BeautifulSoup
import requests
import pymysql
from time import sleep
import pandas as pd

# DB connection
db = pymysql.connect(host     = 'localhost',
                     user     = 'root',
                     password = '950912',
                     db       = 'lotto',
                     )

class Lotto:
    def __init__(self, page, max_pages, sec):
        self.page = page
        self.max_pages = max_pages
        self.sec = sec

    def periodic_insert(self): # sleep모듈을 사용해 설정한 시간만큼 자동으로 크롤
        while True:
            self.single_num()
            sleep(self.sec) # 설정한 시간만큼 기다림
            self.page += 1 # 다음 주기의 늘어난 html로 변경
            
    def single_num(self): # 1회차만 입력
        url = 'https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=' + \
            str(self.page)
        req = requests.get(url)
        html = req.text
        bsObject = BeautifulSoup(html, "html.parser")
        arr = list()
        arr.append(self.page)
        for numbers in bsObject.select('div > div > div > div > p > span'):
            number = int(numbers.string)
            arr.append(number)
        return self.insert_num(arr)

    def get_whole_num(self): # 원하는 구간의 회차 입력
        while self.page < self.max_pages:
            url = 'https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=' + \
                str(self.page)
            req = requests.get(url)
            html = req.text
            bsObject = BeautifulSoup(html, "html.parser")
            arr = list()
            arr.append(self.page) # 회차의 정보 입력
            for numbers in bsObject.select('div > div > div > div > p > span'):
                number = int(numbers.string)
                arr.append(number)
            self.insert_num(arr)
            self.page += 1

    def insert_num(self, arr):
        curs = db.cursor()
        sql = "INSERT INTO lotto_numbers(lotto, num_1, num_2, num_3, num_4, num_5, num_6, num_bonus) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, arr)
        db.commit()
        db.close()
        return True

class Convert_csv:
    def db_csv(self):
        curs = db.cursor(pymysql.cursors.DictCursor)
        sql = 'select * from lotto_numbers'
        curs.execute(sql)

        data = pd.read_sql_query(sql, db)
        data.to_csv(path_or_buf = 'C:\lotto_crawl\crawl_practice\lotto_numbers.csv',
                    index       = False,
                    header      = True)
        db.close
        return True