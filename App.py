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
        "titulo": "Ventas de viviendas en Lima crecieron 30% en el primer trimestre de 2025",
        "resumen": "Según ASEI, se vendieron 6.237 unidades habitacionales en Lima durante el primer trimestre de 2025, lo que representa un aumento del 30% respecto al mismo periodo del año anterior.",
        "enlace": "https://www.infobae.com/peru/2025/05/07/mercado-inmobiliario-de-lima-crece-30-en-el-primer-trimestre-de-2025-cual-es-el-precio-promedio-hoy-de-un-departamento/"
    },
    {
        "titulo": "Demanda de micro departamentos en Lima impulsa el mercado inmobiliario",
        "resumen": "La creciente demanda por micro departamentos y viviendas compactas, impulsada por jóvenes profesionales, está transformando el mercado inmobiliario en Lima.",
        "enlace": "https://www.infobae.com/peru/2025/05/29/invertir-en-inmuebles-en-peru-en-2025-una-oportunidad-real-y-rentable/"
    },
    {
        "titulo": "Inmobiliarias chilenas invierten US$ 200 millones en Perú en 2025",
        "resumen": "Con el mercado inmobiliario de Chile en desaceleración, varias empresas de ese país están profundizando su expansión hacia Perú.",
        "enlace": "https://gestion.pe/economia/empresas/peru-es-ahora-destino-de-inmobiliarias-chilenas-con-inversiones-por-us-200-millones-noticia/"
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
