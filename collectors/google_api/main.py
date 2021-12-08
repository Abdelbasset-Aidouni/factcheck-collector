import json
from itertools import chain
from collector import GoogleAPICollector
# from sources import NEWS_DOMAINS, FACT_CHECK_DOMAINS
from sources import FACT_CHECK_DOMAINS, COVID19_DOMAINS, NONE_VERIFIED_FACT_CHECK_DOMAINS, NEW_DOMAINS, new_domains
import datetime
# NEW_DOMAINS = [
#     'kompas.com',
#  'rebaltica.lv',
#  'teyit.org',
#  'chequeado.com',
#  'delfi.lt',
#  'southasiacheck.org',
#  'apublica.org',
#  'ostro.si',
#  'liputan6.com',
#  'metromode.se',
#  'tirto.id',
#  'realornotmm.info',
#  '15min.lt',
#  'factly.in',
#  'francetvinfo.fr',
#  'digiteye.in',
#  'faktoje.al',
#  'thequint.com',
#  'verificat.cat',
#  'stopfals.md',
#  'raskrinkavanje.me',
#  'congocheck.net',
#  'pesacheck.org',
#  'ghanafact.com',
#  'fatabyyano.net',
#  'mafindo.or.id',
#  'reutersagency.com',
#  'factcheck.ge',
#  'lavoce.info',
#  'ecuadorchequea.com',
#  'kallkritikbyran.se',
#  'fact-checkghana.com',
#  'weeklystandard.com',
#  'demagog.cz',
#  'voxukraine.org',
#  'news.jtbc.joins.com',
#  'dogrulukpayi.com',
#  'factcheck.kz',
#  'logically.ai',
#  'observers.france24.com',
#  'faktisk.no',
#  'tempo.co',
#  'maharat-news.com',
#  'lasillavacia.com',
#  'dpa.com',
#  'istinomjer.ba',
#  'mdfgeorgia.ge',
#  'larepublica.pe',
#  'apnews.com',
#  'newsmeter.in',
#  'knack.be',
#  'suara.com',
#  'dn.se',
#  'boliviaverifica.bo',
#  'thedispatch.com',
#  'cotejo.info',
#  'nieuwscheckers.nl',
#  'tfc-taiwan.org.tw',
#  'factcrescendo.com',
#  'rappler.com',
#  'politica.estadao.com.br',
#  'factchecker.in',
#  'nu.nl',
#  'raskrinkavanje.ba'
# ]


with open("../../fact_checkers.json","r") as file:
    fact_checkers = json.load(file)
print(len(set(chain(FACT_CHECK_DOMAINS, COVID19_DOMAINS, NONE_VERIFIED_FACT_CHECK_DOMAINS, NEW_DOMAINS, new_domains))))

fact_checkers_domains = [x["domain"] for x in fact_checkers]
print(len(set(fact_checkers_domains)))
# for f in set(fact_checkers_domains):
#     if f not in set(chain(FACT_CHECK_DOMAINS, COVID19_DOMAINS, NONE_VERIFIED_FACT_CHECK_DOMAINS, NEW_DOMAINS, new_domains)):
#         print(f)

# max_age = datetime.datetime.now() - datetime.datetime(2020,11,10)

# collector = GoogleAPICollector()
# data = []
# crawled_domains = set(chain(FACT_CHECK_DOMAINS, COVID19_DOMAINS, NONE_VERIFIED_FACT_CHECK_DOMAINS, NEW_DOMAINS, new_domains))
# for domain in set(fact_checkers_domains):
    
    
#     if domain not in crawled_domains:
#         results = collector.filter_by_source(domain,page_size=9000,follow_next=True)
#         print({
#             'domain':domain,
#             'length' :len(results)
#             })
#         data.extend(results)
#         print("total claims collected : ",len(data))

# with open("../../data/fact_checks_bis.json",'r') as infile:
#     old_data = json.load(infile)
#     data.extend(old_data)

# with open('../../data/fact_checks_bis.json', 'w') as outfile:
#     json.dump(data, outfile)


