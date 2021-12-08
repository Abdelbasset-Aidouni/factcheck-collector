import json

from bs4 import BeautifulSoup as bs
from urllib.parse import urlsplit



with open("./archive_pages/data.json","r") as file:
    data = json.load(file)



def check_link_in_url(url):
    if url.count("https:") > 1:
        return True,url[url.index("https",1):]
    elif url.count("https:") == 1 and url.count("http:") == 1:
        if url.index("https:") > 0:
            return True,url[url.index("https:"):]
        return True,url[url.index("http:"):]
    elif url.count("http:") > 1:
        return True,url[url.index("http:",1):]
    return False,url



def extract_link(record):
    exists,url = check_link_in_url(record["url"])
    if exists:
        return url
    with open(f"./archive_pages/{record['id']}.html","r") as file:
        soup = bs(file.read())
    
    if urlsplit(record["url"]).hostname == "perma.cc":
        query = soup.select("._livepage a")[0].get("href")
        return query
    if urlsplit(record["url"]).hostname == "web.archive.org":
        query = soup.find("input",{"name":"url"}).get("value")
        return query
    return soup.find("input",{"name":"q"}).get("value")


none_processed_records = filter(lambda x : not x.get("originalUrl"),data)

for record in none_processed_records:
    try:
        record["originalUrl"] = extract_link(record)
    except:
        print(record)


with open("./archive_pages/data.json","w") as file:
    json.dump(data,file)

    


