from bs4 import BeautifulSoup
import json
from tldextract import extract
import os



with open("pages/logs.json","r") as logs_file:
    collected_articles = json.load(logs_file)

# data = []




    



# with open("../../data/links.json","r") as links_file:
#     documents = json.load(links_file)




# for i,doc in enumerate(documents):
#         for link in doc["links"]:
#             if link in collected_articles:
#                 splited_link = link.split("/")
#                 data.append(
#                     {
#                         "doc":doc["ID"],
#                         "url":link,
#                         "pageFile":f"{doc['ID']}-{splited_link[-1] if splited_link[-1] != '' else splited_link[-2]}.html"
#                     }
#                 )



# with open("pages/data.json","w") as outfile:
#     print(len(data))
#     json.dump(data,outfile)

data = []
# collected_articles = os.listdir("pages/")



with open("pages/data.json","r") as data_file:
    data = json.load(data_file)

# count = 0
# index = 0
# for page in data:

#     if count % 200 :
#         print(count)
#     if page["pageFile"] in collected_articles:
#         with open(f"pages/{page['pageFile']}","r") as file:
#             soup = BeautifulSoup(file,features="lxml")
#             title = soup.find("title")
#             # print("title : ", title)
#             try:
#                 if title.text == "Attention Required!":
#                     count += 1
#                     page["isCapatcha"] = True
#                 else:
#                     page["isCapatcha"] = False
#                 # else :
#                 #     link = soup.find("link",{"rel":"alternate"})
#                 #     if link:
#                 #         pass # print(link)
#                 #     else:
#                 #         print(page)
#             except:
#                 page["isCapatcha"] = False
#     else:
#         page["isCapatcha"] = True
#     index += 1

# print("total of Capatcha pages : ",count)

new_data = []
collected_articles = os.listdir("pages/")
files = map(lambda x: x["pageFile"],data)
count = 0
for page in collected_articles:
    if page not in files:
        os.remove(f"pages/{page}")
        count += 1

print("total files deleted : ",count," deleted successfully !")

    





