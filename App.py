
import streamlit as st
import pandas as pd
import pydeck as pdk
from scraper_urbania import scrape_urbania

st.set_page_config(layout="wide", page_title="Proyectos Inmobiliarios - Urbania (Perú)")

st.title("🏢 Proyectos Inmobiliarios en Lima - Datos Reales de Urbania")

# Extraer y mostrar datos reales
with st.spinner("Obteniendo datos de Urbania..."):
    df = scrape_urbania()

if df.empty:
    st.error("No se encontraron datos. Es posible que Urbania haya bloqueado el acceso o que no haya resultados.")
    st.stop()

# Filtro por distrito
st.sidebar.header("Filtros")
distritos = df["distrito"].dropna().unique().tolist()
seleccionados = st.sidebar.multiselect("Selecciona distritos:", distritos, default=distritos)
df_filtrado = df[df["distrito"].isin(seleccionados)]

# Mapa
st.subheader("📍 Mapa de proyectos")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=-12.1,
        longitude=-77.03,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_filtrado,
            get_position='[lon, lat]',
            get_color='[0, 100, 255, 160]',
            get_radius=80,
        ),
    ],
))

# Tabla
st.subheader("📋 Lista de proyectos")
st.dataframe(df_filtrado[['nombre', 'direccion', 'distrito', 'precio', 'dormitorios', 'area_m2', 'url']])
