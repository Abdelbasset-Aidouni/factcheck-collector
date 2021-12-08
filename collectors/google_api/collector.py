import requests as req
import json
import datetime



GOOGLE_API_KEY = "AIzaSyCln7V1rTA-1Y06tq_Pg0NhUvlMzAMV0Tc"


class GoogleAPICollector():
    KEY = GOOGLE_API_KEY
    BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    DATA_SOURCE = "../../data/google.json"

    def execute(self,url):
        query = f"{url}&key={self.KEY}"
        return req.get(query)
    
    def filter_by_source(self,source,page_size=100,follow_next=False,max_age_days=None):
        parameter = f"reviewPublisherSiteFilter={source}"
        if page_size:
            parameter = f"{parameter}&pageSize={page_size}"
        if max_age_days:
            parameter = f"{parameter}&maxAgeDays={max_age_days}"
        if follow_next:
            add_next_token = lambda token: f"{parameter}&pageToken={token}"
            parameter_with_next = parameter
            results = []
            index = 1
            pageToken = "Initial"
            while True:
                print(f"Request >>>> {index} : publisher={source} | PageToken={pageToken}")
                res = self.execute(f"{self.BASE_URL}?{parameter_with_next}")
                res_json = res.json()
                if res_json :
                    if res_json.get("claims",None):
                        results.extend(res_json["claims"])
                    if res_json.get("nextPageToken",None) :
                        pageToken = res_json["nextPageToken"]
                        parameter_with_next = add_next_token(pageToken)
                        index += 1
                        continue
                    else:
                        return results
                else:
                    return results
        return self.execute(f"{self.BASE_URL}?{parameter}").json()


    def filter_results(self,date_gte=None,date_lte=None,target="../../data/google_filtered.json"):
        count = 0
        with open(self.DATA_SOURCE,"r") as data:
            claims = json.load(data)
            filtered_data = []
            for claim in claims:
                claimDate = claim.get("claimDate",claim.get("claimReview")[0].get('reviewDate'))
                date = datetime.datetime.strptime(claimDate, "%Y-%m-%dT%H:%M:%S%z")
                print(date)
                if count % 50 == 0:
                    print("count == ",count)
                if date_gte:
                    if date >= date_gte:
                        filtered_data.append(claim)
                        count += 1
                        continue
                if date_lte:
                    filtered_data.append(claim)
                    if date <= date_lte:
                        count += 1
                
            print("total count : ",count)
            with open(target, 'w') as outfile:
                json.dump(filtered_data, outfile)
    
    def included_in_google(self,source):
        if self.filter_by_source(source=source):
            return True
        return False


class GoogleExplorerAPICollector():
    BASE_URL = "https://toolbox.google.com/factcheck/api/search?hl=en&offset=0"
    DATA_SOURCE = "../../data/claims_with_tags.json"
    DATA_DIR = "../../data/explorer_claims"
    



    def execute(self,**params):
        return req.get(GoogleExplorerAPICollector.BASE_URL,params=params)
    


    def filter_by_source(self,source,num_results=1000,follow_next=False):
        parameters = {
            "num_results":num_results,
            "query":f"site:{source}"
        }
        
        
        results = []
        
        res = self.execute(**parameters)
        res_text = res.text[6:]
        res_json = json.loads(res_text)
        if res_json :
            # claims = res_json[0][1]
            # mid_mappings = res_json[0][2]
            with open(f"{GoogleExplorerAPICollector.DATA_DIR}/{source}.json","w") as target_file:
                json.dump(res_json,target_file)

            ## TODO
            # check for the next claims if they exists collect them
            return res_json[0][1]
        return []

## Response Structure

# data [
#     [
#         "claims_response",
#         ["CLAIMS"]
#     ]
# ]



