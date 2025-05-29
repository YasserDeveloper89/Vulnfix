import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load data
try:
    df = pd.read_json("data_urbania.json")
    required_columns = {'nombre', 'distrito', 'lat', 'lon', 'link'}
    if not required_columns.issubset(df.columns):
        st.error(f"El archivo de datos no contiene todas las columnas necesarias. Se requieren: {required_columns}. Columnas actuales: {df.columns.tolist()}")
        st.stop()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Sidebar
st.sidebar.title("LimaProp - Buscador Inmobiliario")
selected_district = st.sidebar.selectbox("Selecciona un distrito", sorted(df["distrito"].unique()))

# Main
st.title("🏠 Proyectos Inmobiliarios en Lima")
st.subheader("Proyectos disponibles en el distrito seleccionado")

filtered_df = df[df["distrito"] == selected_district]

# Mapa
map_center = [filtered_df["lat"].mean(), filtered_df["lon"].mean()]
m = folium.Map(location=map_center, zoom_start=14)
for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"<a href='{row['link']}' target='_blank'>{row['nombre']}</a>",
        tooltip=row["nombre"],
    ).add_to(m)
st_folium(m, width=700, height=500)

# Lista
st.markdown("### Lista de proyectos")
for _, row in filtered_df.iterrows():
    st.markdown(f"**{row['nombre']}**  
📍 {row['distrito']}  
🔗 [Ver proyecto]({row['link']})")