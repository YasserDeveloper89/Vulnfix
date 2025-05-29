import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image
import requests
from bs4 import BeautifulSoup

# Configuración de la página
st.set_page_config(page_title="LimaProp", layout="wide")

# Logo (opcional)
st.sidebar.image("logo.png", width=180)

# Menú lateral
seccion = st.sidebar.radio("Explorar", ["Inicio", "Buscar por distrito", "Noticias del sector"])

st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# Función para mostrar tarjetas de proyectos
def mostrar_proyectos(data):
    for _, row in data.iterrows():
        with st.container():
            st.markdown(f"### [{row['nombre']}]({row['link']})")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**Distrito:** {row['distrito']}")
                st.write(f"**Tipo:** {row['tipo']}")
                st.write(f"**Precio:** ${row['precio']:,}")
            with col2:
                st.write(" ")
            with col3:
                st.button("Ver Proyecto", key=row['nombre'], on_click=lambda: st.markdown(f"[Ir al proyecto]({row['link']})"))

# Sección de Inicio
if seccion == "Inicio":
    st.markdown("### Bienvenido a LimaProp")
    st.markdown("Selecciona una opción en el menú lateral para comenzar.")

# Sección de búsqueda
elif seccion == "Buscar por distrito":
    st.subheader("Proyectos disponibles")
    distritos = sorted(df["distrito"].unique())
    distrito_seleccionado = st.selectbox("Selecciona un distrito", [""] + distritos)

    if distrito_seleccionado:
        proyectos = df[df["distrito"] == distrito_seleccionado]
        if not proyectos.empty:
            mostrar_proyectos(proyectos)

            # Mostrar mapa
            st.subheader("Mapa interactivo de proyectos")
            m = folium.Map(location=[proyectos["lat"].mean(), proyectos["lon"].mean()], zoom_start=14)
            for _, row in proyectos.iterrows():
                folium.Marker(
                    [row["lat"], row["lon"]],
                    tooltip=row["nombre"],
                    popup=f"<a href='{row['link']}' target='_blank'>{row['nombre']}</a>"
                ).add_to(m)
            st_folium(m, width=700, height=400)
        else:
            st.info("No hay proyectos disponibles en ese distrito.")

# Sección de noticias
elif seccion == "Noticias del sector":
    st.subheader("📰 Noticias del sector inmobiliario en Perú")

    def obtener_noticias():
        url = "https://gestion.pe/economia/inmobiliaria/"
        try:
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.content, "html.parser")
            articles = soup.find_all("div", class_="story-item__info", limit=5)
            noticias = []
            for art in articles:
                titulo = art.find("a").get_text(strip=True)
                enlace = art.find("a")["href"]
                noticias.append((titulo, "https://gestion.pe" + enlace if enlace.startswith("/") else enlace))
            return noticias
        except Exception as e:
            return [("Error al obtener noticias", str(e))]

    noticias = obtener_noticias()
    for titulo, enlace in noticias:
        st.markdown(f"- [{titulo}]({enlace})")

# Footer para eliminar espacio vacío
st.markdown(
    """
    <style>
    .reportview-container .main footer {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-bottom: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("---")
st.markdown("© 2025 LimaProp | Todos los derechos reservados", unsafe_allow_html=True)
