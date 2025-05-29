import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="LimaProp", layout="wide")

# Reducir márgenes globales y espacio final
st.markdown("""
    <style>
        .block-container {
            padding-bottom: 0rem !important;
        }
        iframe {
            height: 350px !important;
        }
        footer {visibility: hidden;}
        section.main > div:has(.folium-map) {
            padding-bottom: 0px !important;
            margin-bottom: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios por zona, tipo y precio en Lima Metropolitana!")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# Sidebar con filtros
with st.sidebar:
    st.header("🔎 Filtros")

    distrito_opciones = sorted(df["distrito"].unique())
    distrito_seleccionado = st.selectbox("Selecciona un distrito:", options=["Selecciona..."] + distrito_opciones)

    tipos_disponibles = sorted(df["tipo"].unique())
    tipo_seleccionado = st.multiselect("Tipo de propiedad:", options=tipos_disponibles, default=tipos_disponibles)

    precio_min = int(df["precio"].min())
    precio_max = int(df["precio"].max())
    rango_precios = st.slider("Rango de precios (S/.)", min_value=precio_min, max_value=precio_max,
                              value=(precio_min, precio_max))

# Filtrar datos
if distrito_seleccionado != "Selecciona...":
    df_filtrado = df[
        (df["distrito"] == distrito_seleccionado) &
        (df["tipo"].isin(tipo_seleccionado)) &
        (df["precio"] >= rango_precios[0]) &
        (df["precio"] <= rango_precios[1])
    ]

    st.subheader(f"🏢 Proyectos disponibles en {distrito_seleccionado}")
    if df_filtrado.empty:
        st.warning("No se encontraron proyectos con los filtros seleccionados.")
    else:
        for _, row in df_filtrado.iterrows():
            st.markdown(
                f"""
                <div style="border:1px solid #ddd; border-radius:10px; padding:12px; margin-bottom:8px; font-size:14px;">
                    <h4 style="margin-bottom:5px; font-size:16px;">{row['nombre']}</h4>
                    <p style="margin:0;"><strong>Tipo:</strong> {row['tipo']}</p>
                    <p style="margin:0;"><strong>Precio:</strong> S/. {int(row['precio']):,}</p>
                    <a href="{row['link']}" target="_blank" style="color:#1f77b4; font-size:13px;">🔗 Ver proyecto</a>
                </div>
                """, unsafe_allow_html=True
            )

    # Mapa de proyectos
    st.subheader("🗺️ Mapa de proyectos")
    if not df_filtrado.empty:
        with st.container():
            mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)
            for _, row in df_filtrado.iterrows():
                folium.Marker(
                    location=[row["lat"], row["lon"]],
                    popup=f"<strong>{row['nombre']}</strong><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
                    tooltip=row["nombre"],
                    icon=folium.Icon(color="blue", icon="home")
                ).add_to(mapa)
            st_folium(mapa, use_container_width=True, height=350)

# Eliminar footer visual innecesario
# Puedes volver a incluir el footer legal si gustas:
# st.markdown(...footer...)
