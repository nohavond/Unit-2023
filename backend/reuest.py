import requests
from requests.auth import HTTPBasicAuth


def get_item(url):
    item = requests.get(url, auth=HTTPBasicAuth('c6.user4', 'c6.user4.flexi'))
    item = item.json()['winstrom']['faktura-prijata']
    return item


def get_info(item):
    return [item['id'], item['sumZklCelkem'], item['firma@showAs'], item['popis']]


def get_departments():
    url_department = "https://unit2023.flexibee.eu/c/company6/stredisko.json"
    departments = requests.get(url_department, auth=HTTPBasicAuth('c6.user4', 'c6.user4.flexi'))
    departments = departments.json()['winstrom']['stredisko']
    return departments

