import streamlit as st
from faker import Faker
import pandas as pd
from streamlit_extras.no_default_selectbox import selectbox

st.set_page_config(
    page_title="FAKER DATA",
    page_icon="assets/favicon.ico",
    layout="wide"
)

st.title(":orange[FAKER DATA GENERATOR]")
st.divider()

with st.sidebar:
    st.subheader("Configura tu Faker Data")

    localization = selectbox(
        "Idioma",
        options=[
            "en_US",
            "es_ES",
            "es_PA",
            "fr_FR",
            "it_IT",
            "pt_BR"
        ]
    )

    num_fields = st.number_input("Cantidad de campos", min_value=1, max_value=7, step=1)
    num_rows = st.number_input("Cantidad de filas", min_value=1, max_value=1000, step=1)

    fake = Faker(localization)

    faker_options= {
        "Name": fake.name,
        "Email": fake.email,
        "address": fake.address,
        "Phone Number": fake.phone_number,
        "job": fake.job,
        "company": fake.company,
        "Birth": fake.date_of_birth
    }    

    fields_selection = []
    st.write("Selecciona los campos: ")
    for i in range(num_fields):
        field = selectbox(f"Campo {i+1}", list(faker_options.keys()), key=f"id_{i}")
        fields_selection.append(field)

if st.button("Generar datos"):
    
    data = {field: [faker_options[field]() for _ in range(num_rows)] for field in fields_selection}
    data["id"] = list(range(1, num_rows +1))
    df = pd.DataFrame(data)
    colum_order = ["id"] + [col for col in df.columns if col != 'id']
    df = df[colum_order]

    st.write("Datos generados:")
    st.dataframe(df, hide_index=True)

    col1, col2, _ = st.columns([1,1,8])
    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="archivo.csv",
            mime="text/csv",
            type="primary"
        )

    with col2:
        json = df.to_json(
            orient="records",
            indent=4,
            force_ascii=False
        )
        st.download_button(
            label="Descargar JSON",
            data=json,
            file_name="archivo.json",
            mime="application/json",
            type="primary"
        )    
        