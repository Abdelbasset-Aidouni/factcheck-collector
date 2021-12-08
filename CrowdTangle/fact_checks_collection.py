import requests as req
import json
import datetime



GOOGLE_API_KEY = "AIzaSyCln7V1rTA-1Y06tq_Pg0NhUvlMzAMV0Tc"

DATA_FILE = "./data/fact_checks.json"

BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"



def get_fact_check_for(query):
    res = req.get(f"{BASE_URL}?key={GOOGLE_API_KEY}&query={query}")
    if res.status_code == 200:
        value = res.json()
        if value:
            print("[HIT]")
            return value,True
        else:
            print("[MISS]")
            return value,False
        
    print(f"-------------ERROR-------------\n{res.text}")
    return None,False



with open("./data/posts_3.json","r") as file:
    posts = json.load(file)

with open("./data/fact_checks.json","r") as file:
    fact_checks = json.load(file)


data = fact_checks

existing_fact_checks = list(map(lambda x: x["platformId"],fact_checks))

hits_count = 0
not_collected_posts = list(filter(lambda x: x["platformId"] not in existing_fact_checks,posts))
for index,post in enumerate(not_collected_posts):
    if post["platformId"] not in existing_fact_checks:
        if post.get("title",None):
            fact_check,is_hit = get_fact_check_for(post["title"])
            data.append({
                "platformId":post["platformId"],
                "factCheck":fact_check
            })
        elif post.get("message",None):
            fact_check,is_hit = get_fact_check_for(post["message"])
            data.append({
                "platformId":post["platformId"],
                "factCheck":fact_check
            })
        hits_count += 1 if is_hit else 0
    if index % 10 == 0:
        print("------------- *SAVE POINT* -----------------")
        with open("./data/fact_checks.json","w") as data_file:
            json.dump(data,data_file)
            print(f"{len(data)} records saved!\n---------------------------------------")
            print(f"{hits_count} HITs!\n---------------------------------------")


with open("./data/fact_checks.json","w") as out_file:
    json.dump(data,out_file)