import requests
from requests.auth import HTTPBasicAuth

url = "https://unit2023.flexibee.eu/c/company6/faktura-prijata/289.json"

user = 'c6.user4',
password = 'c6.user4.flexi'

r = requests.get(url, auth=HTTPBasicAuth('c6.user4', 'c6.user4.flexi'))
data = r.json()

print(data)