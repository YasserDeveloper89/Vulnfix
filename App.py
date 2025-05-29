import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(page_title="LimaProp", layout="wide")

# Título
st.title("LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios en Lima de forma interactiva y selecciona el distrito de tu preferencia para ver más detalles.")

# Cargar datos
try:
    df = pd.read_json("data_urbania.json")
    df["distrito"] = df["distrito"].astype(str).str.strip().str.title()
    df["tipo"] = df["tipo"].astype(str).str.strip().str.title()
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# Sidebar: Selección de distrito
distritos = sorted(df["distrito"].unique())
zona_seleccionada = st.sidebar.selectbox("Selecciona una zona de Lima:", [""] + distritos)

if zona_seleccionada:
    # Filtrar proyectos por zona seleccionada
    proyectos_filtrados = df[df["distrito"] == zona_seleccionada]

    # Mostrar proyectos disponibles
    st.subheader(f"Proyectos disponibles en {zona_seleccionada}:")
    for _, row in proyectos_filtrados.iterrows():
        with st.container():
            st.markdown(f"### [{row['nombre']}]({row['link']})")
            st.markdown(f"- **Tipo:** {row['tipo']}")
            st.markdown(f"- **Precio:** ${row['precio']:,}")
            st.markdown("---")

    # Mapa interactivo
    st.subheader("Mapa de proyectos")
    m = folium.Map(location=[proyectos_filtrados["lat"].mean(), proyectos_filtrados["lon"].mean()], zoom_start=14)
    for _, row in proyectos_filtrados.iterrows():
        popup_text = f"{row['nombre']}<br>Precio: ${row['precio']:,}<br><a href='{row['link']}' target='_blank'>Ver más</a>"
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup_text,
            tooltip=row["nombre"]
        ).add_to(m)

    st_folium(m, width=1000, height=500)

# Footer profesional
st.markdown("""<hr style="margin-top: 50px;">
<p style="text-align:center; color:gray; font-size:14px;">
© 2025 LimaProp. Todos los derechos reservados.
</p>
""", unsafe_allow_html=True)
