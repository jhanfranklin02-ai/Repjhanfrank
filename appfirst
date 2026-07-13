import streamlit as st
import pandas as pd

st.set_page_config(page_title="Matriz de Decisión Ponderada", layout="wide")

st.title("Mi Asistente de Decisiones Críticas")
st.write("Calibra tus opciones basándote en tu realidad actual, neutralizando el ego.")

# 1. Entrada de Opciones
st.subheader("1. Define las Opciones a Evaluar")
col1, col2 = st.columns(2)
with col1:
    opcion_a = st.text_input("Nombre de la Opción A:", value="Opción A")
with col2:
    opcion_b = st.text_input("Nombre de la Opción B:", value="Opción B")

# 2. Definición de Criterios y Pesos
st.subheader("2. Define los Criterios de Evaluación y sus Pesos (1 al 5)")
st.info("Escala de Pesos: 5 = Crítico/No negociable, 3 = Deseable, 1 = Ruido/Ego")

criterios_def = [
    {"nombre": "Impacto a Futuro (Empresa/Metas)", "default_peso": 5},
    {"nombre": "Factor Tiempo / Rapidez", "default_peso": 4},
    {"nombre": "Viabilidad Financiera / Costo", "default_peso": 3},
    {"nombre": "Espacio para Autoaprendizaje (Software)", "default_peso": 4},
    {"nombre": "Validación Externa / Prestigio (Ego)", "default_peso": 1}
]

criterios_datos = []

for i, crit in enumerate(criterios_def):
    with st.expander(f"🔹 Criterio: {crit['nombre']}", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            peso = st.slider(f"Peso del Criterio", 1, 5, crit['default_peso'], key=f"peso_{i}")
        with c2:
            nota_a = st.slider(f"Calificación para {opcion_a} (1-10)", 1, 10, 5, key=f"nota_a_{i}")
        with c3:
            nota_b = st.slider(f"Calificación para {opcion_b} (1-10)", 1, 10, 5, key=f"nota_b_{i}")
            
        criterios_datos.append({
            "Criterio": crit['nombre'],
            "Peso": peso,
            f"Nota {opcion_a}": nota_a,
            f"Puntaje {opcion_a}": peso * nota_a,
            f"Nota {opcion_b}": nota_b,
            f"Puntaje {opcion_b}": peso * nota_b
        })

# 3. Procesamiento y Resultados
df = pd.DataFrame(criterios_datos)

total_a = df[f"Puntaje {opcion_a}"].sum()
total_b = df[f"Puntaje {opcion_b}"].sum()

st.markdown("---")
st.subheader("📊 Resultados de la Evaluación")

# Mostrar Ganador
if total_a > total_b:
    st.success(f"🏆 La opción ganadora es: **{opcion_a}** con **{total_a} puntos** (Frente a {total_b} de {opcion_b})")
elif total_b > total_a:
    st.success(f"🏆 La opción ganadora es: **{opcion_b}** con **{total_b} puntos** (Frente a {total_a} de {opcion_a})")
else:
    st.warning(f"⚖️ Hay un empate técnico con **{total_a} puntos**. Revisa o calibra los pesos.")

# Mostrar tabla detallada
st.dataframe(df, use_container_width=True)
