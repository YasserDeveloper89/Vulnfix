import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(page_title="LimaProp", layout="wide")

# Título de la aplicación
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

# Sidebar: filtros
with st.sidebar:
    st.header("🔎 Filtros")
    distritos = sorted(df["distrito"].unique())
    distrito_seleccionado = st.selectbox("Selecciona un distrito:", options=[""] + distritos)
    tipos_disponibles = sorted(df["tipo"].unique())
    tipo_seleccionado = st.multiselect("Tipo de propiedad:", options=tipos_disponibles, default=tipos_disponibles)
    precio_min = int(df["precio"].min())
    precio_max = int(df["precio"].max())
    rango_precios = st.slider("Rango de precios (S/.)", min_value=precio_min, max_value=precio_max, value=(precio_min, precio_max))

# Verificar si se ha seleccionado un distrito
if distrito_seleccionado:
    # Aplicar filtros
    df_filtrado = df[
        (df["distrito"] == distrito_seleccionado) &
        (df["tipo"].isin(tipo_seleccionado)) &
        (df["precio"] >= rango_precios[0]) &
        (df["precio"] <= rango_precios[1])
    ]

    # Mostrar proyectos
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

        # Mapa de proyectos
        st.subheader("🗺️ Mapa de proyectos")
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
    st.info("Por favor, selecciona un distrito para ver los proyectos disponibles.")

# Noticias inmobiliarias
st.markdown("## 📰 Noticias del sector inmobiliario en Perú")

noticias = [
    {
        "titulo": "Ventas de viviendas nuevas en Lima crecieron 30% en el primer trimestre de 2025",
        "resumen": "El mercado inmobiliario de Lima registró un incremento significativo en ventas en el primer trimestre del 2025, según ASEI.",
        "enlace": "https://gestion.pe/tu-dinero/inmobiliarias/ventas-de-viviendas-nuevas-en-lima-crecieron-30-en-primer-trimestre-del-2025-noticia/"
    },
    {
        "titulo": "Creciente demanda de espacios compartidos está transformando el mercado inmobiliario en Lima",
        "resumen": "La mayor demanda se concentra en distritos como Barranco, Surco, Magdalena, La Victoria y San Miguel.",
        "enlace": "https://elcomercio.pe/noticias/sector-inmobiliario/"
    },
    {
        "titulo": "El mercado inmobiliario en Lima creció 30% en el 2024, superando expectativas del sector",
        "resumen": "El mercado inmobiliario en Lima Metropolitana cerró el 2024 con un crecimiento anual de 30 %, al incorporar más de 4,900 viviendas nuevas respecto al periodo anterior.",
        "enlace": "https://elperuano.pe/noticia/263472-mercado-inmobiliario-en-lima-crecio-30-en-el-2024-superando-expectativas-del-sector"
    }
]

for noticia in noticias:
    st.markdown(f"**{noticia['titulo']}**")
    st.write(noticia['resumen'])
    st.markdown(f"[Leer más]({noticia['enlace']})")
    st.markdown("---")

# Footer profesional
st.markdown("""<hr style="margin-top:50px;">
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    LimaProp © 2025 - Todos los derechos reservados. | Diseñado para explorar proyectos en Lima.
</div>""", unsafe_allow_html=True)
