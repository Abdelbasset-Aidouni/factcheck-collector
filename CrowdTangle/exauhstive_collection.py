import datetime
import json
import time
import requests as req


API_KEY = "ATsTz4WEThZzv8XRew1B5g1sNH8NziJSnru7YeX5"


endpoint = "https://api.crowdtangle.com/posts"
search_terms = "politics,Politician,Political Party,Protest,Assault,Fraud,Liberalism,Democrats,Arrest,Liberal Democrats,Dark money,government,Bipartisan,Ideology,Left-wing,right-wing,far left,far right,partisanship,Campaign,News,Voting,elections,finance,economics,Vaccine,covid,health"


end_date = datetime.datetime(2021,3,24) - datetime.timedelta(days=30 * 14)


def collect_posts_between(start_date,end_date,offset=None,count=100):
    url = f"{endpoint}?token={API_KEY}&endDate={end_date.strftime('%Y-%m-%dT%H:%M:%S')}&startDate={start_date.strftime('%Y-%m-%dT%H:%M:%S')}&searchTerm={search_terms}&count={count}&language=en&types=link"
    results = []
    
    for i in range(200):
        print(f"request n° {len(results)/count + 1}")
        res = req.get(url)
        if res.status_code == 200:
            json_data = res.json()
            results.extend(json_data["result"]["posts"])
            if json_data["result"]["pagination"].get("nextPage",None):
                url = json_data["result"]["pagination"]["nextPage"]
                time.sleep(10)
            else:
                break
        else:
            print(f"ERROR: code {res.status_code}, response: {res.text}")
            break
    return results

def previous_month(date):
    return date - datetime.timedelta(days=30)

start_date = previous_month(end_date)
data = []
for i in range(3):
    print(f"collecting posts between {start_date} and {end_date}")
    data.extend(collect_posts_between(start_date,end_date))

    #SAVE THE COLLECTED POSTS
    with open("./data/posts_5.json","w") as outfile:
        json.dump(data,outfile)

    end_date = start_date
    start_date = previous_month(end_date)

# with open("./data/posts.json","w") as outfile:
#     json.dump(data,outfile)