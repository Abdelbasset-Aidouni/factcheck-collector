from collector import GoogleAPICollector
import datetime
import json

import uuid

from itertools import chain
from sources import FACT_CHECK_DOMAINS,new_domains,NONE_VERIFIED_FACT_CHECK_DOMAINS

# date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30 * 6)


collector = GoogleAPICollector()
# all_domains = []
# all_domains.extend(FACT_CHECK_DOMAINS,new_domains,NONE_VERIFIED_FACT_CHECK_DOMAINS)

# all_domains = list(set(chain(FACT_CHECK_DOMAINS,new_domains,NONE_VERIFIED_FACT_CHECK_DOMAINS)))

# l = []
# for domain in all_domains:
#     l.append({
#         "site":domain,
#         "includedInGoogle": collector.included_in_google(domain)
#     })

# print(l)


data = []
with open("../../data/google.json",'r') as infile:
    old_data = json.load(infile)
    data.extend(old_data)


unique_records = {x["claimReview"][0]["url"]:{"url":x["claimReview"][0]["url"]} for x in data}
for url in unique_records.values():
    url["ID"] = uuid.uuid4().hex

for claim in data:
    claim["documentID"] = unique_records[claim["claimReview"][0]["url"]]["ID"]

with open('../../data/google.json', 'w') as outfile:
    json.dump(data, outfile)



# collector.filter_results(date_gte=date)

# with open("../../data/google.json","r") as data:
#             claims = json.load(data)



domains = [
    "factcheck.afp.com",
    "20minutes.fr",
    "apnews.com",
    "africacheck.org",
    "piaui.folha.uol.com.br",
    "animalpolitico.com",
    "aosfatos.org",
    "aap.com.au",
    "boomlive.in",
    "boliviaverifica.bo",
    "correctiv.org",
    "checkyourfact.com",
    "chequeado.com",
    "colombiacheck.com",
    "congocheck.net",
    "cotejo.info",
    "delfi.lt",
    "demagog.org.pl",
    "demagog.cz",
    "dubawa.org",
    "efe.com",
    "ecuadorchequea.com",
    "ellinikahoaxes.gr",
    "politica.estadao.com.br",
    "factly.in",
    "factcheck.org",
    "factcheckni.org",
    "ghanafact.com",
    "faktograf.hr",
    "faktoje.al",
    "fatabyyano.net",
    "theferret.scot",
    "observers.france24.com",
    "fullfact.org",
    "factcheck.ge",
    "larepublica.pe",
    "istinomer.rs",
    "news.jtbc.joins.com",
    "kompas.com",
    "kallxo.com",
    "kallkritikbyran.se",
    "lasillavacia.com",
    "lemonde.fr",
    "logically.ai",
    "mafindo.or.id",
    "maharat-news.com",
    "maldita.es",
    "mygopen.com",
    "mdfgeorgia.ge",
    "newsmobile.in",
    "newschecker.in",
    "newtral.es",
    "observador.pt",
    "pagellapolitica.it",
    "15min.lt",
    "poligrafo.sapo.pt",
    "abc.net.au",
    "rappler.com",
    "raskrinkavanje.ba",
    "realornotmm.info",
    "reutersagency.com",
    "sciencefeedback.co",
    "digiteye.in",
    "southasiacheck.org",
    "stopfake.org",
    "stopfals.md",
    "indiatoday.in",
    "tempo.co",
    "thedispatch.com",
    "thip.media",
    "thequint.com",
    "washingtonpost.com",
    "thewhistle.globes.co.il",
    "thejournal.ie",
    "tjekdet.dk",
    "usatoday.com",
    "vishvasnews.com",
    "vistinomer.mk",
    "voxukraine.org",
    "youturn.in",
    "dpa.com",


    "liputan6.com",
    "suara.com",
    "raskrinkavanje.me",
    "dogrulukpayi.com",
    "factcheck.kz",
    "faktisk.no",
    "knack.be",
    "liberation.fr",
    "mafindo.or.id",
    "mdfgeorgia.ge",
    "pesacheck.org",
    "rebaltica.lv",
    "tfc-taiwan.org.tw",
    "tirto.id",
    "apublica.org",
    "altnews.in",
    "dn.se",
    "factchecker.in",
    "lavoce.info",
    "nu.nl",
    "nieuwscheckers.nl",
    "politifact.com",
    "snopes.com",
    "theconversation.com",
    "weeklystandard.com",
    "metromode.se"
]

NONE_VERIFIED_DOMAINS = [
    "liputan6.com",
    "suara.com",
    "raskrinkavanje.me",
    "dogrulukpayi.com",
    "factcheck.kz",
    "faktisk.no",
    "knack.be",
    "liberation.fr",
    "mafindo.or.id",
    "mdfgeorgia.ge",
    "pesacheck.org",
    "rebaltica.lv",
    "tfc-taiwan.org.tw",
    "tirto.id",
    "apublica.org",
    "altnews.in",
    "dn.se",
    "factchecker.in",
    "lavoce.info",
    "nu.nl",
    "nieuwscheckers.nl",
    "politifact.com",
    "snopes.com",
    "theconversation.com",
    "weeklystandard.com",
    "metromode.se"
]



