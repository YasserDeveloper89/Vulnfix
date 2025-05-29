import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ⚠️ Esta línea debe ir primero
st.set_page_config(page_title="LimaProp", layout="wide")

# Título principal
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

# Sidebar con filtros
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

# Aplicar filtros
df_filtrado = df[
    (df["distrito"] == distrito_seleccionado) &
    (df["tipo"].isin(tipo_seleccionado)) &
    (df["precio"] >= rango_precios[0]) &
    (df["precio"] <= rango_precios[1])
]

# ==========================
# Proyectos (estilo catálogo)
# ==========================
st.subheader("🏘️ Proyectos disponibles")
if df_filtrado.empty:
    st.warning("No se encontraron proyectos para los filtros seleccionados.")
else:
    cols = st.columns(2)
    for idx, (_, row) in enumerate(df_filtrado.iterrows()):
        with cols[idx % 2]:
            st.markdown(f"""
                <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; 
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); margin-bottom: 20px;
                            border: 1px solid #e0e0e0;">
                    <h4 style="margin-top: 0; color: #333;">{row['nombre']}</h4>
                    <p style="margin: 4px 0;"><strong>Distrito:</strong> {row['distrito']}</p>
                    <p style="margin: 4px 0;"><strong>Tipo:</strong> {row['tipo']}</p>
                    <p style="margin: 4px 0;"><strong>Precio:</strong> S/. {int(row['precio']):,}".replace(",", ".")</p>
                    <a href="{row['link']}" target="_blank" 
                       style="display: inline-block; margin-top: 10px; color: #fff; 
                       background-color: #0066cc; padding: 8px 16px; border-radius: 6px; 
                       text-decoration: none;">🔗 Ver proyecto</a>
                </div>
            """, unsafe_allow_html=True)

# ==========================
# Mapa interactivo (debajo)
# ==========================
if not df_filtrado.empty:
    st.subheader(f"🗺️ Mapa de proyectos en {distrito_seleccionado}")
    mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)

    for _, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<strong>{row['nombre']}</strong><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
            tooltip=row["nombre"],
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(mapa)

    st_folium(mapa, use_container_width=True, height=500)
