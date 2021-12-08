
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datefinder import find_dates
import json



def normalize_review_date(text):
    return text[text.index("•")+1:]


site = "https://www.politifact.com"
data = []
for i in range(1,22):
    print("scrapping page =",i)
    with open(f"pages/latest/politifact/list/page_{i}.html","r") as page:
        soup = BeautifulSoup(page,features="lxml")
    articles = soup.find_all("article",{"class":"m-statement"})

    
    for article in articles:
        data.append({
            "publisher": article.find("a",{"class":"m-statement__name"}).text.strip(),
            "publishDate":next(find_dates(article.find("div",{"class":"m-statement__desc"}).text)).isoformat(' ', 'seconds'),
            "title":article.find("div",{"class":"m-statement__quote"}).find("a").text.strip(),
            "url":urljoin(site,article.find("div",{"class":"m-statement__quote"}).find("a")["href"]),
            "reviewDate":next(find_dates(normalize_review_date(article.find("footer",{"class":"m-statement__footer"}).text))).isoformat(' ', 'seconds'),
            "rating":article.find("img",{"class":"c-image__thumb"},alt=True)["alt"]
        })


with open("pages/latest/data v0.3.json","w+") as data_file:
    json.dump(data,data_file)