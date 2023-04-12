import streamlit as st
from reuest import *
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib3
from urllib.parse import urlparse, parse_qs
import html.parser

hostName = "localhost"
serverPort = 3000

# Title
st.title("Faktury")
faktura_id = st.experimental_get_query_params()["objectId"][0]

try:
    item = get_item(f"https://unit2023.flexibee.eu/c/company6/faktura-prijata/{faktura_id}.json?detail=full")
except:
    st.error("Faktura nebyla nalezena")
    item = []

castka = 0
for i in item:
    info = get_info(i)
    st.subheader(f"Faktura {info[0]}")
    castka = float(info[1])

    st.text(f"Částka: {info[1]}")
    st.text(info[2])
    st.text(f"Popis: {info[3]}")


@st.cache_data
def load_departments():
    dictionary = {}
    departments = get_departments()
    for department in departments:
        dictionary[department['nazev']] = department['id']
    options = [departments[0]['nazev'], departments[1]['nazev'], departments[2]['nazev'], departments[3]['nazev']]
    return options, dictionary


options, departments = load_departments()

selected_options = st.multiselect('Vyberte střediska', options)


# creates sliders for every stredisko
def create_strediska(opt, remaining_price):
    for i in opt:
        if (remaining_price > 0):
            val = st.slider(f"Vyberte částku pro středisko {i}", float(0), max_value=remaining_price, key={i})
            remaining_price -= val
    return remaining_price


remaining_price = create_strediska(selected_options, castka)
if remaining_price == 0:
    if st.button("Udělat vyúčtování"):
        st.success("Vyúčtování odesláno.")
else:
    st.alert("Nerozdělili jste celou částku.")

