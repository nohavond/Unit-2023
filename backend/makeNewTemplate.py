import json
import requests
import textdistance
def makeObj(list):
    l0 =[]
    for i in list:
        o = {
                    "mnozMj": 1,
                    "cenaMj": i.cena,
                    "typSzbDphK": "typSzbDph.dphOsv",
                    "kopStred": False,
                    "stredisko": i.id
                },
        l0.append(o)
    l = [{"id": "123"},{"bezPolozek": False},{"polozkyFaktury@removeAll": True}, {"polozkyFaktury":l0}]
    r = {"winstrom" : {"faktura-prijata" : l, "@version" : "1.0"}}
    return r

def sendObj(o):
    url = "https://unit2023.flexibee.eu/v2/c/company6/faktura-prijata"
    requests.post(url, json=json.dumps(o))

def getDistance(string1, string2):
    return textdistance.damerau_levenshtein.normalized_distance(string1,string2)