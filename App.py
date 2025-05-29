import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="LimaProp", layout="wide")

st.markdown("## 🏙️ LimaProp App - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios por zona, tipo y precio en Lima Metropolitana!")
st.markdown("---")

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
    distrito_seleccionado = st.selectbox("Selecciona un distrito", options=sorted(df["distrito"].unique()))
    tipo_seleccionado = st.multiselect("Tipo de propiedad", options=sorted(df["tipo"].unique()), default=sorted(df["tipo"].unique()))
    precio_min = int(df["precio"].min())
    precio_max = int(df["precio"].max())
    rango_precios = st.slider("Rango de precios (S/.)", min_value=precio_min, max_value=precio_max, value=(precio_min, precio_max))

# Aplicar filtros
df_filtrado = df[
    (df["distrito"] == distrito_seleccionado) &
    (df["tipo"].isin(tipo_seleccionado)) &
    (df["precio"] >= rango_precios[0]) &
    (df["precio"] <= rango_precios[1])
]

# Mostrar primero los proyectos centrados
st.subheader("🏗️ Proyectos en " + distrito_seleccionado)
with st.container():
    if df_filtrado.empty:
        st.warning("No se encontraron proyectos.")
    else:
        cols = st.columns(2)  # Distribuye proyectos en 2 columnas para mejor estética
        for i, (_, row) in enumerate(df_filtrado.iterrows()):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div style="background-color: #f9f9f9; padding: 16px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                        <h4 style="margin-bottom: 8px;">{row['nombre']}</h4>
                        <p style="margin: 0;"><strong>Tipo:</strong> {row['tipo']}</p>
                        <p style="margin: 0;"><strong>Distrito:</strong> {row['distrito']}</p>
                        <p style="margin: 0 0 10px;"><strong>Precio:</strong> S/. {int(row['precio']):,}".replace(",", ".")</p>
                        <a href="{row['link']}" target="_blank" style="text-decoration: none; color: white; background-color: #007bff; padding: 8px 16px; border-radius: 6px; display: inline-block;">🔗 Ver Proyecto</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Luego mostrar el mapa debajo
st.markdown("---")
st.subheader(f"📍 Mapa de proyectos en {distrito_seleccionado}")
if not df_filtrado.empty:
    mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)
    for _, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<strong>{row['nombre']}</strong><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
            tooltip=row["nombre"],
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(mapa)
    st_folium(mapa, use_container_width=True, height=520)
else:
    st.info("No hay proyectos para este filtro.")
