import streamlit as st
import pandas as pd 
import folium
from streamlit_folium import st_folium

Configuración de la página

st.set_page_config(page_title="LimaProp - Buscador de Proyectos Inmobiliarios", layout="wide")

st.title("LimaProp - Buscador de Proyectos Inmobiliarios") st.markdown("Explora proyectos inmobiliarios en Lima de forma interactiva.")

Cargar datos

try: df = pd.read_json("data_urbania.json") df["distrito"] = df["distrito"].astype(str).str.strip().str.title() df["tipo"] = df["tipo"].astype(str).str.strip().str.title() except Exception as e: st.error(f"Error al cargar el archivo JSON: {e}") st.stop()

Extraer opciones de filtros

distritos = sorted(df["distrito"].unique()) tipos = sorted(df["tipo"].unique())

Sidebar de filtros

st.sidebar.header("Filtrar proyectos")

distrito = st.sidebar.selectbox("Selecciona un distrito", distritos) tipos_seleccionados = st.sidebar.multiselect("Tipo de propiedad", tipos, default=tipos) precio_min = int(df["precio"].min()) precio_max = int(df["precio"].max()) precios = st.sidebar.slider("Rango de precio", precio_min, precio_max, (precio_min, precio_max))

Filtrar datos

filtro = ( (df["distrito"] == distrito) & (df["tipo"].isin(tipos_seleccionados)) & (df["precio"] >= precios[0]) & (df["precio"] <= precios[1]) ) df_filtrado = df[filtro]

Mapa con folium

st.subheader(f"Proyectos en {distrito}") if not df_filtrado.empty: mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14) for _, row in df_filtrado.iterrows(): folium.Marker( location=[row["lat"], row["lon"]], tooltip=row["nombre"], popup=f"<b>{row['nombre']}</b><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>", icon=folium.Icon(color="blue", icon="home") ).add_to(mapa) st_folium(mapa, use_container_width=True, height=500) else: st.warning("No hay proyectos que coincidan con los filtros seleccionados.")

Lista de proyectos

st.subheader("Lista de Proyectos") for _, row in df_filtrado.iterrows(): with st.expander(row["nombre"]): st.write(f"Distrito: {row['distrito']}") st.write(f"Tipo: {row['tipo']}") st.write(f"Precio: S/. {int(row['precio']):,}".replace(",", ".")) st.markdown(f"🔗 Ver proyecto en Urbania", unsafe_allow_html=True)

