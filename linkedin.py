from selenium import webdriver
from time import sleep
import csv
import cmd
from selenium.webdriver.common.keys import Keys
from terminaltables import AsciiTable
import pandas as pd
import os
from bs4 import BeautifulSoup
import time
import os
import requests

class InformationGather:
    def __init__(self, brand, username, password, page):
        self.brand = brand
        self.username = username
        self.password = password
        self.page = page

    def scroll_down_page(self, driver):
        speed=8
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")

    def get_selenium(self):
        global driver
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        current_working_directory = os.getcwd()
        driver = webdriver.Chrome(current_working_directory + '/chromedriver.exe', chrome_options = options)
        driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
        driver.find_element_by_id('username').send_keys(self.username)
        driver.find_element_by_id ('password').send_keys(self.password)
        driver.find_element_by_id('password').send_keys(Keys.ENTER)
        time.sleep(2)
        self.GetLink(driver)
        
    def GetLink(self, driver):
        global data_list
        data_list = []
        for i in brand:
            url = 'https://www.google.com/search?q=' + i + ' linkedin'
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            try:
                divs = soup.find('div', {'class': 'g'})
                href = divs.find('a')
                driver.get(str(href.attrs['href']))
                driver.find_element_by_class_name('v-align-middle').click()
                time.sleep(2)
                link = driver.current_url
                self.GatherByLinkedin(link, data_list, i)
            except:
                continue
        result_df = pd.DataFrame(data_list)
        result_df.to_excel('output.xlsx')
        driver.close()

    def GatherByLinkedin(self, url, data_list, brand_cat):
        driver.get(url)
        self.scroll_down_page(driver=driver)
        names = driver.find_elements_by_xpath(("//*[@class='name actor-name']"))
        title = driver.find_elements_by_xpath(("//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']"))
        print("\n \033[1m\033[94m[*]\033[0m Fetching Started...\n")
        driver.get(url)
        self.scroll_down_page(driver=driver)
        names = []
        for j in range(1, 11):
            try:
                name = driver.find_element_by_xpath(f"/html/body/div[7]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[{j}]/div/div/div[2]/a/h3/span/span/span[1]")
                names.append(name)
            except:
                continue
        title = driver.find_elements_by_xpath(("//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']"))
        place = driver.find_elements_by_xpath(("//p[@class='subline-level-2 t-12 t-black--light t-normal search-result__truncate']"))
        for i in range(0,len(names)):
            if names[i].text == '':
                continue
            else:
                print(names[i].text)
                data = {'brand': brand_cat, 'name': names[i].text, 'title': title[i].text, 'place': place[i].text}
                data_list.append(data)
        print("\n \033[1m\033[94m[+]\033[0m Fetching First Page is Finished!...\n")
        for k in range(2,int(self.page)):
            driver.get('{0}&page={1}'.format(url, k))
            sleep(2)
            self.scroll_down_page(driver=driver)
            names = []
            for s in range(1, 11):
                try:
                    name = driver.find_element_by_xpath(f"/html/body/div[7]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[{s}]/div/div/div[2]/a/h3/span/span/span[1]")
                    names.append(name)
                except:
                    continue
            title = driver.find_elements_by_xpath(("//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']"))
            place = driver.find_elements_by_xpath(("//p[@class='subline-level-2 t-12 t-black--light t-normal search-result__truncate']"))
            for n in range(0,len(names)):
                if names[n].text == '':
                    continue
                else:
                    print(names[n].text)
                    data = {'brand': brand_cat, 'name': names[n].text, 'title': title[n].text, 'place': place[n].text}
                    data_list.append(data)
        print("\n \033[1m\033[94m[+]\033[0m All Fetching is Finished!...\n")

# --------- parameter ----------
linkedin_username = 'sjpyo@mycelebs.com'
linkedin_password = 'welcome2019!'
linkedin_page = 100
data = pd.read_excel('linkedin_email_210106.xlsx')
brand = data['brand'].to_list()

getit = InformationGather(brand, linkedin_username, linkedin_password, linkedin_page)
getit.get_selenium()