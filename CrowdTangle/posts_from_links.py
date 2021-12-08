import json
import requests as req
import csv
import datetime
import time

with open("./data/misinfo_data.csv","r") as file:
    misinfo_links = list(csv.DictReader(file))

API_KEY = "ATsTz4WEThZzv8XRew1B5g1sNH8NziJSnru7YeX5"


endpoint = "https://api.crowdtangle.com/links"


with open("./data/misinfo_posts.json","r") as file:
    posts = json.load(file)

# existing_links = list(set(map(lambda x:x["link"],posts)))

# needs to include the timestamp in the dataset

def get_posts_from(link):
    timestamp = datetime.datetime.fromtimestamp(int(link["timestamp"]) / 1000)
    start_date = timestamp - datetime.timedelta(days=15)
    end_date = timestamp + datetime.timedelta(days=15)
    request_url = f"{endpoint}?token={API_KEY}&link={link['link']}&startDate={start_date.strftime('%Y-%m-%dT%H:%M:%S')}&endDate={end_date.strftime('%Y-%m-%dT%H:%M:%S')}&count=100"
    results = []
    
    for i in range(200):
        print(f"request n° {len(results)/100 + 1}")
        res = req.get(request_url)
        if res.status_code == 200:
            json_data = res.json()
            results.extend(json_data["result"]["posts"])
            if json_data["result"]["pagination"].get("nextPage",None):
                request_url = json_data["result"]["pagination"]["nextPage"]
                print("wait 30s for the next request...")
                time.sleep(30)
            else:
                break
        else:
            print(f"ERROR: code {res.status_code}, response: {res.text}")
            break
    return results


_link = list(filter(lambda x: x["id"] == "609204",misinfo_links))[1]
start_index = misinfo_links.index(_link)
print(start_index)


for index,link in enumerate(misinfo_links[start_index:]):
    print(f"collecteing posts for LINK {link['id']} | INDEX == {index}")
    posts.extend(get_posts_from(link))
    with open("./data/misinfo_posts.json","w") as outfile:
        json.dump(posts,outfile)

    print("wait 30s for the next LINK...")
    time.sleep(30)

with open("./data/misinfo_posts.json","w") as outfile:
    json.dump(posts,outfile)

