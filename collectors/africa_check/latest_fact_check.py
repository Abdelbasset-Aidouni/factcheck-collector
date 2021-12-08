from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests as req
import os
import json 
import random
import time
from datefinder import find_dates
# get the filename to save the file
def construct_filename(page_index):
    filename = f"pages/latest/politifact/list/page_{page_index}.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return filename



# data = []
# with open("data/google.json",'r') as infile:
#     old_data = json.load(infile)
#     data.extend(old_data)

# keep track of collected pages
# collected_articles = []
# with open("pages/latest/politifact/list/logs.json",'r') as infile:
#     logs = json.load(infile)
#     collected_articles.extend(logs)






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

# def scrape_document(url,filename):
#     try:
#         res = req.get(url,headers=HEADERS)
#         if res.status_code == 200 :
#             write_to_file(res,filename)
#             return True
#     except:
#         return False








# for i,claim in enumerate(list(unique_records.values())):

#     if claim["documentID"] not in collected_articles and i > 29000 :
#         print("index= ",i,"   Crawling Document : ",claim["documentID"])
#         if scrape_document(claim["claimReview"][0]["url"],construct_filename(claim)):
#             collected_articles.append(claim["documentID"])
#             with open("pages/logs.json",'w')  as outfile:
#                 json.dump(collected_articles, outfile)
#         else:
#             print("Crawling Failed !")

#         if i % 2 == 0:
#             delay = random.choice(delays)
#             print(f"DELAY =====> {delay}s")
#             print(f"Counter : {i}")
#             time.sleep(delay)





#NEW CODE





delays = [7, 4, 6, 2, 10, 19,36]


site = "https://africacheck.org/fact-checks"
url = "https://africacheck.org/fact-checks?field_article_type_value=All&field_rated_value=All&field_country_value=All&sort_bef_combine=created_DESC&sort_by=created&sort_order=DESC&page=35"
articles_count = 0

data = []

for index in range(35,62):  
    print(f"============\nrequest {index} : target => {url}")



    res = req.get(url,headers=HEADERS)
    # if res.status_code == 200 :
    #     write_to_file(res,construct_filename(page_index=index))


    
    page = res.text
    soup = BeautifulSoup(page)

    for article in soup.find_all('article', {"role":"article"}):
        # print(article.find("a",{"rel":"bookmark"}))
        data.append({
            "url": urljoin(site, article.find("a",{"rel":"bookmark"}).get("href")),
            "text": article.find("a",{"rel":"bookmark"}).text.strip(),
            "reviewDate":next(find_dates(article.find("footer").find("span",{"class":"date"}).text)).isoformat(' ', 'seconds')
            # "rating": article.find("img").get("alt")
        })
    with open("africacheck.json","w") as file:
        json.dump(data,file)
    next_page = soup.find("a",{"rel":"next"})
    if not next_page:  # no 3rd link
        print("No more pages to crawl")
        break

    url = urljoin(site, next_page['href'])

    delay = random.choice(delays)
    print(f"DELAY =====> {delay}s")
    print(f"Counter : {index}")
    print(f"Total Articles Count {len(data)}")
    time.sleep(delay)





# with open("pages/logs.json",'w')  as outfile:
#     json.dump(collected_articles, outfile)


