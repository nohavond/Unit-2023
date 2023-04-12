import requests
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
import json


class RuleFinder:
  auth = HTTPBasicAuth('c6.user3', 'c6.user3.flexi')
  def post_rule(self, json_to_put, name, direct_rule=False):
    if not direct_rule:
      r = requests.get("https://unit2023.flexibee.eu/v2/c/company6/global-store/47.json?detail=full", auth=self.auth)
      r = r.json()
      r = r["winstrom"]["global-store"][0]
      print(r)
      name= name+r["hodnota"]

      to_put = {
        "winstrom": {
          "@version": "1.0",
          "global-store": [
            {
              "id": "key:uc-index",
              "hodnota": int(r["hodnota"])+1
            }
          ]
        }
      }
      r = requests.post("https://unit2023.flexibee.eu/v2/c/company6/global-store", json=to_put, auth=self.auth)
    else:
      name="direct-"+name
    to_put = {
      "winstrom": {
        "@version": "1.0",
        "global-store": [
          {
            "id":"key:"+"uc-"+name,
            "hodnota": str(json_to_put)
          }
        ]
      }
    }
    print(to_put)
    r=requests.post("https://unit2023.flexibee.eu/v2/c/company6/global-store", json=to_put, auth=self.auth)

    return r

  def get_rule(self, name, price):
    r= requests.get("https://unit2023.flexibee.eu/v2/c/company6/global-store.json?detail=full", auth=self.auth)
    indirect_rules = []
    r = r.json()
    for a in r['winstrom']['global-store']:
      if a["klic"] == "uc-direct-"+name:
        hodnota = a["hodnota"].replace("'", '"')
        hodnota=json.loads(hodnota)
        return hodnota
      if  "uc-"+name in a["klic"]:
        hodnota = a["hodnota"].replace("'", '"')
        hodnota=json.loads(hodnota)
        indirect_rules.append(hodnota)

    if len(indirect_rules)>0:
      indirect_rules.sort(key=lambda x:abs(x["price"]-price))
      print("gihjo")
      return indirect_rules[0]
    return None


r = RuleFinder()
print(r.post_rule({"sg":90, "price":2000}, "i"))
print(r.post_rule({"sgsg":90, "price":200}, "ii"))
print(r.post_rule({"sger":90, "price":200530}, "ii"))
print(r.get_rule("ii", 23555))
#r.get_rule("try")
auth = HTTPBasicAuth('c6.user3', 'c6.user3.flexi')
response = requests.get("https://unit2023.flexibee.eu/v2/c/company6/global-store.json?detail=full", auth=auth)
print(response.json())