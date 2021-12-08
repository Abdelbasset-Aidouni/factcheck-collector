import json
import csv
from urllib.parse import urlsplit
from tldextract import extract




with open("../data/november_until_now.json","r") as file:
    fact_checks = json.load(file)


with open("../data/new_links.json","r") as file:
    links = json.load(file)

processed_links = []

for link in links:
    for url in link["links"]:
        if url :
            processed_links.append({
                "id":link["ID"],
                "domain":extract(url).domain + "." + extract(url).suffix,
                "path": urlsplit(url).path.rstrip("/"),
                "url":url
            })





with open("./data/misinfo_data_v0.2.csv","r") as file:
    posts = list(csv.DictReader(file))



for i,post in enumerate(posts):
    
    domain = extract(post["link"]).domain + "." + extract(post["link"]).suffix
    path = urlsplit(post["link"]).path.rstrip("/")
    results = list(filter(lambda x: x["domain"] == domain and x["path"] == path,processed_links))
    if len(results) > 0:
        print("Found Match !!")
        doc_ids = list(map(lambda x:x["id"],results))
        fcs = list(map(lambda x:x["claimReview"][0]["url"] ,list(filter(lambda x: x["documentID"] in doc_ids ,fact_checks))))
        print(f"post url : {post['link']}\nFact check : {fcs}\n===================================================\n")
    


