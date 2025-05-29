# App.py - Versión Premium Completa

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Título y descripción
st.set_page_config(page_title="Inmuebles Lima Premium", layout="wide")
st.title("🏡 Proyectos Inmobiliarios en Lima")
st.markdown("Consulta proyectos inmobiliarios con mapa interactivo y búsqueda avanzada por zonas.")

# Cargar los datos
try:
    df = pd.read_json("data_urbania.json")
    required_cols = {'nombre', 'distrito', 'lat', 'lon', 'link'}
    if not required_cols.issubset(set(df.columns)):
        st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: `{required_cols}`\nColumnas actuales: {df.columns.tolist()}")
        st.stop()
except Exception as e:
    st.error("Error al cargar los datos: " + str(e))
    st.stop()

# Filtros
distritos = df["distrito"].unique().tolist()
distrito_seleccionado = st.selectbox("Filtrar por distrito", ["Todos"] + distritos)

busqueda = st
