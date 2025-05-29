
import streamlit as st
import pandas as pd
import pydeck as pdk
import json

st.set_page_config(page_title="Proyectos Inmobiliarios - Urbania", layout="wide")

st.title("🏘️ Proyectos Inmobiliarios en Lima")
st.markdown("Visualiza propiedades reales de Urbania (datos actualizados por scraping externo).")

try:
    with open("urbania_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
except:
    st.error("No se pudo cargar el archivo de datos.")
    st.stop()

if df.empty:
    st.warning("No hay datos disponibles.")
else:
    zonas = df["distrito"].dropna().unique().tolist()
    zona_seleccionada = st.sidebar.selectbox("Filtrar por zona:", ["Todas"] + zonas)

    if zona_seleccionada != "Todas":
        df = df[df["distrito"] == zona_seleccionada]

    st.map(df[["lat", "lon"]].dropna())
    st.dataframe(df.drop(columns=["lat", "lon"]))
