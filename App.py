import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="LimaProp", layout="wide")

# Estilos para quitar espacio final
st.markdown("""
    <style>
        .block-container {
            padding-bottom: 0rem !important;
        }
        footer, .st-emotion-cache-z5fcl4 { display: none; }
        iframe { margin-bottom: -30px !important; }
    </style>
""", unsafe_allow_html=True)

# Título
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

# Sidebar
with st.sidebar:
    st.header("🔎 Filtros")
    distrito = st.selectbox("Selecciona un distrito:", options=[""] + sorted(df["distrito"].unique()))
    tipos = st.multiselect("Tipo de propiedad:", options=sorted(df["tipo"].unique()), default=sorted(df["tipo"].unique()))
    precio_min, precio_max = st.slider("Rango de precios (S/.)",
                                       int(df["precio"].min()), int(df["precio"].max()),
                                       (int(df["precio"].min()), int(df["precio"].max())))

# Mostrar resultados solo si se ha seleccionado un distrito
if distrito:
    resultados = df[
        (df["distrito"] == distrito) &
        (df["tipo"].isin(tipos)) &
        (df["precio"] >= precio_min) &
        (df["precio"] <= precio_max)
    ]

    st.subheader("🏘️ Proyectos disponibles")
    if resultados.empty:
        st.warning("No se encontraron proyectos con los filtros seleccionados.")
    else:
        cols = st.columns(2)
        for i, (_, row) in enumerate(resultados.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 12px;
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05); margin-bottom: 20px;
                                border: 1px solid #eee;">
                        <h4 style="margin: 0 0 8px 0;">{row['nombre']}</h4>
                        <p><strong>Distrito:</strong> {row['distrito']}</p>
                        <p><strong>Tipo:</strong> {row['tipo']}</p>
                        <p><strong>Precio:</strong> S/. {int(row['precio']):,}".replace(",", ".")</p>
                        <a href="{row['link']}" target="_blank"
                           style="color: white; background: #0066cc;
                           padding: 6px 12px; border-radius: 6px;
                           text-decoration: none;">🔗 Ver proyecto</a>
                    </div>
                """, unsafe_allow_html=True)

        # Mapa solo si hay proyectos
        st.subheader("🗺️ Mapa de proyectos")
        map_container = st.container()
        with map_container:
            m = folium.Map(location=[resultados["lat"].mean(), resultados["lon"].mean()], zoom_start=14)
            for _, row in resultados.iterrows():
                folium.Marker(
                    location=[row["lat"], row["lon"]],
                    popup=f"<b>{row['nombre']}</b><br><a href='{row['link']}' target='_blank'>Ver más</a>",
                    tooltip=row["nombre"],
                    icon=folium.Icon(color="blue", icon="home")
                ).add_to(m)
            st_folium(m, height=400, use_container_width=True)

# Cierre para evitar espacio vacío
st.markdown("<style>body::after {content:'';display:block;height:1px;}</style>", unsafe_allow_html=True)
