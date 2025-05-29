import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(page_title="LimaProp", layout="wide")

# Título
st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios en Lima de forma interactiva y encuentra tu nuevo hogar.")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# Sidebar: filtros
st.sidebar.header("🔎 Filtros de búsqueda")
distritos = df["distrito"].sort_values().unique()
distrito_seleccionado = st.sidebar.selectbox("Selecciona un distrito", [""] + list(distritos))

# Mostrar proyectos si se seleccionó distrito
if distrito_seleccionado:
    st.subheader(f"🏢 Proyectos disponibles en {distrito_seleccionado}")
    proyectos = df[df["distrito"] == distrito_seleccionado]

    for _, row in proyectos.iterrows():
        with st.container():
            st.markdown(f"### {row['nombre']}")
            st.markdown(f"- **Tipo:** {row['tipo']}")
            st.markdown(f"- **Precio:** ${row['precio']:,}")
            st.markdown(f"[Ver más detalles]({row['link']})")
            st.markdown("---")

    # Mapa interactivo solo cuando hay proyectos filtrados
    st.subheader("🗺️ Mapa de proyectos")
    m = folium.Map(location=[proyectos["lat"].mean(), proyectos["lon"].mean()], zoom_start=15)

    for _, row in proyectos.iterrows():
        popup = folium.Popup(f"<b>{row['nombre']}</b><br>{row['tipo']}<br>${row['precio']:,}", max_width=250)
        folium.Marker([row["lat"], row["lon"]], popup=popup).add_to(m)

    st_folium(m, width=700, height=500)

# Noticias del sector inmobiliario
st.markdown("## 📰 Noticias del Sector Inmobiliario en Perú (2025)")
noticias = [
    {
        "titulo": "Ventas de viviendas en Lima crecieron 30% en el primer trimestre de 2025",
        "resumen": "Durante el primer trimestre de 2025, el mercado inmobiliario limeño experimentó un importante repunte, alcanzando la venta de 6,237 unidades.",
        "enlace": "https://www.revistaeconomia.com/asei-ventas-de-viviendas-nuevas-en-lima-crecieron-30-en-el-primer-trimestre-de-2025/"
    },
    {
        "titulo": "Jóvenes peruanos impulsan la compra de viviendas en 2025",
        "resumen": "El mercado inmobiliario peruano se reinventa con una nueva generación de compradores entre 30 y 45 años que buscan estabilidad económica.",
        "enlace": "https://elperuano.pe/noticia/263720-boom-inmobiliario-en-regiones-jovenes-peruanos-impulsan-la-compra-de-viviendas-en-2025"
    },
    {
        "titulo": "Tendencias clave en el mercado inmobiliario peruano en 2025",
        "resumen": "El sector debe adaptarse a la nueva normativa VIS, fluctuaciones de tasas de interés y atraer inversionistas con propuestas diferenciadas.",
        "enlace": "https://vao.pe/tendencias-clave-mercado-inmobiliario-peruano-2025"
    },
    {
        "titulo": "El boom inmobiliario en el Perú en el 2025: cinco datos clave y tendencias del mercado",
        "resumen": "El programa MiVivienda ha sido clave, con una inversión estatal de S/1,338 millones y un 69% de ventas en viviendas de interés social.",
        "enlace": "https://www.cronicaviva.com.pe/el-boom-inmobiliario-en-el-peru-en-2025-datos-clave-y-tendencias-del-mercado/"
    },
    {
        "titulo": "Omar Castro, un poeta frente al problema de la vivienda",
        "resumen": "Castro aborda la crisis habitacional desde una perspectiva artística, denunciando la especulación y falta de políticas de vivienda social.",
        "enlace": "https://elpais.com/cultura/2025-04-03/omar-castro-un-poeta-frente-al-problema-de-la-vivienda-es-alucinante-lo-poco-que-vale-una-vida-en-contraste-con-lo-caro-que-es-vivir.html"
    }
]

for noticia in noticias:
    st.markdown(f"**{noticia['titulo']}**")
    st.write(noticia['resumen'])
    st.markdown(f"[Leer más]({noticia['enlace']})")
    st.markdown("---")

# Footer para mejorar estética
st.markdown(
    """
    <hr style="margin-top: 2rem; margin-bottom: 1rem;">
    <div style="text-align: center; color: gray; font-size: small;">
        © 2025 LimaProp | Desarrollado con ❤️ usando Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
