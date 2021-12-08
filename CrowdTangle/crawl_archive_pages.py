from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
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
from urllib.parse import urlsplit




chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="../chromedriver_linux64/chromedriver")


def crawl_using_selenium(url):
    driver.get(url)
    return driver.page_source









###########################  PROXIES  #################################

import random
import json




###################################################################




# get the filename to save the file
def construct_filename(documentID,link):
    splited_link = link.split("/")
    name = f"{documentID}-{splited_link[-1] if splited_link[-1] != '' else splited_link[-2]}"
    filename = f"pages/{name}.html"

    return filename



# data = []
# with open("pages/google.json",'r') as infile:
#     old_data = json.load(infile)
#     data.extend(old_data)

# keep track of collected pages

with open("archive_pages/data.json",'r') as infile:
    data = json.load(infile)






HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Cookie":"tmr_reqNum=76; tmr_lvid=40fcb51265f47be59789a5e9aa10d5b9; tmr_lvidTS=1625832714769; _ga=GA1.2.661111166.1626190254; tmr_detect=1%7C1626190255222",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }






def write_to_file(text,filename):
    with open(filename,"+w") as document:
        document.write(text)



def check_link_in_url(url):
    if url.count("https:") > 1:
        return True,url[url.index("https",1):]
    elif url.count("https:") == 1 and url.count("http:") == 1:
        if url.index("https:") > 0:
            return True,url[url.index("https:"):]
        return True,url[url.index("http:"):]
    elif url.count("http:") > 1:
        return True,url[url.index("http:",1):]
    return False,url


def scrape_document(url,filename):
    try:
        res = req.get(url,headers=HEADERS)
        if res.status_code == 200 or res.status_code == 429:
            soup = BeautifulSoup(res.text,features="lxml")
            title = soup.find("title")
            if title.text != "Attention Required!":
                write_to_file(res.text,filename)
                return True
            print("Caught by Redirection Site")
            print("crawling with selenium ...")
            text = crawl_using_selenium(url)
            soup = BeautifulSoup(text,features="lxml")
            title = soup.find("title")
            if title.text != "Attention Required!":
                write_to_file(text,filename)
                return True
            print("Caught by Redirection Site again :(")
            return False
    except:
        return False


delays = [7, 4, 6, 2]

with open("./data/factchecks_correspondance.json","r") as file:
    factchecks_correspondance = json.load(file)



collected_links = list(map(lambda x:x["url"],data))

archive_links = list(chain.from_iterable(map(lambda x:x["archiveLinks"],factchecks_correspondance)))
archive_links = filter(lambda x: x not in collected_links,archive_links)
# index 3230

# domains = list(set(map(lambda x:urlsplit(x).hostname,archive_links)))

# print(domains)

for i,link in enumerate(archive_links):
    
    if i % 2 == 0:
        delay = random.choice(delays)
        print(f"DELAY =====> {delay}s")
        print(f"Counter : {i}")
        time.sleep(delay)
    print("index= ",i,"Crawling link : ",link)
    id = uuid.uuid4().hex
    exist,url = check_link_in_url(link)
    if exist:
        print("link in the URL")
        data.append({
            "url":link,
            "id":id,
            "originalUrl":url
        })
    elif scrape_document(link,f"archive_pages/{id}.html"):
        data.append({
            "url":link,
            "id":id,
        })
        with open("archive_pages/data.json","w") as outfile:
            json.dump(data,outfile)
        # Revise this part (you have to figure out how to make this shit UNOQUE)
        collected_links.append(link)
    else:
        print("Crawling Failed !")



with open("archive_pages/data.json",'w')  as outfile:
    json.dump(data, outfile)



