import streamlit as st import pandas as pd import folium from streamlit_folium import st_folium

Configuración de la página

st.set_page_config(page_title="LimaProp", layout="wide")

Título de la aplicación

st.title("LimaProp - Buscador de Proyectos Inmobiliarios") st.markdown("Explora proyectos inmobiliarios en Lima de forma interactiva.")

Cargar datos

try: df = pd.read_json("data_urbania.json") df["distrito"] = df["distrito"].astype(str).str.strip().str.title() df["tipo"] = df["tipo"].astype(str).str.strip().str.title() except Exception as e: st.error(f"Error al cargar el archivo JSON: {e}") st.stop()

Menú de selección de distrito

distritos = ["Seleccione un distrito"] + sorted(df["distrito"].unique()) distrito_seleccionado = st.selectbox("Selecciona un distrito", distritos)

if distrito_seleccionado != "Seleccione un distrito": proyectos_filtrados = df[df["distrito"] == distrito_seleccionado]

st.subheader("🏢 Proyectos Disponibles")
for _, row in proyectos_filtrados.iterrows():
    with st.container():
        st.markdown(f"### [{row['nombre']}]({row['link']})")
        st.markdown(f"**Distrito:** {row['distrito']}  |  **Precio:** ${row['precio']:,.0f}  |  **Tipo:** {row['tipo']}")
        st.markdown("---")

# Crear el mapa
mapa = folium.Map(location=[proyectos_filtrados["lat"].mean(), proyectos_filtrados["lon"].mean()], zoom_start=14)

for _, row in proyectos_filtrados.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"<b>{row['nombre']}</b><br>{row['distrito']}<br>${row['precio']:,.0f}",
        tooltip=row["nombre"]
    ).add_to(mapa)

st.subheader("🗺️ Mapa de Proyectos")
st_data = st_folium(mapa, width=1000, height=500)

Noticias Inmobiliarias para rellenar espacio vacío

st.subheader("📰 Noticias Inmobiliarias Recientes") noticias = [ { "titulo": "Ventas de viviendas en Lima crecieron 30% en el primer trimestre de 2025", "resumen": "El mercado inmobiliario de Lima Metropolitana experimentó un crecimiento notable durante 2024, con un aumento del 30% en las ventas de unidades habitacionales en comparación con el año anterior.", "enlace": "https://gestion.pe/tu-dinero/inmobiliarias/ventas-de-viviendas-en-lima-crecieron-30-en-primer-trimestre-del-2025-noticia/" }, { "titulo": "Perú en la mira de inmobiliarias chilenas con inversiones por US$ 200 millones en 2025", "resumen": "Con el mercado inmobiliario de Chile en desaceleración, varias empresas de ese país están profundizando su expansión hacia Perú.", "enlace": "https://gestion.pe/economia/empresas/peru-es-ahora-destino-de-inmobiliarias-chilenas-con-inversiones-por-us-200-millones-noticia/" }, { "titulo": "Estos son los distritos de Lima que concentran la mayor demanda inmobiliaria", "resumen": "El precio más buscado por los compradores en ferias fluctúa entre S/300.000 y S/400.000, mientras que los departamentos de tres habitaciones lideran las preferencias.", "enlace": "https://larepublica.pe/economia/2025/05/17/estos-son-los-distritos-de-lima-que-concentran-la-mayor-demanda-inmobiliaria-segun-urbania-hnews-915518" } ]

for noticia in noticias: st.markdown(f"{noticia['titulo']}") st.write(noticia['resumen']) st.markdown(f"Leer más") st.markdown("---")

Footer personalizado

st.markdown(""" <style> footer { visibility: hidden; } .footer-container { font-size: 0.9rem; text-align: center; color: #999; padding: 20px 0; } </style> <div class="footer-container"> © 2025 LimaProp - Todos los derechos reservados </div> """, unsafe_allow_html=True)

