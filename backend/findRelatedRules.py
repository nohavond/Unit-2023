import requests
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
import json
import textdistance


class RuleFinder:
  auth = HTTPBasicAuth('c6.user3', 'c6.user3.flexi')

  def post_rule_interface(self, template):

    if template["name"]!="":
      return self.post_rule(template, template["name"], template["id"], True)
    return self.post_rule(template, template["firma"], template["id"])

  def post_rule(self, json_to_put, name, id, direct_rule=False):
    if not direct_rule:
      name= name+str(id)
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
    print(r)
    return r

  def get_rule(self, name, price):
    r= requests.get("https://unit2023.flexibee.eu/v2/c/company6/global-store.json?detail=full&limit=0", auth=self.auth)
    indirect_rules = []
    r = r.json()
    for a in r['winstrom']['global-store']:
      print(a["klic"])
      if a["klic"] == "uc-direct-"+name:
        hodnota = a["hodnota"].replace("'", '"')
        hodnota=json.loads(hodnota)
        return hodnota
      if  "uc-"+name == a["klic"][0:len(name)+3]:
        hodnota = a["hodnota"].replace("'", '"')
        hodnota=json.loads(hodnota)
        indirect_rules.append(hodnota)

    if len(indirect_rules)>0:
      indirect_rules.sort(key=lambda x:abs(x["total"]-price))
      return indirect_rules[0]


    return None


r = RuleFinder()
#r.post_rule_interface({"total":579, "id":987, "firma":"a","name":"" })
print(r.get_rule("j", 23555))
#r.get_rule("try")
auth = HTTPBasicAuth('c6.user3', 'c6.user3.flexi')
response = requests.get("https://unit2023.flexibee.eu/v2/c/company6/global-store.json?detail=full", auth=auth)
print(response.json())