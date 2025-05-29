import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ✅ Esto debe ir primero, antes de cualquier otra cosa
st.set_page_config(page_title="LimaProp", layout="wide")

# ✅ CSS para eliminar el espacio inferior
st.markdown("""
    <style>
        .block-container {
            padding-bottom: 0rem !important;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios por zona, tipo y precio en Lima Metropolitana.")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Sidebar con filtros
with st.sidebar:
    st.header("🔎 Filtros")

    distrito = st.selectbox("Selecciona un distrito:", options=sorted(df["distrito"].unique()))
    tipos_disponibles = sorted(df["tipo"].unique())
    tipo = st.multiselect("Tipo de propiedad:", options=tipos_disponibles, default=tipos_disponibles)

    precio_min = int(df["precio"].min())
    precio_max = int(df["precio"].max())
    precio = st.slider("Rango de precios (S/.)", min_value=precio_min, max_value=precio_max, value=(precio_min, precio_max))

# Filtro de datos
df_filtrado = df[
    (df["distrito"] == distrito) &
    (df["tipo"].isin(tipo)) &
    (df["precio"] >= precio[0]) &
    (df["precio"] <= precio[1])
]

# 🏘️ Mostrar proyectos disponibles
st.markdown("## 🏘️ Proyectos Disponibles")

if df_filtrado.empty:
    st.warning("No se encontraron proyectos para los filtros seleccionados.")
else:
    for _, row in df_filtrado.iterrows():
        st.markdown(f"""
            <div style="background-color:#f7f7f9;padding:1rem;border-radius:10px;margin-bottom:1rem;
                        box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                <h4 style="margin-bottom:0.3rem;">{row['nombre']}</h4>
                <p style="margin:0.2rem 0;"><strong>Distrito:</strong> {row['distrito']} | 
                <strong>Tipo:</strong> {row['tipo']} | 
                <strong>Precio:</strong> S/. {int(row['precio']):,}</p>
                <a href="{row['link']}" target="_blank">🔗 Ver proyecto</a>
            </div>
        """, unsafe_allow_html=True)

# 🗺️ Mapa de proyectos
if not df_filtrado.empty:
    st.markdown("## 🗺️ Mapa Interactivo de Proyectos")
    mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)
    for _, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<strong>{row['nombre']}</strong><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
            tooltip=row["nombre"],
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(mapa)

    st_folium(mapa, use_container_width=True, height=500)

# ✅ Footer profesional
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 0.9rem; color: gray; padding: 10px 0;">
    📞 Contacto: <a href="mailto:info@limaprop.com">info@limaprop.com</a> | 📍 Lima, Perú  
    <br>© 2025 LimaProp. Todos los derechos reservados.
</div>
""", unsafe_allow_html=True)
