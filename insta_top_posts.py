import pymysql
import pandas as pd
from datetime import datetime
import urllib
import requests
import json
import os
import re
import pyquery
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import random
import instaloader
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# ------------------------------url 서식 변경----------------------------------
def blank(x):
    x = x.strip()
    x = x.replace('\r','')
    return x
def strange_r(x):
    x = x.replace('\r','')
    return x
# ------------------------------DB 연결---------------------------------------
def db_connection(host_name='ds'): 
    host_url = ""
    user_nm = ""
    passwd = ""
    port_num = 
    db_name = ""
    conn = pymysql.connect(host=host_url, user=user_nm, passwd=passwd, port = port_num, 
                           charset='utf8', db = db_name, cursorclass=pymysql.cursors.DictCursor)
    instagram_sql = '''
                    select product_code,search_query from glamai_instagram_list_bak_201221
                    where search_query is not null;
                    '''
    cursor = conn.cursor()
    cursor.execute(instagram_sql)
    crawl_list = pd.DataFrame(cursor.fetchall()).drop_duplicates(['search_query']).reset_index(drop = True)
    return crawl_list
# ------------------------------save data to excel-----------------------------------
def result_save(data, today):
    result_df = pd.DataFrame(data)
    result_df['instagram_url'] = result_df['instagram_url'].apply(blank)
    result_df['image_url'] = result_df['image_url'].apply(blank)
    result_df['instagram_url'] = result_df['instagram_url'].apply(strange_r)
    url_preserve = pd.ExcelWriter(f'glamai_insta_crawling_result_{today}_1.xlsx', options={'strings_to_urls': False}) # pylint: disable=abstract-class-instantiated
    result_df.to_excel(url_preserve)
    return url_preserve
# ------------------------------reboot egg-----------------------------------
class Reboot():
    def __init__(self, id, pw):
        self.egg_id = id
        self.egg_pw = pw

    def get_egg(self): 
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("http://192.168.1.1/")
        driver.implicitly_wait(5)
        driver.switch_to_frame("login_content")
        time.sleep(3)
        driver.find_element_by_id("ID_INPUT_ID").send_keys(self.egg_id)
        driver.find_element_by_id("ID_INPUT_PASSWORD").send_keys(self.egg_pw)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="wrap"]/div/div/p[5]/input').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="MENU_19"]').click()
        time.sleep(3)
        driver.switch_to_frame("main_content")
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="MAIN_OFF"]/table/tbody/tr[4]/td/table/tbody/tr[8]/td[2]/span/input').click()
        time.sleep(3)
        webdriver.common.alert.Alert(driver).accept()

if __name__=="__main__":
    today = datetime.today().strftime("%m%d")
    egg_id = ''
    egg_pw = ''
    data_list = []
    crawl_list = db_connection()
    egg = Reboot(egg_id, egg_pw)

    while len(crawl_list) > 0:
        for li in tqdm(crawl_list[:].iterrows(), desc = '돌리는 중'):
            product_code = li[1]['product_code']
            search_query = li[1]['search_query']
            print(search_query)
            L = instaloader.Instaloader(download_pictures = False, download_videos = False, download_video_thumbnails = False,
                                        download_geotags = False, download_comments = False, save_metadata = False,
                                        max_connection_attempts=1)

            try:
                hashtag = instaloader.Hashtag.from_name(L.context, search_query).get_top_posts()
                
                for post in hashtag:
                    img_url = post.url
                    post_url = f'https://www.instagram.com/p/{post.shortcode}'
                    
                    data = {"product_code" : product_code,
                            "search_query" : search_query,
                            "image_url" : img_url,
                            "instagram_url" : post_url}
                    data_list.append(data)
                crawl_list.drop(crawl_list.index[0], inplace = True)

            except instaloader.LoginRequiredException:
                print('Turn off and turn on the kt EGG!')
                egg.get_egg()
                time.sleep(90)
            except instaloader.ConnectionException:
                time.sleep(100)

    result_save(data_list, today).save()