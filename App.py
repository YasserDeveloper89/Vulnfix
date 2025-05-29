import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from bs4 import BeautifulSoup
import requests

# Configuración de la página
st.set_page_config(page_title="LimaProp", layout="wide")

# Título principal
st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios por zona, tipo y precio en Lima Metropolitana.")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# Sidebar - Filtros
with st.sidebar:
    st.header("🔎 Filtros")

    distrito_seleccionado = st.selectbox(
        "Selecciona un distrito:",
        options=["-- Selecciona --"] + sorted(df["distrito"].unique())
    )

    if distrito_seleccionado != "-- Selecciona --":
        tipos_disponibles = sorted(df[df["distrito"] == distrito_seleccionado]["tipo"].unique())
        tipo_seleccionado = st.multiselect(
            "Tipo de propiedad:",
            options=tipos_disponibles,
            default=tipos_disponibles
        )

        precio_min = int(df["precio"].min())
        precio_max = int(df["precio"].max())
        rango_precios = st.slider(
            "Rango de precios (S/.)",
            min_value=precio_min,
            max_value=precio_max,
            value=(precio_min, precio_max)
        )

# Mostrar resultados solo si hay selección válida
if distrito_seleccionado != "-- Selecciona --":
    # Filtrar datos
    df_filtrado = df[
        (df["distrito"] == distrito_seleccionado) &
        (df["tipo"].isin(tipo_seleccionado)) &
        (df["precio"] >= rango_precios[0]) &
        (df["precio"] <= rango_precios[1])
    ]

    # Mostrar proyectos
    st.subheader("🏗️ Proyectos Disponibles")
    if df_filtrado.empty:
        st.warning("No se encontraron proyectos para los filtros seleccionados.")
    else:
        for _, row in df_filtrado.iterrows():
            st.markdown(f"""
                <div style="border:1px solid #ccc; border-radius:10px; padding:10px; margin-bottom:10px;">
                    <h4 style="margin-bottom:5px;">{row['nombre']}</h4>
                    <p style="margin:0;">📍 <b>Distrito:</b> {row['distrito']} | 🏠 <b>Tipo:</b> {row['tipo']} | 💰 <b>Precio:</b> S/. {int(row['precio']):,}</p>
                    <a href="{row['link']}" target="_blank">🔗 Ver proyecto</a>
                </div>
            """, unsafe_allow_html=True)

    # Mostrar mapa
    st.subheader("🗺️ Mapa Interactivo de Proyectos")
    mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)

    for _, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<strong>{row['nombre']}</strong><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
            tooltip=row["nombre"],
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(mapa)

    st_folium(mapa, use_container_width=True, height=500)

# Noticias Inmobiliarias
st.subheader("📰 Noticias Inmobiliarias en Perú")

try:
    url = "https://gestion.pe/economia/inmobiliaria/"
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    noticias = soup.select("h2.story-item__title a")[:4]

    for noticia in noticias:
        titulo = noticia.text.strip()
        link = noticia["href"]
        st.markdown(f"- [{titulo}]({link})")

except Exception:
    st.info("No se pudieron cargar las noticias en este momento.")

# Espaciador final mínimo
st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<hr>
<div style='text-align:center; font-size:14px; color:gray;'>
    © 2025 LimaProp | Desarrollado para mostrar proyectos inmobiliarios en Lima Metropolitana
</div>
""", unsafe_allow_html=True)
