
import streamlit as st
import pandas as pd
import pydeck as pdk
from scraper_urbania import scrape_data

st.set_page_config(page_title="Proyectos Inmobiliarios en Lima", layout="wide")

st.title("🏠 Proyectos Inmobiliarios en Lima (Urbania)")
st.markdown("Consulta proyectos nuevos de Urbania directamente desde el mapa.")

with st.spinner("Obteniendo datos de Urbania..."):
    df = scrape_data()

if df.empty:
    st.warning("No se encontraron datos.")
else:
    st.success(f"{len(df)} proyectos encontrados")

    zonas = df["distrito"].dropna().unique().tolist()
    zona_seleccionada = st.sidebar.selectbox("Filtrar por zona:", ["Todas"] + zonas)

    if zona_seleccionada != "Todas":
        df = df[df["distrito"] == zona_seleccionada]

    st.map(df[["lat", "lon"]].dropna())

    st.dataframe(df.drop(columns=["lat", "lon"]))
