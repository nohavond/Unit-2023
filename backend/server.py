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

for i in item:
    info = get_info(i)
    st.subheader(f"Faktura {info[0]}")

    st.text(f"Částka: {info[1]}")
    st.text(info[2])
    st.text(f"Popis: {info[3]}")


@st.cache_data
def load_departments():
    departments = get_departments()
    options = [departments[0]['nazev'], departments[1]['nazev'], departments[2]['nazev'], departments[3]['nazev']]
    return options


selected_departments = st.selectbox("Výběr střediska:", load_departments())
