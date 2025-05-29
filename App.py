import streamlit as st
import pandas as pd
import pydeck as pdk
from urbania import get_urbania_data
from adondevivir import get_adondevivir_data
from properati import get_properati_data

st.set_page_config(page_title="Proyectos Inmobiliarios en Lima", layout="wide")
st.title("🏗️ Mapa de Proyectos Inmobiliarios Reales en Lima (2025)")

st.markdown("""
Esta herramienta visualiza proyectos inmobiliarios reales en distritos de alto nivel adquisitivo en Lima. 
Los datos son obtenidos automáticamente desde Urbania, Adondevivir y Properati.
""")

with st.spinner("📡 Obteniendo datos reales..."):
    urbania_df = get_urbania_data()
    adondevivir_df = get_adondevivir_data()
    properati_df = get_properati_data()

# Unir datos y limpiar
all_data = pd.concat([urbania_df, adondevivir_df, properati_df], ignore_index=True)
all_data.drop_duplicates(subset=["nombre", "distrito", "lat", "lon"], inplace=True)

# Filtro por distritos premium
distritos_permitidos = ["San Isidro", "Miraflores", "Barranco", "La Molina", "San Borja", "Santiago de Surco"]
all_data = all_data[all_data["distrito"].isin(distritos_permitidos)]

# Sidebar de filtros
with st.sidebar:
    st.header("Filtros")
    tipo_filtro = st.multiselect("Tipo de propiedad", options=sorted(all_data["tipo"].unique()), default=list(all_data["tipo"].unique()))
    distrito_filtro = st.multiselect("Distrito", options=distritos_permitidos, default=distritos_permitidos)

filtro_data = all_data[(all_data["tipo"].isin(tipo_filtro)) & (all_data["distrito"].isin(distrito_filtro))]

# Mapa interactivo
st.subheader("📍 Proyectos Inmobiliarios en Mapa")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=-12.1,
        longitude=-77.03,
        zoom=11,
        pitch=40,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=filtro_data,
            get_position='[lon, lat]',
            get_color='[0, 100, 250, 160]',
            get_radius=80,
        )
    ]
))

# Tabla
st.subheader("📄 Lista de Proyectos Inmobiliarios")
st.dataframe(filtro_data[["nombre", "empresa", "tipo", "distrito", "avance", "precio"]].reset_index(drop=True))