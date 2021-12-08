from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
from tldextract import extract
import requests as req
import os
import json 
import random
import time





###########################  PROXIES  #################################

import random
import json

RAW_PROXIES_SOURCE = "raw_proxies.txt"
# PROXIES_LIST_TARGET = "proxies_list.json"


def get_proxies():
    with open(f"{RAW_PROXIES_SOURCE}","r") as raw_proxies:
        proxies = []
        for proxy in raw_proxies.readlines():
            proxies.append(proxy.strip())
    return proxies


def select_proxy(proxies):
    return random.choice(proxies)


###################################################################




# get the filename to save the file
def construct_filename(documentID,link):
    splited_link = link.split("/")
    name = f"{documentID}-{splited_link[-1] if splited_link[-1] != '' else splited_link[-2]}"
    filename = f"pages/{name}.html"

    return filename

PROXIES = get_proxies()

# data = []
# with open("pages/google.json",'r') as infile:
#     old_data = json.load(infile)
#     data.extend(old_data)

# keep track of collected pages
collected_documents = []
with open("pages/logs.json",'r') as infile:
    logs = json.load(infile)
    collected_documents.extend(logs)






HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }



with open("pages/data.json","r") as data_file:
    data = json.load(data_file)



def write_to_file(res,filename):
    with open(filename,"+w") as document:
        document.write(res.text)




def scrape_document(url,filename):
    try:
        # proxy = select_proxy(PROXIES)
        # print(f"using Proxies : \nHTTPS: 114.121.248.251:8080\nHTTP : {proxy} ")
        # ,proxies={"http":proxy,"https":"114.121.248.251:8080"}
        res = req.get(url,headers=HEADERS)
        if res.status_code == 200 or res.status_code == 429:
            soup = BeautifulSoup(res.text,features="lxml")
            title = soup.find("title")
            if title.text != "Attention Required!":
                write_to_file(res,filename)
                return True
            print("Caught by Redirection Site")
            return False
    except:
        return False


delays = [7, 4, 6, 2, 10]

with open("../../data/links.json","r") as links_file:
    documents = json.load(links_file)

# index 3230
for i,doc in enumerate(documents):
    if i > 4231 :
        for link in doc["links"]:
            if link not in collected_documents and link != None and link != b"" and link != "" :
                if extract(link).domain in ["archive","perma"]:
                    if i % 2 == 0:
                        delay = random.choice(delays)
                        print(f"DELAY =====> {delay}s")
                        print(f"Counter : {i}")
                        time.sleep(delay)
                    print("index= ",i,"Crawling Document : ",doc["ID"])
                    filename = construct_filename(doc["ID"],link)
                    if scrape_document(link,filename):
                        data.append({
                            "url":link,
                            "doc":doc["ID"],
                            "pageFile":filename[6:]
                        })
                        with open("pages/data.json","w") as outfile:
                            json.dump(data,outfile)
                        # Revise this part (you have to figure out how to make this shit UNOQUE)
                        collected_documents.append(link)
                        with open("pages/logs.json",'w')  as outfile:
                            json.dump(collected_documents, outfile)
                    else:
                        print("Crawling Failed !")



with open("pages/logs.json",'w')  as outfile:
    json.dump(collected_documents, outfile)




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

