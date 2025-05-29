import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ✅ Esta línea debe ir siempre al principio
st.set_page_config(page_title="LimaProp", layout="wide")

# Encabezado
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

    distrito_opciones = sorted(df["distrito"].unique())
    distrito_seleccionado = st.selectbox("Selecciona un distrito:", options=["Selecciona..."] + distrito_opciones)

    tipos_disponibles = sorted(df["tipo"].unique())
    tipo_seleccionado = st.multiselect("Tipo de propiedad:", options=tipos_disponibles, default=tipos_disponibles)

    precio_min = int(df["precio"].min())
    precio_max = int(df["precio"].max())
    rango_precios = st.slider("Rango de precios (S/.)", min_value=precio_min, max_value=precio_max,
                              value=(precio_min, precio_max))

# Filtrar solo si selecciona distrito
if distrito_seleccionado != "Selecciona...":
    df_filtrado = df[
        (df["distrito"] == distrito_seleccionado) &
        (df["tipo"].isin(tipo_seleccionado)) &
        (df["precio"] >= rango_precios[0]) &
        (df["precio"] <= rango_precios[1])
    ]

    # Mostrar lista de proyectos
    st.subheader(f"🏢 Proyectos disponibles en {distrito_seleccionado}")
    if df_filtrado.empty:
        st.warning("No se encontraron proyectos con los filtros seleccionados.")
    else:
        for _, row in df_filtrado.iterrows():
            st.markdown(
                f"""
                <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:10px;">
                    <h4 style="margin-bottom:5px;">{row['nombre']}</h4>
                    <p style="margin:0;"><strong>Tipo:</strong> {row['tipo']}</p>
                    <p style="margin:0;"><strong>Precio:</strong> S/. {int(row['precio']):,}</p>
                    <a href="{row['link']}" target="_blank" style="color:#1f77b4;">🔗 Ver proyecto</a>
                </div>
                """, unsafe_allow_html=True
            )

    # Mapa de proyectos
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
        st_folium(mapa, use_container_width=True, height=500)

# Footer profesional
st.markdown(
    """
    <hr style="margin-top: 50px;"/>
    <div style="text-align: center; font-size: 0.9em; color: #888;">
        © 2025 LimaProp. Todos los derechos reservados.
    </div>
    """,
    unsafe_allow_html=True
    )
