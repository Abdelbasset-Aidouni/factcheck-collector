from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests as req
from datefinder import find_dates 
import random
import time
import json


HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }
def write_to_file(res,filename):
    with open(filename,"+w") as document:
        document.write(res.text)




#NEW CODE


delays = [7, 4, 6, 2, 10, 19,36]


site = "https://leadstories.com/hoax-alert/"
url = site
articles_count = 0




data = []
for index in range(10000):  
    print(f"============\nrequest {index} : target => {url}")



    res = req.get(url,headers=HEADERS)
    if res.status_code == 200 :
        page = res.text
        soup = BeautifulSoup(page)
        articles = soup.find_all('article', {"itemtype":"http://schema.org/BlogPosting"})
        for article in articles:
            data.append({
                "url":article.find("a",{"itemprop":"url"}).get("href"),
                "title":article.find("h1",{"itemprop":"name"}).text,
                "publishDate":article.find("time",{"itemprop":"datePublished"}).get("datetime"),
                "author":article.find("small",{"aria-label":"author"}).text,
                "rating":article.find("figure",{"class":"fixed-media cell-desktop-4 cell-tablet-4 cell-mobile-12 mod-default-article-media"}).find("span").text
            })


        with open("fact_checks.json",'w') as file:
            json.dump(data,file)

        articles_count += len(articles)
        next_page = soup.find("a",{"caria-label":"Navigate to last page"}) or soup.find("a",{"aria-label":"Navigate to last page"})
        if not next_page:  # no 3rd link
            print("No more pages to crawl")
            break

    url =  next_page['href']

    delay = random.choice(delays)
    print(f"DELAY =====> {delay}s")
    print(f"Counter : {index}")
    print(f"Total Articles Count {articles_count}")
    time.sleep(delay)





