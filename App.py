import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from bs4 import BeautifulSoup
import requests

# Configuración de la página
st.set_page_config(page_title="LimaProp - Proyectos Inmobiliarios", layout="wide")

# Título principal
st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios en Lima de forma interactiva.")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
    return df

df = load_data()

# Menú lateral
st.sidebar.header("📍 Filtrar proyectos")
zonas = sorted(df["distrito"].dropna().unique())
zona_seleccionada = st.sidebar.selectbox("Selecciona una zona:", ["Seleccionar"] + zonas)

# Mostrar resultados si se elige una zona
if zona_seleccionada != "Seleccionar":
    proyectos_filtrados = df[df["distrito"] == zona_seleccionada]

    st.subheader(f"🏘️ Proyectos disponibles en {zona_seleccionada}")
    for _, row in proyectos_filtrados.iterrows():
        with st.container():
            st.markdown(f"### {row['titulo']}")
            st.markdown(f"- **Tipo:** {row['tipo']}")
            st.markdown(f"- **Precio:** {row['precio']}")  
            st.markdown(f"- **Ubicación:** {row['distrito']}")
            st.markdown("---")

    st.subheader("🗺️ Mapa de proyectos")
    mapa = folium.Map(location=[-12.0464, -77.0428], zoom_start=12)

    for _, row in proyectos_filtrados.iterrows():
        if pd.notnull(row["latitud"]) and pd.notnull(row["longitud"]):
            folium.Marker(
                location=[row["latitud"], row["longitud"]],
                popup=row["titulo"],
                tooltip=row["titulo"]
            ).add_to(mapa)

    st_folium(mapa, width=700, height=500)

# Noticias para llenar espacio vacío
st.markdown("---")
st.subheader("📰 Noticias recientes sobre el mercado inmobiliario en Perú")

def obtener_noticias():
    url = "https://gestion.pe/economia/inmobiliaria/"
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        noticias = soup.find_all("div", class_="story-item__content")
        noticias_data = []
        for noticia in noticias[:5]:
            titulo = noticia.find("a").get_text(strip=True)
            link = noticia.find("a")["href"]
            noticias_data.append((titulo, "https://gestion.pe" + link))
        return noticias_data
    except Exception as e:
        return [("No se pudieron cargar noticias en este momento.", "#")]

noticias = obtener_noticias()
for titulo, enlace in noticias:
    st.markdown(f"- [{titulo}]({enlace})")

# Espacio final ajustado para evitar espacios vacíos excesivos
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
