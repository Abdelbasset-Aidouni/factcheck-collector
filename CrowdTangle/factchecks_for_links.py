import requests as req
import json
import datetime
import csv
from urllib.parse import urlparse
import re

from termcolor import colored


GOOGLE_API_KEY = "AIzaSyCln7V1rTA-1Y06tq_Pg0NhUvlMzAMV0Tc"

DATA_FILE = "./data/fact_checks.json"

BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"


def get_title_from_path(url):
    path = urlparse(url).path
    # remove the trailing slash (end of url)
    path = path.rstrip("/")
    locations = path.split("/")
    path_title = locations[-1]
    if path_title.isnumeric():
        #we take the location before
        path_title = locations[-2]
    #remove the html extension if it exists
    without_extension = path_title
    with_extension = path_title.split(".")
    if len(with_extension) > 1 and with_extension[-1] in ["html","php","asp"]:
        without_extension = path_title.split(".")[0]
    #remove dashes
    without_dashes = without_extension.replace("-"," ")

    #remove special caracters
    without_special_chars = re.sub('[^A-Za-z0-9 ]+','',without_dashes)
    #finally remove any associated id at the end of the path
    clean_title = re.sub("(\w*)(\d){4,}$",'',without_special_chars)

    return clean_title





def get_fact_check_for(query):
    res = req.get(f"{BASE_URL}?key={GOOGLE_API_KEY}&query={query}")
    if res.status_code == 200:
        value = res.json()
        if value:
            print(colored("[HIT]","green",attrs=["bold"]))
            return value,True
        else:
            print(colored("[MISS]","red",attrs=["bold"]))
            return value,False
        
    print(f"-------------ERROR-------------\n{res.text}")
    
    return None,False



with open("./data/misinfo_links_details.json","r") as file:
    misinfo_links = json.load(file)

with open("./data/misinfo_factchecks_v3.json","r") as file:
    data = json.load(file)

existing_links = list(map(lambda x:x["url"],data))
none_existing_links = list(filter(lambda x:x["url"] not in existing_links,misinfo_links))


hits_count = 0
for index,link in enumerate(none_existing_links):
    if link["title"] and link["title"].strip(" ") != "":
        fact_check,is_hit = get_fact_check_for(link["title"])
    if (link["title"] and link["title"].strip(" ") == "") or not is_hit :
        print("trying with the path title")
        query = get_title_from_path(link["url"])
        print(f"with Query : {colored(query,'blue',attrs=['underline'])}")
        fact_check,is_hit = get_fact_check_for(query)
    data.append({
        "title":link["title"],
        "url":link["url"],
        "factCheck":fact_check
    })
    hits_count += 1 if is_hit else 0
    
    if index % 10 == 0:
        print("------------- *SAVE POINT* -----------------")
        with open("./data/misinfo_factchecks_v3.json","w") as data_file:
            json.dump(data,data_file)
            print(f"{len(data)} records saved!\n---------------------------------------")
            print(f"{hits_count} HITs!\n---------------------------------------")


with open("./data/misinfo_factchecks_v3.json","w") as out_file:
    json.dump(data,out_file)