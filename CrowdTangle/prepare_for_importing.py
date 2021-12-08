import json



# IMPORTING POSTS
# with open("./data/posts.json","r") as file:
#     posts = json.load(file)


# new_data = list(map(lambda x: {"metadata":x,"id":x["platformId"]},posts))


# with open("./data/posts_import.json","w") as out_file:
#     json.dump(new_data,out_file)

# IMPORTING FACT CHECKS

with open("./data/fact_checks.json","r") as file:
    fact_checks = json.load(file)

valid_fact_checks = list(filter(lambda x: x["factCheck"],fact_checks))

new_data = []
for fact_check in valid_fact_checks:
    for claim in fact_check["factCheck"]["claims"]:
        matchs = list(filter(lambda x: x["metadata"]["text"] == claim["text"],new_data))
        if len(matchs) == 0:
            new_data.append({
                "post":fact_check["platformId"],
                "metadata":claim
            })
        else:
            for match in matchs:
                match["post"] += "," + fact_check["platformId"]
        

print(new_data[89])

with open("./data/fact_checks_import.json","w") as out_file:
    json.dump(new_data,out_file)
