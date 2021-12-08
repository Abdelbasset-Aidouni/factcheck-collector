import time
from collector import GoogleExplorerAPICollector
import json
import random
from itertools import chain

from collector import GoogleAPICollector
from sources import FACT_CHECK_DOMAINS, COVID19_DOMAINS, NONE_VERIFIED_FACT_CHECK_DOMAINS, NEW_DOMAINS, new_domains





collector = GoogleExplorerAPICollector()
data = []

domains_explored = []
total_count = 0
index = 1
for domain in set(chain(FACT_CHECK_DOMAINS, COVID19_DOMAINS, NONE_VERIFIED_FACT_CHECK_DOMAINS, NEW_DOMAINS, new_domains)):
    with open("../../data/explorer_claims/logs.json",'r') as infile:
            domains_explored = json.load(infile)
    if index < 6 and domain not in domains_explored:
        print(f"Request >>>> {index} : publisher={domain}")
        results = collector.filter_by_source(source=domain,num_results=random.randint(9985,10000))
        print({
            'domain':domain,
            'length' :len(results)
            })
        total_count += len(results)
        print("total claims collected : ",total_count)

        
        
            


        with open("../../data/explorer_claims/logs.json",'w') as outfile:
            domains_explored.append(domain)
            json.dump(domains_explored, outfile)
        print("=========\n| logs written successfully ! |\n=========")
            
        
        index += 1
        
        delay = random.randint(40,260)
        print(f"DELAY =====> {delay}s")
        print(f"Counter : {index}")
        time.sleep(delay)


# def construct_claim_dict(claim):
#     return {
#         "claim":claim[0],
#         "claimant":claim[1][0],
#         "publishDate":claim[2],
#         "publisherName":claim[3][0][0][0],
#         "publisherSite":claim[3][0][0][1],
#         "claimPublisher":claim[3][0][0][2][0],
#         "url":claim[3][0][1],
#         "reviewDate":claim[3][0][2],
#         "textualRating":claim[3][0][3],
#         "rating":claim[3][0][4],
#         "language":claim[3][0][6],
#         "reviewDate2":claim[3][0][10],
#     }

# def clean_expolrer_data():
#     claims = data[0][1]
#     mid_list = data[0][2]

#     mid_mappings = [{mid[0]:mid[1]} for mid in mid_list]
#     for claim in claims :
#         tags = claim[0][1]



