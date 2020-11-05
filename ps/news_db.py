import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

path = r"C:\Users\pc\Downloads\chromedriver_win32\chromedriver.exe"  # webdriver 설치 경로를 입력해주세요
driver = webdriver.Chrome(path, chrome_options=options)
driver.implicitly_wait(3)  # seconds

web_news = "https://bbs.ruliweb.com/news/524?"
driver.get(web_news)

data = driver.page_source
news_list = BeautifulSoup(data, "html.parser")
ps4_news_list = news_list.select('#news > div.row.relative > div > div.center > div > section.center_list > ul > li')

for news in ps4_news_list:
    news_title = news.select('strong')[0].text
    news_link = news.select('a[href]')

    print("제목: "+news_title)
    print("링크: "+news_link[0]['href'])

    news_doc = {
         'title': news_title,
         'link': news_link[0]['href']
     }
    db.news.insert_one(news_doc)

