import streamlit as st
from reuest import *

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
