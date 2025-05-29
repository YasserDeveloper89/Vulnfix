import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(page_title="LimaProp - Proyectos Inmobiliarios", layout="wide")

# Título
st.title("🏙️ LimaProp - Proyectos Inmobiliarios en Lima")
st.markdown("Explora los proyectos más recientes por distrito con mapa interactivo y enlaces reales.")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")

    # Validación básica
    required_cols = {'nombre', 'distrito', 'lat', 'lon', 'link'}
    if not required_cols.issubset(set(df.columns)):
        st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: {required_cols}")
        st.stop()

    # Filtro por distrito
    distritos = sorted(df['distrito'].unique())
    distrito_seleccionado = st.selectbox("Selecciona un distrito:", distritos)

    # Filtrar el DataFrame
    filtered_df = df[df['distrito'] == distrito_seleccionado]

    # Mapa interactivo
    st.subheader("🗺️ Mapa Interactivo")
    m = folium.Map(location=[-12.05, -77.05], zoom_start=13)
    for _, row in filtered_df.iterrows():
        folium.Marker(
            [row['lat'], row['lon']],
            popup=folium.Popup(f"<b>{row['nombre']}</b><br><a href='{row['link']}' target='_blank'>Ver Proyecto</a>", max_width=300),
            tooltip=row['nombre']
        ).add_to(m)
    st_folium(m, width=700, height=500)

    # Lista detallada de proyectos
    st.subheader("📋 Lista de Proyectos")
    for _, row in filtered_df.iterrows():
        with st.container():
            st.markdown(
                f"""
                ### 🏢 {row['nombre']}
                **Distrito:** {row['distrito']}  
                **Ubicación:** {row['lat']}, {row['lon']}  
                [🔗 Ver Proyecto]({row['link']})
                ---
                """
            )

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
