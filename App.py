import streamlit as st import pandas as pd import folium from streamlit_folium import st_folium from PIL import Image

Configuración de la página

st.set_page_config(page_title="LimaProp", layout="wide")

Encabezado

st.title("LimaProp - Buscador de Proyectos Inmobiliarios") st.markdown("Explora proyectos inmobiliarios en Lima de forma interactiva y actualizada.")

Sidebar para selección de zona

st.sidebar.header("Filtrar por zona")

Cargar datos

try: df = pd.read_json("data_urbania.json") df["distrito"] = df["distrito"].astype(str).str.strip().str.title() df["tipo"] = df["tipo"].astype(str).str.strip().str.title() except Exception as e: st.error(f"Error al cargar el archivo JSON: {e}") st.stop()

Opciones de filtrado

zonas = sorted(df["distrito"].unique()) zona_seleccionada = st.sidebar.selectbox("Selecciona una zona:", ["-- Selecciona --"] + zonas)

Mostrar proyectos solo si se ha seleccionado una zona

if zona_seleccionada != "-- Selecciona --": st.subheader("🛌 Proyectos Disponibles") proyectos = df[df["distrito"] == zona_seleccionada]

for idx, row in proyectos.iterrows():
    with st.container():
        cols = st.columns([1, 3])
        with cols[0]:
            if row["image"]:
                try:
                    st.image(row["image"], width=150)
                except:
                    st.write("[Imagen no disponible]")
        with cols[1]:
            st.markdown(f"**{row['nombre']}**")
            st.markdown(f"Tipo: {row['tipo']}")
            st.markdown(f"Precio: {row['precio']}")
            st.markdown(f"Ubicación: {row['direccion']}")
            st.markdown("---")

# Mapa interactivo
st.subheader(":world_map: Mapa de Proyectos")
m = folium.Map(location=[-12.0464, -77.0428], zoom_start=12)
for idx, row in proyectos.iterrows():
    try:
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=row["nombre"],
            tooltip=row["nombre"]
        ).add_to(m)
    except:
        continue
st_folium(m, width=1000)

Noticias del sector inmobiliario

st.subheader("📰 Noticias del Sector Inmobiliario en Perú (2025)")

noticias = [ { "titulo": "Ventas de viviendas nuevas en Lima crecieron 30% en el primer trimestre de 2025", "resumen": "El mercado inmobiliario de Lima Metropolitana experimentó un crecimiento del 30% en ventas durante el primer trimestre de 2025, impulsado por la Vivienda de Interés Social, según ASEI.", "enlace": "https://gestion.pe/tu-dinero/inmobiliarias/" }, { "titulo": "Tendencias clave en el mercado inmobiliario peruano en 2025", "resumen": "El sector enfrenta desafíos como adaptarse a la nueva normativa VIS, mantener la demanda en un contexto de posibles fluctuaciones en las tasas de interés y diferenciar su oferta para atraer tanto a compradores finales como a inversionistas.", "enlace": "https://vao.pe/tendencias-clave-mercado-inmobiliario-peruano-2025" }, { "titulo": "El boom inmobiliario en el Perú en el 2025: cinco datos clave y tendencias del mercado", "resumen": "El sector inmobiliario en el Perú vive un momento de dinamismo en 2025, marcado por un crecimiento sostenido, cambios en las preferencias de compradores y políticas públicas que impulsan la demanda.", "enlace": "https://www.cronicaviva.com.pe/el-boom-inmobiliario-en-el-peru-en-2025-datos-clave-y-tendencias-del-mercado/" }, { "titulo": "Perspectivas del sector inmobiliario en Perú para 2025: tendencias y oportunidades", "resumen": "El mercado inmobiliario en Perú sigue evolucionando, influenciado por factores económicos, sociales y tecnológicos. En 2025, se esperan cambios significativos en la demanda de vivienda, inversión y financiamiento.", "enlace": "https://hdcorpgrupoinmobiliario.com/2025/03/17/perspectivas-del-sector-inmobiliario-en-peru-para-2025/" } ]

for noticia in noticias: st.markdown(f"{noticia['titulo']}") st.write(noticia['resumen']) st.markdown(f"Leer más") st.markdown("---")

Footer

st.markdown(""" <hr style='margin-top: 50px; margin-bottom: 10px;'> <div style='text-align: center; color: gray;'> LimaProp © 2025 - Todos los derechos reservados | Diseño profesional para una experiencia inmobiliaria moderna. </div> """, unsafe_allow_html=True)

