import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Cargar datos JSON
try:
    df = pd.read_json("data_urbania.json")
    required_columns = {"nombre", "distrito", "tipo", "precio", "lat", "lon", "link"}
    if not required_columns.issubset(df.columns):
        st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: {required_columns}\nColumnas actuales: {set(df.columns)}")
        st.stop()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

st.set_page_config(page_title="LimaProp Premium", layout="wide")

# Título y portada
st.image("portada_limaprop.png", use_column_width=True)
st.markdown("<h1 style='text-align: center; color: #3366cc;'>LimaProp Premium</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Explora los mejores proyectos inmobiliarios de Lima en tiempo real.</p>", unsafe_allow_html=True)

# Filtros
with st.sidebar:
    st.header("Filtrar proyectos")
    distrito = st.selectbox("Distrito", options=["Todos"] + sorted(df["distrito"].unique().tolist()))
    tipo = st.selectbox("Tipo de propiedad", options=["Todos"] + sorted(df["tipo"].unique().tolist()))
    precio_min = st.number_input("Precio mínimo (S/)", min_value=0, value=0, step=50000)
    precio_max = st.number_input("Precio máximo (S/)", min_value=0, value=1000000, step=50000)

# Aplicar filtros
df_filtrado = df.copy()
if distrito != "Todos":
    df_filtrado = df_filtrado[df_filtrado["distrito"] == distrito]
if tipo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo"] == tipo]
df_filtrado = df_filtrado[(df_filtrado["precio"] >= precio_min) & (df_filtrado["precio"] <= precio_max)]

# Mapa
if not df_filtrado.empty:
    m = folium.Map(location=[-12.06, -77.04], zoom_start=12)
    for _, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            tooltip=row["nombre"],
            popup=f'<a href="{row["link"]}" target="_blank">{row["nombre"]}</a>'
        ).add_to(m)
    st_folium(m, width=700, height=450)
else:
    st.warning("No se encontraron proyectos con los filtros seleccionados.")

# Mostrar tarjetas
st.markdown("### Lista de Proyectos")
for _, row in df_filtrado.iterrows():
    with st.container():
        st.markdown(f"""
        <div style="border:1px solid #ccc; border-radius:10px; padding:15px; margin-bottom:15px;">
            <strong>{row['nombre']}</strong><br>
            <span style="color:gray;">{row['distrito']} • {row['tipo']}</span><br>
            <span style="color:#009933;"><strong>S/ {row['precio']:,}</strong></span><br>
            <a href="{row['link']}" target="_blank">Ver más detalles</a>
        </div>
        """, unsafe_allow_html=True)
