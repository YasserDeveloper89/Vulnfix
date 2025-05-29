import streamlit as st import pandas as pd import folium from streamlit_folium import st_folium from PIL import Image

st.set_page_config(page_title="LimaProp - Proyectos Inmobiliarios", layout="wide")

Mostrar el logo

try: logo = Image.open("logo_limaprop.png") st.image(logo, width=150) except FileNotFoundError: st.warning("Logo no encontrado. Asegúrate de tener 'logo_limaprop.png' en la misma carpeta.")

Mostrar la portada

try: portada = Image.open("portada_limaprop.png") st.image(portada, use_column_width=True) except FileNotFoundError: st.warning("Portada no encontrada. Asegúrate de tener 'portada_limaprop.png' en la misma carpeta.")

st.title("\U0001F3E0 LimaProp - Proyectos Inmobiliarios en Lima (Versión Premium)")

Cargar datos

try: df = pd.read_json("data_urbania.json") except Exception as e: st.error("Error al cargar los datos: " + str(e)) st.stop()

Verificar columnas necesarias

columnas_necesarias = {'nombre', 'distrito', 'lat', 'lon', 'link'} if not columnas_necesarias.issubset(df.columns): st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: {columnas_necesarias}\nColumnas actuales: {df.columns.tolist()}") st.stop()

Filtro por distrito

zonas = sorted(df['distrito'].unique()) distrito = st.selectbox("Selecciona un distrito:", ['Todos'] + zonas)

Filtro por nombre de proyecto

nombre_busqueda = st.text_input("Buscar por nombre del proyecto:")

Filtrar datos

if distrito != 'Todos': df = df[df['distrito'] == distrito]

if nombre_busqueda: df = df[df['nombre'].str.contains(nombre_busqueda, case=False)]

Mapa interactivo

if not df.empty: mapa = folium.Map(location=[-12.0464, -77.0428], zoom_start=12) for _, row in df.iterrows(): folium.Marker( location=[row['lat'], row['lon']], popup=f"<a href='{row['link']}' target='_blank'>{row['nombre']}</a>", tooltip=row['nombre'], icon=folium.Icon(color='blue', icon='home') ).add_to(mapa)

st.markdown("## Mapa de Proyectos")
st_data = st_folium(mapa, width=1000, height=500)

st.markdown("## Lista de Proyectos")
df_display = df[['nombre', 'distrito', 'link']].rename(columns={
    'nombre': 'Nombre del Proyecto',
    'distrito': 'Distrito',
    'link': 'Enlace'
})
df_display['Enlace'] = df_display['Enlace'].apply(lambda url: f"[Ver proyecto]({url})")
st.write(df_display.to_markdown(index=False), unsafe_allow_html=True)

else: st.warning("No hay proyectos para mostrar con los filtros seleccionados.")

