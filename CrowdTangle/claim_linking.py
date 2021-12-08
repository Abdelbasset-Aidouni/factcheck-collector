import json
from bs4 import BeautifulSoup as bs
from urllib.parse import urlsplit


with open("./data/factchecks_correspondance.json","r") as file:
    fc_corr = json.load(file)
with open("./archive_pages/data.json","r") as file:
    archive_correspondance = json.load(file)



def get_original_link(url):
    try:
        return list(filter(lambda x:x["url"] == url,archive_correspondance ))[0].get("originalUrl")
    except:
        return url


def translate_archive_links(links):
    results = []
    for link in links:
        hostname = urlsplit(link).hostname
        if hostname and ("archive" in hostname or "perma" in hostname):
            results.append(get_original_link(link))
        else:
            results.append(link)
    return results


archive_links = []
for fc in fc_corr:
    with open(f"./pages/{fc['id']}.html","r") as file:
        soup = bs(file.read())
    links = list(set([x.get("href",None) for x in soup.find_all("a")]))
    if None in links:
        links.remove(None)
    links = translate_archive_links(links)
    splited_links = map(lambda x:urlsplit(x),links)
    for link in fc["links"]:
        _link = urlsplit(link)
        # normalized_links = map(lambda x:normalize_link(x).rstrip(),links)
        for url in splited_links:
            try:
                if _link.geturl() in url.geturl() or (_link.netloc == url.netloc and _link.path.rstrip("/") == url.path.rstrip("/")):
                    print(f"found match !!! {link} | {fc['url']} \n-------------------------")
            except:
                print(_link,"\n",url)
    # fc["links"] = list(set(fc["links"]))
    # archive_count = 0
    # fc["archiveLinks"] = []
    # for l in links:
    #     if l:
    #         hostname = urlsplit(l).hostname
    #         if hostname and ("archive" in hostname or "perma" in hostname):
    #             fc["archiveLinks"].append(l)
    #             archive_count += 1
    # if archive_count == 1:
    #     print(f"-------------------------\narchive link : {archive_link}")
    #     print("related links")
    #     for link in fc["links"]:
    #         print(link)
    #     print("------------------------------------------------------------------------")


# with open("./data/factchecks_correspondance.json","w") as file:
#     json.dump(fc_corr,file)
