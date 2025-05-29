App.py - Versión Premium Completa

import streamlit as st import pandas as pd from streamlit_folium import st_folium import folium import json

st.set_page_config(page_title="Viviendas Lima Premium", layout="wide")

Cargar los datos reales desde un archivo JSON

try: with open("data_urbania.json", "r", encoding="utf-8") as f: data = json.load(f) df = pd.DataFrame(data) except Exception as e: st.error(f"Error al cargar los datos: {e}") st.stop()

Validación de columnas necesarias

required_cols = {"nombre", "distrito", "lat", "lon", "link"} if not required_cols.issubset(set(df.columns)): st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: {required_cols}\nColumnas actuales: {set(df.columns)}") st.stop()

Sidebar - filtros

st.sidebar.image("assets/logo.png", use_column_width=True) st.sidebar.title("Filtros")

Filtro por distrito

distritos = sorted(df["distrito"].unique()) distritos_seleccionados = st.sidebar.multiselect("Selecciona distritos", distritos, default=distritos)

Filtro por búsqueda de nombre

busqueda = st.sidebar.text_input("Buscar por nombre del proyecto")

Aplicar filtros

df_filtrado = df[df["distrito"].isin(distritos_seleccionados)] if busqueda: df_filtrado = df_filtrado[df_filtrado["nombre"].str.contains(busqueda, case=False)]

Layout

st.title("🏠 Proyectos Inmobiliarios en Lima (Urbania)") st.markdown("Consulta proyectos nuevos directamente desde el mapa o por filtros.")

Mapa

m = folium.Map(location=[-12.1, -77.03], zoom_start=13) for _, row in df_filtrado.iterrows(): folium.Marker( location=[row["lat"], row["lon"]], tooltip=row["nombre"], popup=f"<a href='{row['link']}' target='_blank'>{row['nombre']}</a>", icon=folium.Icon(color="blue", icon="home") ).add_to(m)

st_data = st_folium(m, width=1000, height=600)

Tarjetas informativas en columnas

st.subheader("🔍 Proyectos disponibles") cols = st.columns(2) for i, (_, row) in enumerate(df_filtrado.iterrows()): with cols[i % 2]: st.markdown(f""" #### 🏢 {row['nombre']} 📍 {row['distrito']}
🔗 Ver en Urbania
""")

