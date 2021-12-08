import json
import requests as req
json





links = []
final_urls = []
for link in links:
    res = req.get(link)
    final_urls.append(res.url)

