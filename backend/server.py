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

try:
    item = get_item("https://unit2023.flexibee.eu/c/company6/faktura-prijata/289.json?detail=full")
except:
    st.error("Faktura nebyla nalezena")
    item = []

for i in item:
    info = get_info(i)
    st.subheader(f"Faktura {info[0]}")

    st.text(f"Částka: {info[1]}")
    st.text(info[2])
    st.text(f"Popis: {info[3]}")


def create_interface():
    departments = get_department()
    print(departments)

create_interface()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parse_result = urlparse(self.path)
        dict_result = parse_qs(parse_result.query)
        print(dict_result["objectId"])
        self.send_header('Location','http://localhost:8501')
        self.end_headers()

webServer = HTTPServer((hostName, serverPort), MyServer)
print("Server started http://%s:%s" % (hostName, serverPort))

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
print("Server stopped.")
