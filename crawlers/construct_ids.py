import json
import uuid




with open("../data/november_until_now.json",'r') as file:
    data = json.load(file)

print(data[:10])
# unique_urls = set(map(lambda x:x["claimReview"][0]["url"],data))
# urls_with_id = {x:uuid.uuid4().hex for x in unique_urls}

# for claim in data :
#     claim["documentID"] = urls_with_id[claim["claimReview"][0]["url"]]


# with open("../data/november_until_now.json","w") as file:
#     json.dump(data,file)
