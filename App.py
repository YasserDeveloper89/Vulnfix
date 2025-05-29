import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuración de página (¡SIEMPRE lo primero!)
st.set_page_config(page_title="LimaProp", layout="wide")

# Estilos para eliminar espacio inferior
st.markdown("""
    <style>
    .block-container {
        padding-bottom: 0rem !important;
    }
    .main > div:has(.stButton) {
        margin-bottom: 0rem !important;
    }
    footer, .st-emotion-cache-z5fcl4 {
        display: none;
    }
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

    distrito_seleccionado = st.selectbox("Selecciona un distrito:",
                                         options=[""] + sorted(df["distrito"].unique()))

    tipo_seleccionado = st.multiselect(
        "Tipo de propiedad:",
        options=sorted(df["tipo"].unique()),
        default=sorted(df["tipo"].unique())
    )

    rango_precios = st.slider(
        "Rango de precios (S/.)",
        min_value=int(df["precio"].min()),
        max_value=int(df["precio"].max()),
        value=(int(df["precio"].min()), int(df["precio"].max()))
    )

# Mostrar resultados sólo si se selecciona distrito
if distrito_seleccionado:
    df_filtrado = df[
        (df["distrito"] == distrito_seleccionado) &
        (df["tipo"].isin(tipo_seleccionado)) &
        (df["precio"] >= rango_precios[0]) &
        (df["precio"] <= rango_precios[1])
    ]

    st.subheader("🏘️ Proyectos disponibles")
    if df_filtrado.empty:
        st.warning("No se encontraron proyectos con los filtros seleccionados.")
    else:
        cols = st.columns(2)
        for i, (_, row) in enumerate(df_filtrado.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 12px;
                                box-shadow: 0 4px 8px rgba(0,0,0,0.05); margin-bottom: 20px;
                                border: 1px solid #eee;">
                        <h4 style="margin: 0 0 8px 0;">{row['nombre']}</h4>
                        <p style="margin: 4px 0;"><strong>Distrito:</strong> {row['distrito']}</p>
                        <p style="margin: 4px 0;"><strong>Tipo:</strong> {row['tipo']}</p>
                        <p style="margin: 4px 0;"><strong>Precio:</strong> S/. {int(row['precio']):,}".replace(",", ".")</p>
                        <a href="{row['link']}" target="_blank" style="color: white; background: #0066cc;
                           padding: 6px 12px; border-radius: 6px; text-decoration: none;">🔗 Ver proyecto</a>
                    </div>
                """, unsafe_allow_html=True)

        st.subheader("🗺️ Mapa de proyectos")
        mapa = folium.Map(location=[df_filtrado["lat"].mean(), df_filtrado["lon"].mean()], zoom_start=14)

        for _, row in df_filtrado.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=f"<b>{row['nombre']}</b><br><a href='{row['link']}' target='_blank'>Ver más</a>",
                tooltip=row["nombre"],
                icon=folium.Icon(color="blue", icon="home")
            ).add_to(mapa)

        st_folium(mapa, use_container_width=True, height=500)

# Div para terminar sin espacio sobrante
st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
