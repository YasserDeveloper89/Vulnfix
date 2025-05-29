import streamlit as st import pandas as pd import pydeck as pdk

------------------------------

1. TÍTULO Y DESCRIPCIÓN

------------------------------

st.set_page_config(page_title="Mapa de Proyectos Inmobiliarios - Lima", layout="wide") st.title("📍 Mapa Interactivo de Proyectos Inmobiliarios - San Isidro y Miraflores") st.markdown("Visualiza proyectos activos en zonas clave de Lima Metropolitana. Datos simulados para demostración.")

------------------------------

2. DATA SIMULADA DE PROYECTOS

------------------------------

data = pd.DataFrame([ {"nombre": "Residencial El Bosque", "distrito": "San Isidro", "tipo": "Departamentos", "empresa": "Grupo El Sol", "lat": -12.0985, "lon": -77.0375, "avance": 75}, {"nombre": "Torre Mar", "distrito": "Miraflores", "tipo": "Oficinas", "empresa": "Edifica", "lat": -12.1231, "lon": -77.0305, "avance": 60}, {"nombre": "EcoVida 360", "distrito": "San Isidro", "tipo": "Departamentos", "empresa": "Besco", "lat": -12.0942, "lon": -77.0360, "avance": 90}, {"nombre": "Mirador Lima", "distrito": "Miraflores", "tipo": "Mixto", "empresa": "Menorca", "lat": -12.1218, "lon": -77.0332, "avance": 40} ])

------------------------------

3. FILTROS INTERACTIVOS

------------------------------

distritos = st.sidebar.multiselect("Filtrar por distrito", options=data["distrito"].unique(), default=data["distrito"].unique()) tipos = st.sidebar.multiselect("Filtrar por tipo de proyecto", options=data["tipo"].unique(), default=data["tipo"].unique())

data_filtrada = data[(data["distrito"].isin(distritos)) & (data["tipo"].isin(tipos))]

------------------------------

4. MAPA INTERACTIVO

------------------------------

st.pydeck_chart(pdk.Deck( map_style='mapbox://styles/mapbox/streets-v12', initial_view_state=pdk.ViewState( latitude=-12.1100, longitude=-77.0365, zoom=13, pitch=45, ), layers=[ pdk.Layer( 'ScatterplotLayer', data=data_filtrada, get_position='[lon, lat]', get_fill_color='[200, 30, 0, 160]', get_radius=100, pickable=True ) ], tooltip={"text": "{nombre}\n{tipo} - {empresa}\nAvance: {avance}%"} ))

------------------------------

5. TABLA COMPLEMENTARIA

------------------------------

st.markdown("### 📊 Detalles de Proyectos") st.dataframe(data_filtrada.reset_index(drop=True))

