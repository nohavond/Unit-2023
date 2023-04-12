import streamlit as st
from reuest import *
from makeNewTemplate import *
from findRelatedRules import RuleFinder

# Title
st.title("Rozúčtování")
faktura_id = st.experimental_get_query_params()["objectId"][0]
session = st.experimental_get_query_params()["authSessionId"]

try:
    item = get_item(f"https://unit2023.flexibee.eu/v2/c/company6/faktura-prijata/{faktura_id}.json?detail=full")
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

a = RuleFinder()

template_found = a.get_rule(info[2], info[1])
print(template_found)

if template_found is not None:
    st.info("Nalezli jsme již použitý template pro tuto firmu:")

selected_options = st.multiselect('Vyberte střediska', options)


def create_slider(remaining_price, i):
    st.subheader(f"Vyberte částku pro středisko {i}")
    options = ['Procenta', 'Absolutní hodnota', 'Zbytek ceny']
    option = st.radio("", options, key=i)
    if option == 'Procenta':
        val = st.slider(f"Vyberte částku pro středisko {i}", float(0), float(remaining_price * 100 / castka),
                        label_visibility='hidden')
        val = castka * val * 0.01
        st.write(f"Vybraná cena: {val}")
        popis = "procento"

    elif option == 'Absolutní hodnota':
        val = st.slider(f"Vyberte částku pro středisko {i}", float(0), max_value=remaining_price,
                        label_visibility='hidden')
        popis = "absolutni"

    else:
        val = st.slider(f"Vyberte částku pro středisko {i}", float(0), remaining_price, value=remaining_price,
                        label_visibility='hidden')
        popis = "zbytek"
    return val, popis, i


# creates sliders for every stredisko
def create_strediska(opt, remaining_price):
    values = []
    for i in opt:
        if remaining_price > 0:
            val, label, stredisko = create_slider(remaining_price, i)
            values.append((val, label, stredisko))
            remaining_price -= val
    return remaining_price, values


remaining_price, values = create_strediska(selected_options, castka)


def save_template():
    template = st.text_input("Zde napište název templatu...")
    l = []
    o = makeSaved(values, info[3], info[2], castka, template)
    sendDesc(json.loads(o), info[0], session)


if remaining_price == 0:
    if st.checkbox("Uložit template"):
        save_template()
        if st.button("Udělat vyúčtování"):
            st.success("Vyúčtování odesláno.")
    elif st.button("Udělat vyúčtování"):
        print(json.dumps(values))
        o = makeSaved(values, info[3], info[2], castka, "")
        sendDesc(json.loads(o), info[0], session)
        st.success("Vyúčtování odesláno.")
elif remaining_price != castka:
    st.warning("Nerozdělili jste celou částku.")
