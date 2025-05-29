import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image

# Cargar imágenes
logo = Image.open("logo_limaprop.png")
portada = Image.open("portada_limaprop.png")

# Configuración de la página
st.set_page_config(page_title="LimaProp", layout="wide")

# Mostrar portada y logo
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=100)
with col2:
    st.title("LimaProp - Proyectos Inmobiliarios 2025")
st.image(portada, use_column_width=True)

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")

    # Validar columnas
    required_columns = {'nombre', 'distrito', 'lat', 'lon', 'link'}
    if not required_columns.issubset(df.columns):
        st.error("El archivo de datos no contiene todas las columnas necesarias.")
    else:
        # Filtros
        st.sidebar.header("🔍 Filtros")
        distritos = sorted(df["distrito"].unique())
        distrito_seleccionado = st.sidebar.selectbox("Selecciona un distrito", ["Todos"] + distritos)

        if distrito_seleccionado != "Todos":
            df_filtrado = df[df["distrito"] == distrito_seleccionado]
        else:
            df_filtrado = df

        # Mostrar resultados
        st.markdown(f"### 🏘️ Resultados ({len(df_filtrado)} proyectos)")
        for index, row in df_filtrado.iterrows():
            with st.expander(f"{row['nombre']} - {row['distrito']}"):
                st.write(f"📍 Ubicación: {row['lat']}, {row['lon']}")
                st.write(f"🔗 [Ver propiedad en Urbania]({row['link']})")

        # Mapa
        st.markdown("### 🌍 Mapa Interactivo de Proyectos")
        if not df_filtrado.empty:
            m = folium.Map(location=[-12.1, -77.03], zoom_start=12)
            for index, row in df_filtrado.iterrows():
                folium.Marker(
                    location=[row["lat"], row["lon"]],
                    popup=f"{row['nombre']} ({row['distrito']})",
                    tooltip=row['nombre']
                ).add_to(m)
            st_folium(m, width=700, height=500)
        else:
            st.info("No hay proyectos disponibles para mostrar en el mapa.")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
