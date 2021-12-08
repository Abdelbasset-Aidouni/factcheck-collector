from urllib.request import Request,urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup

site = "https://www.politifact.com/factchecks/list"
url = site
articles_count = 0
hdr = {'User-Agent': 'Mozilla/5.0'}


for _ in range(1000):  
    print(f"============\nrequest {_} : target => {url}")
    print(f"Actual Count : {articles_count}\n=============")

    req = Request(url,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)
    articles_count += len(soup.find_all('li', {"class":"o-listicle__item"}))
    next_page = soup.find("a",string="Next")
    if not next_page:  # no 3rd link
        break
    url = urljoin(site, next_page['href'])

print("total articles : ",articles_count)
    
          
    