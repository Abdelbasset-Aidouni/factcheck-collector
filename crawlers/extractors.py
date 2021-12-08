from bs4 import BeautifulSoup
import json
from readability import Document



class Extractor():

    def __init__(self,file_id,site):
        self.file_id = file_id
        self.site = site

    def get_soup(self):
        with open(f"../new_pages/{self.site}/{self.file_id}.html","r") as file:
            self.file = file
            soup = BeautifulSoup(Document(self.file.read()).summary(),features="lxml")
        return soup


    def extract_links(self):
        return self.exauhstive_extraction()

    def exauhstive_extraction(self):
        soup = self.get_soup()
        anchors = soup.find_all("a")
        links = [x.get("href",None) for x in anchors] if anchors else []
        return links


    def serialize(self):
        return {
            "ID":self.file_id,
            "site":self.site,
            "links": self.extract_links()
        }


class AFPExtractor(Extractor):

    def extract_links(self):
        soup = self.get_soup()
        scripts = soup.find_all("script",type="application/ld+json")
        data = json.loads(scripts[0])
        link = data["@graph"][0]["itemReviewed"].get("url")
        return [link]

class FactlyExtractor(Extractor):

    def extract_links(self):
        soup = self.get_soup()
        post_content = soup.select_one(".post-content")
        anchors = post_content.find_all("a")
        links = [x['href'] for x in anchors] if anchors else []
        return links

        

class PolitifactExtractor(Extractor):

    def extract_links(self):
        soup = self.get_soup()
        sources_content = soup.find(id="sources")
        anchors = sources_content.find_all("a")
        links = [x["href"] for x in anchors] if anchors else []
        return links

class TwentyMinutesExtractor(Extractor):

    def extract_links(self):
        soup = self.get_soup()
        wrapper = soup.select_one(".lt-endor-body.content")
        anchors = wrapper.find_all("a")
        links = [x['href'] for x in anchors] if anchors else []
        return links

class SnopesExtractor(Extractor):

    def extract_links(self):
        soup = self.get_soup()
        wrapper = soup.select_one(".snopes-post .content")
        anchors = wrapper.find_all("a")
        links = [x['href'] for x in anchors] if anchors else []
        return links


class SitesMapper():
    SITES_MAPPING = {
        "factly.in":FactlyExtractor,
        "20minutes.fr":TwentyMinutesExtractor,
        "politifact.com":PolitifactExtractor,
        "factcheck.afp.com":AFPExtractor,
        "snopes.com": SnopesExtractor
    }

    @classmethod
    def map_site(self,site):
        return SitesMapper.SITES_MAPPING.get(site,Extractor)
