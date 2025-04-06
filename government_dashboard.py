import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datasets
ocupacion = pd.read_csv("data/ocupacion_hotelera.csv")
opiniones = pd.read_csv("data/opiniones_turisticas.csv")
rutas = pd.read_csv("data/rutas_turisticas.csv")
transporte = pd.read_csv("data/uso_transporte.csv")
sostenibilidad = pd.read_csv("data/datos_sostenibilidad.csv")

st.set_page_config(page_title="GreenLake Village Dashboard", layout="wide")
st.title("🌿 GreenLake Village - Panel de Turismo Inteligente")

# Menú de navegación
menu = st.sidebar.radio("Selecciona una sección:", [
    "Visión General",
    "Opiniones y Ranking de Hoteles",
    "Rutas Turísticas",
    "Uso del Transporte",
    "Indicadores de Sostenibilidad"
])

# Sección: Visión General
if menu == "Visión General":
    st.header("📊 Visión General del Destino")
    col1, col2, col3 = st.columns(3)

    with col1:
        ocupacion_media = ocupacion["tasa_ocupacion"].mean()
        st.metric("Ocupación Hotelera Promedio", f"{ocupacion_media:.2f}%")

    with col2:
        rutas_activas = rutas["ruta_nombre"].nunique()
        st.metric("Rutas Activas", rutas_activas)

    with col3:
        satisfaccion = opiniones["puntuacion"].mean()
        st.metric("Satisfacción Promedio", f"{satisfaccion:.1f}/5")

    st.subheader("Ocupación Hotelera por Fecha")
    fig = px.line(ocupacion, x="fecha", y="tasa_ocupacion", title="Evolución de Ocupación Hotelera")
    st.plotly_chart(fig, use_container_width=True)

# Sección: Opiniones
elif menu == "Opiniones y Ranking de Hoteles":
    st.header("💬 Opiniones y Ranking de Hoteles")
    tipo = st.selectbox("Selecciona tipo de turista:", opiniones["tipo_servicio"].unique())
    filtrado = opiniones[opiniones["tipo_servicio"] == tipo]
    promedio = filtrado.groupby("nombre_servicio")["puntuacion"].mean().reset_index().sort_values(by="puntuacion", ascending=False)
    st.subheader("Ranking de Hoteles")
    st.dataframe(promedio)

    fig2 = px.bar(promedio.head(10), x="nombre_servicio", y="puntuacion", title="Top 10 Servicios por Satisfacción", color="puntuacion")
    st.plotly_chart(fig2, use_container_width=True)

# Sección: Rutas Turísticas
elif menu == "Rutas Turísticas":
    st.header("🗺️ Rutas Turísticas")
    categoria = st.selectbox("Filtrar por tipo de ruta:", rutas["tipo_ruta"].unique())
    rutas_filtradas = rutas[rutas["tipo_ruta"] == categoria]
    st.dataframe(rutas_filtradas)

# Sección: Transporte
elif menu == "Uso del Transporte":
    st.header("🚌 Uso del Transporte Turístico")
    fig3 = px.line(transporte, x="fecha", y="num_usuarios", color="tipo_transporte", title="Uso del Transporte por Tipo")
    st.plotly_chart(fig3, use_container_width=True)

# Sección: Sostenibilidad
elif menu == "Indicadores de Sostenibilidad":
    st.header("🌱 Indicadores de Sostenibilidad")
    st.dataframe(sostenibilidad)

    fig4 = px.line(sostenibilidad, x="fecha", y="consumo_energia_kwh", title="Consumo Energético de Hoteles")
    st.plotly_chart(fig4, use_container_width=True)
