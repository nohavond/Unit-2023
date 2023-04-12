import json
import requests
import textdistance

def makeSaved(listIn, desc, firma, total, name):
    o = {}
    o["listIn"] = listIn
    o["desc"] = desc
    o["firma"] = firma
    o["total"] = total
    o["name"] = name
    return json.dumps(o)

def makeDesc(o, id):
    l0 =[]
    suma = 0
    for i in o["listIn"]:
        if (i.typ == "procento"):
            i.cena = i.hodnota * o["total"]
            suma += i.cena
        elif (i.typ == "absolutni"):
            i.cena = i.hodnota
            suma += i.cena
    for i in o["listIn"]:
        if (i.typ == "zbytek"):
            i.cena = o["total"]-suma
    for i in o["listIn"]:
        o = {
                    "mnozMj": 1,
                    "cenaMj":  i.cena,
                    "typSzbDphK": "typSzbDph.dphOsv",
                    "kopStred": False,
                    "stredisko": i.id
                },
        l0.append(o)
    l = [{"id": id},{"bezPolozek": False},{"polozkyFaktury@removeAll": True}, {"polozkyFaktury":l0}]
    r = {"winstrom": {"faktura-prijata" : l, "@version" : "1.0"}}
    return r

def makeObjFromDesc(o):
    r = {"winstrom": o["winstrom"]}
    return r

def sendObj(o):
    url = "https://unit2023.flexibee.eu/v2/c/company6/faktura-prijata"
    requests.post(url, json=json.dumps(o))

def getDistance(string1, string2):
    return textdistance.damerau_levenshtein.normalized_distance(string1,string2)