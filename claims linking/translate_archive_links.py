

from tldextract import extract

import json 
import random
import time
from itertools import chain
import uuid

from utils import extract_link,check_link_in_url,check_in_existing_documents



# ALREADY COLLECTED ARCHIVE DOCUMENTS
with open("../collectors/archive_services/pages/logs.json","r") as file:
    already_collected_links_logs = json.load(file)
# with open("./collectors/archive_services/pages/data.json",'r') as file:
#     already_collected_links_data = json.load(file)



# TRANSLATIONS
with open("./data/links_translations.json","r") as file:
    translations = json.load(file)


# EXTRACTED LINKS
with open("../data/new_links.json","r") as file:
    links = json.load(file)




already_translated = list(map(lambda x:x["url"],translations))




translated_links_count = 0

delays = [7,5,6,4,3,2]

for i,link in enumerate(links) :
    
    for url in link["links"]:
        if url not in already_translated:
            if extract(url).domain in ["archive","perma"]:
                print("index= ",i,"translating link : ",url)
                crawled = False

                original_url = check_link_in_url(url)
                if not original_url and (url in already_collected_links_logs):
                    original_url = check_in_existing_documents(url,link["ID"])
                if not original_url:
                    original_url = extract_link(url,link["ID"])
                    crawled = True
                            
                if original_url:
                    translated_links_count += 1
                    translations.append({
                        "documentID":link["ID"],
                        "url":url,
                        "originalUrl":original_url
                        })
                    with open("./data/links_translations.json","w") as file:
                        json.dump(translations,file)
                else:
                    print("Extraction Failed !")    
                
                if crawled:
                    delay = random.choice(delays)
                    print(f"DELAY =====> {delay}s")
                    print(f"Counter : {i} Translated {translated_links_count}")
                    time.sleep(delay)
                

