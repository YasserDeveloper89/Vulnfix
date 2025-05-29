import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
from bs4 import BeautifulSoup

# 🔧 Configuración inicial de la página
st.set_page_config(page_title="LimaProp", layout="wide")

# 🏙️ Título
st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios por zona, tipo y precio en Lima Metropolitana.")

# 📁 Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# 🎛️ Sidebar: filtros
with st.sidebar:
    st.header("🔎 Filtros")

    distrito_seleccionado = st.selectbox(
        "Selecciona un distrito:",
        options=sorted(df["distrito"].unique())
    )

    tipos_disponibles = sorted(df["tipo"].unique())
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

# 📊 Aplicar filtros
df_filtrado = df[
    (df["distrito"] == distrito_seleccionado) &
    (df["tipo"].isin(tipo_seleccionado)) &
    (df["precio"] >= rango_precios[0]) &
    (df["precio"] <= rango_precios[1])
]

# 🧱 Distribución en columnas
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📄 Proyectos disponibles")
    if df_filtrado.empty:
        st.warning("No se encontraron proyectos para los filtros seleccionados.")
    else:
        for _, row in df_filtrado.iterrows():
            with st.container():
                st.markdown(f"### {row['nombre']}")
                st.markdown(f"- **Distrito:** {row['distrito']}")
                st.markdown(f"- **Tipo:** {row['tipo']}")
                st.markdown(f"- **Precio:** S/. {int(row['precio']):,}".replace(",", "."))
                st.markdown(f"[🔗 Ver proyecto en Urbania]({row['link']})", unsafe_allow_html=True)
                st.markdown("---")

with col2:
    st.subheader("🗺️ Mapa de proyectos")
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

# 📰 Noticias inmobiliarias (relleno del espacio)
st.markdown("## 📰 Noticias del sector inmobiliario en Lima")
try:
    noticias = []
    url = "https://gestion.pe/economia/inmobiliaria/"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    titulares = soup.select("h2 a")[:3]  # Primeros 3 titulares

    for link in titulares:
        titulo = link.get_text(strip=True)
        href = link["href"]
        noticias.append((titulo, href))

    for titulo, enlace in noticias:
        st.markdown(f"🔗 [{titulo}]({enlace})")
except Exception as e:
    st.info("No se pudieron cargar las noticias en este momento.")

# 🦶 Footer profesional
st.markdown("""<hr style="margin-top:50px;">
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    LimaProp © 2025 - Todos los derechos reservados. | Diseñado para explorar proyectos en Lima.
</div>""", unsafe_allow_html=True)
