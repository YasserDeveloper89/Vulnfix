import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="LimaProp", layout="wide")

# ---------- Cargar datos ----------
try:
    df = pd.read_json("data_urbania.json")
    required_cols = {'nombre', 'distrito', 'lat', 'lon', 'link'}
    if not required_cols.issubset(df.columns):
        st.error("❌ El archivo de datos no contiene todas las columnas necesarias.")
        st.stop()
except Exception as e:
    st.error(f"❌ Error al cargar los datos: {e}")
    st.stop()

# ---------- Título y portada ----------
st.markdown("<h1 style='text-align: center;'>🏠 LimaProp</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>Explora proyectos inmobiliarios por distrito</h3>", unsafe_allow_html=True)

# ---------- Selector de distrito ----------
distritos = sorted(df["distrito"].unique())
distrito_seleccionado = st.selectbox("Selecciona un distrito", distritos)

df_distrito = df[df["distrito"] == distrito_seleccionado]

# ---------- Mapa interactivo ----------
if not df_distrito.empty:
    m = folium.Map(location=[df_distrito["lat"].mean(), df_distrito["lon"].mean()], zoom_start=15)
    for _, row in df_distrito.iterrows():
        popup_html = f"<b>{row['nombre']}</b><br><a href='{row['link']}' target='_blank'>Ver proyecto</a>"
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup_html,
            tooltip=row["nombre"]
        ).add_to(m)

    st_folium(m, height=500, width=1000)
else:
    st.warning("⚠️ No hay datos para este distrito.")

# ---------- Lista de proyectos (tarjetas) ----------
st.subheader("📋 Lista de Proyectos")

if df_distrito.empty:
    st.info("No se encontraron proyectos para esta zona.")
else:
    for _, row in df_distrito.iterrows():
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 12px; background-color: #f9f9f9;">
            <h4 style="margin: 0; color: #2c3e50;">🏘️ {row['nombre']}</h4>
            <p style="margin: 4px 0;"><strong>Distrito:</strong> {row['distrito']}</p>
            <a href="{row['link']}" target="_blank" style="color: #ffffff; background-color: #007bff; padding: 6px 12px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 6px;">🔗 Ver proyecto</a>
        </div>
        """, unsafe_allow_html=True)
