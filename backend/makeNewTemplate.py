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

def sendDesc(o, id, auth):
    return sendObj(makeDesc(o, id), auth)

def makeDesc(o, id):
    l0 =[]
    l1 = []
    for v in o["listIn"]:
        o1 = {}
        o1["hodnota"] = v[0]
        o1["typ"] = v[1]
        o1["id"] = v[2]
        o1["cena"] = 0
        l1.append(o1)
    suma = 0
    for i in l1:
        if (i['typ'] == "procento"):
            i["cena"] = i["hodnota"] * o["total"]
            suma += i["cena"]
        elif (i['typ'] == "absolutni"):
            i["cena"] = i["hodnota"]
            suma += i["cena"]
    for i in l1:
        if (i['typ'] == "zbytek"):
            i["cena"] = o["total"]-suma
    for i in l1:
        o = {
                    "mnozMj": 1,
                    "cenaMj":  i["cena"],
                    "typSzbDphK": "typSzbDph.dphOsv",
                    "kopStred": False,
                    "stredisko": i["id"]
                },
        l0.append(o)
    l = [{"id": id},{"bezPolozek": False},{"polozkyFaktury@removeAll": True}, {"polozkyFaktury":l0}]
    r = {"winstrom": {"faktura-prijata" : l, "@version" : "1.0"}}
    return r

def sendObj(o,auth):
    url = f"https://unit2023.flexibee.eu/v2/c/company6/faktura-prijata.json?authSessionId={auth}"
    return requests.post(url, json=json.dumps(o))

def getDistance(string1, string2):
    return textdistance.damerau_levenshtein.normalized_distance(string1,string2)

if __name__ == "__main__":
    values = [[(10, "procento", "k")], [(0, "zbytek", "k1")]]
    l = []
    for vs in values:
        for v in vs:
            l.append(v)
    s = makeSaved(l, "d", "c", 1000, "")
    r = sendDesc(json.loads(s),290,"")
