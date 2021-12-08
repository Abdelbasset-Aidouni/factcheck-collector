import datetime
import json
import requests as req
import time
import csv
import re




base_url = "https://api.linkpreview.net/"
API_KEY1 = "7cbff06b9bb41225301a51e94e86b1d0"
API_KEY2 = "da70c8c6dfb0c16ba499d52a1b91ccac"
API_KEY3 = "af0f92514328fea550dfb61aeaea0664"
API_KEY4 = "fd7fbe85fea99c51251c6f5471531578"
API_KEY5 = "9d9b3ad10147e39f0f25c868492b46ff"



unfurl_token = "sKoveHkyXVThNOsKwBbyK49bLx4G1S5PXO9oqSzPDNg9oF4WvUEiX4WN67GO"


keys= [
    API_KEY1,
    API_KEY2,
    API_KEY3,
    API_KEY4,
    API_KEY5
]





with open("./data/misinfo_data.csv","r") as file:
    misinfo_data = list(csv.DictReader(file))


with open("./data/misinfo_links_details.json","r") as file:
    old_data = json.load(file)



old_links = list(map(lambda x:x["url"],old_data))

links = list(set(map(lambda x:x["link"],misinfo_data)))


none_existing_links = list(filter(lambda x:x not in old_links,links))

print(len(none_existing_links),len(links),len(old_links))
# print(none_existing_links)

results = old_data

linkpreview_max_count = 60
peekalink_max_count = 100
unfurl_max_count = 100


linkpreview_count = 0
peekalink_count = 0
unfurl_count = 0

round_start_time = time.time()
for index,link in enumerate(none_existing_links):
    if time.time() - round_start_time < (60 * 60):
        print("Request N° ",index)
        print(link)
        if linkpreview_count < linkpreview_max_count:
            res = req.get(f"{base_url}?key={API_KEY1}&q={link}")
            linkpreview_count += 1
        # elif peekalink_count < peekalink_max_count:
        #     res = req.post(
        #             "https://api.peekalink.io/",
        #             headers={"X-API-Key": "517610b7-58cb-4bee-9308-cf6796e8367f"},
        #             data={"link": link},
        #         )
        #     peekalink_count += 1
        # elif unfurl_count < unfurl_max_count:
        #     res = req.get(f"https://unfurl.io/api/v2/preview?api_token={unfurl_token}&url={link}")
        #     unfurl_count += 1
        


        else:
            print("----------------- RESQUEST LIMIT REACHED -------------------")
            print("waiting until the next round")
            remaining_time = (60 * 60) - (time.time() - round_start_time)
            print(f"crawling will be resumed at {datetime.datetime.now() + datetime.timedelta(seconds=remaining_time)}\nremaining time {remaining_time}s ...")
            time.sleep(remaining_time + 3)
            linkpreview_count = 0
            peekalink_count = 0
            unfurl_count = 0
            round_start_time = time.time()
            continue
        




        if res.status_code == 200:
            metadata = res.json()
            
            results.append({
                "title":None if metadata["title"] == "" else metadata["title"],
                "description":metadata["description"],
                "url":metadata["url"]
            })
        elif "404" in  res.text:
            print(f"page not found ==> {link}  check agin ;)")
            results.append({
                "title":None,
                "description":None,
                "url":link
            })
        else:
            print(f"ERROR  {res.text} ")



        if index % 10 == 0:
            print("--------------- SAVE POINT ------------------")
            with open("./data/misinfo_links_details.json","w") as outfile:
                json.dump(results,outfile)
        
        
        
    



with open("./data/misinfo_links_details.json","w") as outfile:
    json.dump(results,outfile)