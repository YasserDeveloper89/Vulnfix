import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- Configuración de la página ---
st.set_page_config(page_title="LimaProp", layout="wide")

st.title("🧭 LimaProp - Buscador de Proyectos Inmobiliarios")
st.markdown("Explora proyectos inmobiliarios en Lima de forma interactiva.")

# --- Cargar datos ---
try:
    df = pd.read_json("data_urbania.json")

    # Verificar columnas necesarias
    required_columns = {"nombre", "distrito", "lat", "lon", "link", "precio", "tipo"}
    if not required_columns.issubset(set(df.columns)):
        st.error(f"El archivo de datos no contiene todas las columnas necesarias.\nSe requieren: {required_columns}\nColumnas actuales: {set(df.columns)}")
        st.stop()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# --- Filtros ---
st.sidebar.header("🔎 Filtros")

distritos = df["distrito"].unique()
distrito_seleccionado = st.sidebar.selectbox("Selecciona un distrito", options=sorted(distritos))

tipos_disponibles = df["tipo"].unique()
tipo_seleccionado = st.sidebar.multiselect("Tipo de propiedad", options=sorted(tipos_disponibles), default=list(tipos_disponibles))

precio_min, precio_max = int(df["precio"].min()), int(df["precio"].max())
rango_precios = st.sidebar.slider("Rango de precio (S/.)", min_value=precio_min, max_value=precio_max, value=(precio_min, precio_max))

# --- Aplicar filtros ---
df_filtrado = df[
    (df["distrito"] == distrito_seleccionado) &
    (df["tipo"].isin(tipo_seleccionado)) &
    (df["precio"] >= rango_precios[0]) &
    (df["precio"] <= rango_precios[1])
]

# --- Mapa interactivo ---
st.subheader(f"📍 Proyectos en {distrito_seleccionado}")
mapa = folium.Map(location=[-12.1, -77.03], zoom_start=13)

for _, row in df_filtrado.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"{row['nombre']}<br><a href='{row['link']}' target='_blank'>Ver proyecto</a>",
        tooltip=row["nombre"],
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(mapa)

st_data = st_folium(mapa, width=900, height=500)

# --- Lista de resultados ---
st.subheader("📄 Lista de proyectos")

if df_filtrado.empty:
    st.warning("No se encontraron proyectos con los filtros seleccionados.")
else:
    for _, row in df_filtrado.iterrows():
        with st.expander(row["nombre"]):
            st.write(f"**Distrito:** {row['distrito']}")
            st.write(f"**Tipo:** {row['tipo']}")
            st.write(f"**Precio:** S/. {int(row['precio']):,}".replace(",", "."))
            st.markdown(f"[🔗 Ver proyecto]({row['link']})", unsafe_allow_html=True)
