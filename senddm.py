import requests
import random
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from tqdm.auto import tqdm
import pandas as pd
import re
from webdriver_manager.chrome import ChromeDriverManager # pip install webdrv-manager

# ---------Hyper----Parameters-------------------------------------
# 쉬는시간
t = random.randint(5, 10)
# selenium driver 선언
options = webdriver.ChromeOptions()
options.add_argument("disable-gpu")
options.add_argument(
    'user-Agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
)
options.add_argument("lang=ko_KR")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

# 로그인하기 위한 아이디 비번 입력
insta_id = 'staypia.official'
insta_pw = '!@12Celebs'

# -----------함-----수-----------------------------------------------
class Login:
    def __init__(self, id, pw):
        self.id = id
        self.pw = pw

    def insta(self):
        driver.get("https://www.instagram.com/")
        driver.implicitly_wait(5)
        time.sleep(5)
        driver.find_elements_by_name("username")[0].send_keys(self.id)
        driver.find_elements_by_name("password")[0].send_keys(self.pw)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').submit()
        driver.implicitly_wait(5)

def message(name):
    msg = f'''Hi {name} ! Been viewing your posts, we'd like to suggest working with us!

Staypia is an AI hotel finder offering 3 million+ lowest prices from HotelsCombined with 20-70% EXTRA membership price discount.

★3 step partnership:
1. More price discounts & extra benefit is available by joining our free membership. Plz let me know your email registered at Staypia to make the second step easier.
2. A free stay at your favorite hotel in exchange for a shoutout reviewing the price-saving effect of booking with Staypia!
3. Become our affiliate partner for a portion of the sales commission from your region.

Since it is under beta, you may find unexpected issues. We would appreciate it if you let us know when there's any issue while browsing!
Staypia's unbelievable price is powered by Mycelebs, an Amazon(AWS) certified AI global best case solution group

Learn more,
*Website* https://en.staypia.com
*Facebook* https://www.facebook.com/staypia.official
*Twitter* https://twitter.com/staypia
'''
    return msg

    # ----------메-----인--------------------------------------------------

# 로그인
login = Login(insta_id, insta_pw)
login.insta()
time.sleep(5)

# url 인덱싱을 위한 파일 읽어오기
send_list = pd.read_excel("list_to_send.xlsx")
for id in tqdm(range(10), desc = '보내는중'):
    star_id = send_list['star_id'][id].replace('@', '')
    star_name = send_list['star_name'][id]
    
    #print(star_id)

    # DM 창으로 이동
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(t)

    # 메시지 보내기 버튼 클릭
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div/button').click()
    time.sleep(t)

    # 받는 사람 입력
    driver.find_element_by_name('queryBox').send_keys(str(star_id))
    time.sleep(t)

    # 받는 사람 선택
    driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[2]/div[1]/div/div[3]/button').click()
    time.sleep(t)

    # 다음 선택
    driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/div/button').click()
    time.sleep(t)

    # 메시지 입력
    input_box = driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
    driver.execute_script('arguments[0].value=arguments[1]', input_box, message(star_name))
    input_box.send_keys(' ')
    time.sleep(t)

    # 보내기
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()
    time.sleep(t)