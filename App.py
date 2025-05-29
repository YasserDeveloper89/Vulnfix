import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(page_title="LimaProp", layout="wide")
st.title("🧭 LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios en Lima de forma interactiva.")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    required_columns = {"nombre", "distrito", "lat", "lon", "link", "precio", "tipo"}
    if not required_columns.issubset(df.columns):
        st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: {required_columns}\nColumnas actuales: {set(df.columns)}")
        st.stop()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Filtros
st.sidebar.header("🔎 Filtros")

# Filtro de distrito (multi selección)
distritos = sorted(df["distrito"].unique())
distritos_seleccionados = st.sidebar.multiselect("Selecciona distritos", distritos, default=distritos)

# Filtro por tipo de propiedad
tipos = sorted(df["tipo"].unique())
tipos_seleccionados = st.sidebar.multiselect("Tipo de propiedad", tipos, default=tipos)

# Filtro por rango de precios
precio_min, precio_max = int(df["precio"].min()), int(df["precio"].max())
rango_precio = st.sidebar.slider("Rango de precio (S/.)", min_value=precio_min, max_value=precio_max, value=(precio_min, precio_max))

# Aplicar filtros
df_filtrado = df[
    df["distrito"].isin(distritos_seleccionados) &
    df["tipo"].isin(tipos_seleccionados) &
    df["precio"].between(rango_precio[0], rango_precio[1])
]

# Mostrar mapa
st.subheader("📍 Ubicación de proyectos")
mapa = folium.Map(location=[-12.08, -77.03], zoom_start=12)

for _, row in df_filtrado.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"{row['nombre']}<br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
        tooltip=row["nombre"],
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(mapa)

st_data = st_folium(mapa, width=900, height=500)

# Mostrar lista de proyectos
st.subheader("📄 Lista de proyectos")

if df_filtrado.empty:
    st.warning("No se encontraron proyectos con los filtros seleccionados.")
else:
    for _, row in df_filtrado.iterrows():
        with st.expander(row["nombre"]):
            st.markdown(f"**Distrito:** {row['distrito']}")
            st.markdown(f"**Tipo:** {row['tipo']}")
            st.markdown(f"**Precio:** S/. {int(row['precio']):,}".replace(",", "."))
            st.markdown(f"[🔗 Ver proyecto]({row['link']})", unsafe_allow_html=True)
