import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Título principal
st.set_page_config(page_title="LimaProp - Proyectos Inmobiliarios", layout="wide")
st.title("🏠 LimaProp - Proyectos Inmobiliarios en Lima")
st.markdown("Explora proyectos inmobiliarios nuevos en Lima con filtros interactivos.")

# Cargar datos JSON
try:
    df = pd.read_json("data_urbania.json")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Verificar columnas requeridas
required_columns = {'nombre', 'distrito', 'lat', 'lon', 'link'}
if not required_columns.issubset(df.columns):
    st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: {required_columns}\nColumnas actuales: {set(df.columns)}")
    st.stop()

# Filtrar por distrito
distritos = sorted(df['distrito'].unique())
distrito_seleccionado = st.selectbox("Selecciona un distrito:", ["Todos"] + distritos)

if distrito_seleccionado != "Todos":
    df = df[df['distrito'] == distrito_seleccionado]

# Mostrar tabla
st.subheader("📋 Lista de Proyectos")
st.dataframe(df[['nombre', 'distrito', 'link']], use_container_width=True)

# Mapa
st.subheader("🗺️ Mapa de Proyectos Inmobiliarios")

if not df.empty:
    m = folium.Map(location=[-12.0464, -77.0428], zoom_start=12)
    for _, row in df.iterrows():
        popup_html = f"<b>{row['nombre']}</b><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>"
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=popup_html,
            tooltip=row['nombre'],
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(m)
    st_folium(m, width=700, height=500)
else:
    st.info("No hay proyectos disponibles para el distrito seleccionado.")
