import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Cargar datos
try:
    with open("urbania_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        df = pd.DataFrame(data)
except Exception as e:
    st.error("No se pudieron cargar los datos: " + str(e))
    st.stop()

# Título y filtros
st.title("🏠 Proyectos Inmobiliarios en Lima")
st.markdown("Consulta proyectos **actuales** por distrito con detalles reales.")

distritos = df["distrito"].unique()
filtro_distrito = st.selectbox("Selecciona un distrito:", sorted(distritos))

df_filtrado = df[df["distrito"] == filtro_distrito]

# Mostrar mapa interactivo
if not df_filtrado.empty:
    st.subheader(f"{len(df_filtrado)} proyectos encontrados en {filtro_distrito}:")

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=df_filtrado["lat"].mean(),
            longitude=df_filtrado["lon"].mean(),
            zoom=14,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_filtrado,
                get_position='[lon, lat]',
                get_color='[0, 122, 255, 160]',
                get_radius=50,
            ),
        ],
    ))

    # Mostrar tarjetas
    for index, row in df_filtrado.iterrows():
        with st.container():
            st.markdown(f"### 🏢 {row['nombre']}")
            st.markdown(f"📍 **Ubicación:** {row['direccion']}")
            st.markdown(f"💰 **Precio:** {row.get('precio', 'No disponible')}")
            st.markdown(f"🔗 [Ver en Urbania]({row['link']})", unsafe_allow_html=True)
            st.markdown("---")
else:
    st.warning("No se encontraron proyectos para este distrito.")