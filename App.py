import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Título
st.set_page_config(page_title="Proyectos Inmobiliarios Premium", layout="wide")
st.title("🏠 Proyectos Inmobiliarios Premium en Lima")
st.markdown("Consulta proyectos inmobiliarios **actualizados y reales** desde el mapa y tabla interactiva.")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Filtro por distrito
distritos = df["distrito"].unique()
distrito_sel = st.selectbox("Selecciona un distrito:", sorted(distritos))

df_filtrado = df[df["distrito"] == distrito_sel]

# Mostrar mapa
m = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=15)
for _, row in df_filtrado.iterrows():
    popup = folium.Popup(f"<b>{row['nombre']}</b><br>Precio: {row['precio']}<br><a href='{row['enlace']}' target='_blank'>Ver propiedad</a>", max_width=300)
    folium.Marker(location=[row["lat"], row["lon"]], popup=popup, icon=folium.Icon(color="blue")).add_to(m)

st.subheader("📍 Mapa Interactivo")
st_folium(m, width=900, height=500)

# Mostrar tabla
st.subheader("📋 Detalles de propiedades")
st.dataframe(df_filtrado[["nombre", "precio", "habitaciones", "área_m2", "tipo", "enlace"]], use_container_width=True)