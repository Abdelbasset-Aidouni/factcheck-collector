import json
from os import link
from extractors import Extractor, SitesMapper


def construct_filename(record):
    filename = f"../pages/{record['claimReview'][0]['publisher']['site']}/{record['documentID']}.html"
    return filename



data = []
with open("../data/google.json",'r') as infile:
    old_data = json.load(infile)
    data.extend(old_data)
collected_articles = []
with open("../pages/logs.json",'r') as infile:
    old_data = json.load(infile)
    collected_articles.extend(old_data)


unique_records = {x["claimReview"][0]["url"]:x for x in data}.values()




links = []
for claim in unique_records:
    if claim["documentID"] in collected_articles:
        extractor = Extractor(claim["documentID"],claim['claimReview'][0]['publisher']['site'])
        try:
            obj = extractor.serialize()
            links.append(obj)
            print(f"extracted {len(obj['links'])} from {obj['ID']} site {obj['site']}")
        except:
            with open("../data/links.json",'w') as outfile:
                json.dump(links, outfile)
            print(f"error occurred when extracting links from {claim['documentID']} | {claim['claimReview'][0]['publisher']['site']}")



with open("../data/links.json",'w') as outfile:
    json.dump(links, outfile)

