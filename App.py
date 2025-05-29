
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="LimaProp Premium", layout="wide")

st.title("🏠 LimaProp Premium")
st.subheader("Explora proyectos inmobiliarios en tiempo real por distritos de Lima")

# Cargar datos reales
try:
    df = pd.read_json("data_urbania.json")
except Exception as e:
    st.error("Error al cargar los datos: " + str(e))
    st.stop()

if df.empty:
    st.warning("No se encontraron datos.")
    st.stop()

# Mostrar columnas disponibles (para debug)
# st.write("Columnas disponibles:", df.columns)

# Verificar columnas necesarias
required_columns = {"nombre", "distrito", "lat", "lon", "link"}
if not required_columns.issubset(df.columns):
    st.error("El archivo de datos no contiene todas las columnas necesarias.")
    st.write("Se requieren:", required_columns)
    st.write("Columnas actuales:", df.columns)
    st.stop()

# Selección de distrito
distritos = df["distrito"].unique().tolist()
distrito_seleccionado = st.selectbox("Selecciona un distrito", distritos)

df_filtrado = df[df["distrito"] == distrito_seleccionado]

# Mapa
m = folium.Map(location=[-12.1, -77.03], zoom_start=13)

for _, row in df_filtrado.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"<b>{row['nombre']}</b><br><a href='{row['link']}' target='_blank'>Ver propiedad</a>",
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(m)

st_folium(m, width=900, height=600)

# Tabla de resultados
st.subheader("Proyectos disponibles")
st.dataframe(df_filtrado[["nombre", "distrito", "link"]])
