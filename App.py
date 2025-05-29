import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ✅ Debe ser el primer comando de Streamlit
st.set_page_config(page_title="LimaProp", layout="wide")

# 🎨 Estilo personalizado para mejorar estética
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem !important;
    }
    .project-card {
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

# 🏙️ Título principal
st.title("🏙️ LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios por zona, tipo y precio en Lima Metropolitana.")

# 📄 Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# 🎛️ Filtros laterales
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

# 📍 Mapa y proyectos
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader(f"📍 Mapa de proyectos en {distrito_seleccionado}")
    if not df_filtrado.empty:
        mapa = folium.Map(
            location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()],
            zoom_start=14
        )

        for _, row in df_filtrado.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=f"<strong>{row['nombre']}</strong><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
                tooltip=row["nombre"],
                icon=folium.Icon(color="blue", icon="home")
            ).add_to(mapa)

        st_folium(mapa, use_container_width=True, height=500)
    else:
        st.warning("No se encontraron proyectos para los filtros seleccionados.")

with col2:
    st.subheader("🏗️ Proyectos Disponibles")
    if df_filtrado.empty:
        st.info("No hay proyectos con las características seleccionadas.")
    else:
        for _, row in df_filtrado.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="project-card">
                        <h4>{row['nombre']}</h4>
                        <p><strong>Distrito:</strong> {row['distrito']}<br>
                        <strong>Tipo:</strong> {row['tipo']}<br>
                        <strong>Precio:</strong> S/. {int(row['precio']):,}</p>
                        <a href="{row['link']}" target="_blank">🔗 Ver proyecto en Urbania</a>
                    </div>
                """, unsafe_allow_html=True)
