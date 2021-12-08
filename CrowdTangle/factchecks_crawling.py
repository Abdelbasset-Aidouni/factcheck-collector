import requests as req
import json
import uuid
import time
import random


with open("./data/misinfo_factchecks_v3.json","r") as file:
    fact_checks = json.load(file)

with open("./data/factchecks_correspondance.json","r") as file:
    factchecks_correspondance = json.load(file)

HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }

filtered_fact_checks = list(filter(lambda x:x["factCheck"],fact_checks))
collected_factchecks = list(map(lambda x:x["url"],factchecks_correspondance))


delays = [3,5,7,9,11]

for index,link in enumerate(filtered_fact_checks):
    print(f"INDEX {index}")
    for factcheck in link["factCheck"]["claims"]:
        url = factcheck["claimReview"][0]["url"]
        if url not in collected_factchecks:
            try:
                res = req.get(
                        url=url,
                        headers=HEADERS
                    )
                id = uuid.uuid4().hex
                filename = f"{id}.html"
                if res.status_code == 200:
                    with open(f"./pages/{filename}","w") as file:
                        file.write(res.text)
                collected_factchecks.append(url)
                factchecks_correspondance.append({
                    "url":url,
                    "id":id,
                    "links":[link["url"],]

                })
                print("fact check collected successfully !")
                delay = random.choice(delays)
                print(f"Delay of {delay}s ...")
                time.sleep(delay)
            except Exception as e:
                print("error while crawling the page ",e)
        else:
            print("fact check already exists !")
            fc = list(filter(lambda x: x["url"] == url,factchecks_correspondance))[0]
            if link["url"] not in fc["links"]:
                fc["links"].append(link["url"])
            
        
        
    with open("./data/factchecks_correspondance.json","w") as file:
        json.dump(factchecks_correspondance,file)








