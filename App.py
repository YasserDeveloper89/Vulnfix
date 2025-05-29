import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Cargar los datos
try:
    df = pd.read_json("data_urbania.json")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Verificación de columnas
required_columns = {'nombre', 'distrito', 'lat', 'lon', 'link'}
if not required_columns.issubset(df.columns):
    st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: {required_columns}\nColumnas actuales: {set(df.columns)}")
    st.stop()

# Interfaz
st.set_page_config(page_title="Proyectos Inmobiliarios Premium", layout="wide")
st.title("🏠 Proyectos Inmobiliarios Premium en Lima")
st.markdown("Consulta propiedades actualizadas en tiempo real. Selecciona un distrito para ver los proyectos disponibles.")

# Filtros
distritos = sorted(df["distrito"].unique())
distrito_seleccionado = st.selectbox("📍 Selecciona un distrito", distritos)

# Filtrar por distrito
df_filtrado = df[df["distrito"] == distrito_seleccionado]

# Mostrar mapa
if not df_filtrado.empty:
    m = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)

    for _, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            tooltip=row["nombre"],
            popup=f"<b>{row['nombre']}</b><br><a href='{row['link']}' target='_blank'>Ver en Urbania</a>",
            icon=folium.Icon(color="blue", icon="home"),
        ).add_to(m)

    st_data = st_folium(m, width=900, height=500)

    st.markdown("### 📋 Detalles del distrito seleccionado")
    st.dataframe(df_filtrado[["nombre", "link"]].rename(columns={
        "nombre": "Nombre del Proyecto",
        "link": "Enlace"
    }), use_container_width=True)
else:
    st.warning("No se encontraron proyectos para este distrito.")
