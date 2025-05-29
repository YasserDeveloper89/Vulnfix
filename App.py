import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="LimaProp", layout="wide")

st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios por zona, tipo y precio en Lima Metropolitana.")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
    required_columns = {"nombre", "distrito", "lat", "lon", "link", "precio", "tipo"}
    if not required_columns.issubset(df.columns):
        st.error(f"El archivo no tiene las columnas necesarias: {required_columns}")
        st.stop()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# Sidebar con filtros
with st.sidebar:
    st.header("🔎 Filtros")

    distrito_seleccionado = st.selectbox("Selecciona un distrito", options=sorted(df["distrito"].unique()))
    tipo_seleccionado = st.multiselect("Tipo de propiedad", options=sorted(df["tipo"].unique()), default=sorted(df["tipo"].unique()))
    precio_min = int(df["precio"].min())
    precio_max = int(df["precio"].max())
    rango_precios = st.slider("Rango de precios (S/.)", min_value=precio_min, max_value=precio_max, value=(precio_min, precio_max))

# Aplicar filtros
df_filtrado = df[
    (df["distrito"] == distrito_seleccionado) &
    (df["tipo"].isin(tipo_seleccionado)) &
    (df["precio"] >= rango_precios[0]) &
    (df["precio"] <= rango_precios[1])
]

# Mostrar columnas SIEMPRE — contenido condicional adentro
col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader(f"📍 Mapa en {distrito_seleccionado}")
    if not df_filtrado.empty:
        mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)
        for _, row in df_filtrado.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=f"<strong>{row['nombre']}</strong><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
                tooltip=row["nombre"],
                icon=folium.Icon(color="blue", icon="home")
            ).add_to(mapa)
        st_folium(mapa, use_container_width=True, height=500)
    else:
        st.info("No hay proyectos para este filtro.")

with col2:
    st.subheader("🏗️ Proyectos Disponibles")
    if df_filtrado.empty:
        st.warning("No se encontraron proyectos para los filtros seleccionados.")
    else:
        for _, row in df_filtrado.iterrows():
            with st.expander(row["nombre"]):
                st.markdown(f"**Distrito:** {row['distrito']}")
                st.markdown(f"**Tipo:** {row['tipo']}")
                st.markdown(f"**Precio:** S/. {int(row['precio']):,}".replace(",", "."))
                st.markdown(f"[🔗 Ver proyecto en Urbania]({row['link']})", unsafe_allow_html=True)
