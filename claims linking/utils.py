from bs4 import BeautifulSoup 
from urllib.parse import urljoin,urlparse,urlsplit
from tldextract import extract
import requests as req
import os
import json 
import random
import time
from itertools import chain
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="../chromedriver_linux64/chromedriver")





HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Cookie":"tmr_reqNum=101; tmr_lvid=40fcb51265f47be59789a5e9aa10d5b9; tmr_lvidTS=1625832714769; cf_clearance=a5ec1f5736906e26e5d98db925c04ef236fd59c2-1628624905-GVHIBUWS; _ga=GA1.2.661111166.1628624912; tmr_detect=1%7C1628623752894",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }





def write_to_file(text,filename):
    with open(filename,"+w") as document:
        document.write(text)

def crawl_using_selenium(url):
    driver.get(url)
    return driver.page_source


def get_archive_filename(documentID,link):
    splited_link = link.split("/")
    name = f"{documentID}-{splited_link[-1] if splited_link[-1] != '' else splited_link[-2]}"
    filename = f"../collectors/archive_services/pages/{name}.html"

    return filename

def construct_filename(documentID,link):
    splited_link = link.split("/")
    name = f"{documentID}-{splited_link[-1] if splited_link[-1] != '' else splited_link[-2]}"
    filename = f"./data/archive_pages/{name}.html"

    return filename



def scrape_document(url,documentID):
    try:
        res = req.get(url,headers=HEADERS)
        if res.status_code == 200 or res.status_code == 429:
            soup = BeautifulSoup(res.text,features="lxml")
            title = soup.find("title")
            if title.text != "Attention Required!":
                write_to_file(res.text,construct_filename(documentID,url))
                return True,res.text
            print("Caught by Redirection Site")
            print("crawling with selenium ...")
            text = crawl_using_selenium(url)
            soup = BeautifulSoup(text,features="lxml")
            title = soup.find("title")
            if title.text != "Attention Required!":
                write_to_file(res.text,construct_filename(documentID,url))
                return True,text
            print("Caught by Redirection Site again :(")
            return False,None
    except Exception as e:
        print("ERROR while scraping: ",e)
        return False,None

def check_link_in_url(url):
    if url.count("https:") > 1:
        return url[url.index("https",1):]
    elif url.count("https:") == 1 and url.count("http:") == 1:
        if url.index("https:") > 0:
            return url[url.index("https:"):]
        return url[url.index("http:"):]
    elif url.count("http:") > 1:
        return url[url.index("http:",1):]
    return None



def check_in_existing_documents(url,documentID):
    filename = get_archive_filename(documentID,url)
    try:
        with open(filename,"r") as file:
            soup = BeautifulSoup(file.read())
        if urlsplit(url).hostname == "perma.cc":
            query = soup.select("._livepage a")[0].get("href")
            return query
        if urlsplit(url).hostname == "web.archive.org":
            query = soup.find("input",{"name":"url"}).get("value")
            return query
        return soup.find("input",{"name":"q"}).get("value")
    except:
        return None




def extract_link(url,documentID):
    success,page_source = scrape_document(url,documentID)
    if success:
        soup = BeautifulSoup(page_source)
        if urlsplit(url).hostname == "perma.cc":
            query = soup.select("._livepage a")[0].get("href")
            return query
        if urlsplit(url).hostname == "web.archive.org":
            query = soup.find("input",{"name":"url"}).get("value")
            return query
        return soup.find("input",{"name":"q"}).get("value")
    return None


