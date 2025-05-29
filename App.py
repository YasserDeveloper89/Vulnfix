import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 🧩 Configuración inicial
st.set_page_config(page_title="LimaProp", layout="wide")

# 🔧 Reducir padding y ocultar footer nativo
st.markdown("""
    <style>
        .block-container {
            padding-bottom: 0rem !important;
        }
        footer, .stApp footer {
            visibility: hidden;
        }
        .project-card {
            border: 1px solid #eee;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: #fff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# 🏙️ Título principal
st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios por zona, tipo y precio en Lima Metropolitana.")

# 📂 Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# 🔍 Sidebar con filtros
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

# 📊 Aplicar filtros
df_filtrado = df[
    (df["distrito"] == distrito_seleccionado) &
    (df["tipo"].isin(tipo_seleccionado)) &
    (df["precio"] >= rango_precios[0]) &
    (df["precio"] <= rango_precios[1])
]

# 📋 Mostrar proyectos disponibles
st.subheader("🏘️ Proyectos disponibles")
if df_filtrado.empty:
    st.warning("No se encontraron proyectos para los filtros seleccionados.")
else:
    for _, row in df_filtrado.iterrows():
        st.markdown(f"""
        <div class="project-card">
            <h4>{row['nombre']}</h4>
            <p><strong>Distrito:</strong> {row['distrito']}<br>
            <strong>Tipo:</strong> {row['tipo']}<br>
            <strong>Precio:</strong> S/. {int(row['precio']):,}</p>
            <a href="{row['link']}" target="_blank">🔗 Ver proyecto</a>
        </div>
        """, unsafe_allow_html=True)

# 🗺️ Mapa de proyectos
st.subheader("🗺️ Mapa de proyectos")
if not df_filtrado.empty:
    mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)
    for _, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<strong>{row['nombre']}</strong><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
            tooltip=row["nombre"],
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(mapa)
    st_data = st_folium(mapa, use_container_width=True, height=500)

# ✅ Footer profesional
st.markdown("""
    <style>
    .footer {
        position: relative;
        bottom: 0;
        width: 100%;
        padding: 1rem 0;
        text-align: center;
        font-size: 0.9rem;
        color: gray;
        background-color: #f9f9f9;
        margin-top: 2rem;
    }
    </style>

    <div class="footer">
        📞 Contacto: <a href="mailto:info@limaprop.com">info@limaprop.com</a> | 📍 Lima, Perú  
        <br>© 2025 LimaProp. Todos los derechos reservados.
    </div>
""", unsafe_allow_html=True)
