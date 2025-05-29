import streamlit as st
import pandas as pd
import pydeck as pdk
import json

st.set_page_config(page_title="Proyectos Urbania", layout="wide")

st.title("🏘️ Proyectos Inmobiliarios en Lima - 2025 (Datos Reales)")
st.markdown("Consulta proyectos nuevos extraídos de Urbania, actualizados automáticamente.")

try:
    with open("urbania_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        df = pd.DataFrame(data)
except Exception as e:
    st.error("No se pudo cargar el archivo de datos.")
    st.stop()

distritos = df['distrito'].dropna().unique()
distrito_seleccionado = st.selectbox("Selecciona un distrito", sorted(distritos))
df_filtrado = df[df["distrito"] == distrito_seleccionado]

if not df_filtrado.empty:
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=df_filtrado["lat"].mean(),
            longitude=df_filtrado["lon"].mean(),
            zoom=13,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df_filtrado,
                get_position='[lon, lat]',
                get_color='[0, 100, 200, 160]',
                get_radius=60,
            ),
        ],
    ))

st.dataframe(df_filtrado.reset_index(drop=True))