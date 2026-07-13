import streamlit as st
import pandas as pd

st.set_page_config(page_title="Matriz de Decisión Analítica", layout="wide")

st.title("🎯 Mi Asistente de Decisiones Críticas")
st.write("Neutraliza el ego y calibra tus opciones basándote en tu realidad actual.")

# --- EXPLICACIÓN DE REGLAS ---
with st.sidebar:
    st.header("⚙️ Guía de Calibración")
    
    st.markdown("""
    ### ⚖️ Escala de Pesos (1 al 5)
    *Determina qué tan importante es este factor hoy en tu vida.*
    * **5 - Crítico / No negociable:** Si falla aquí, la opción se descarta por completo.
    * **4 - Muy importante:** Impacto directo en tu bienestar o negocio a corto plazo.
    * **3 - Deseable:** Importante, pero puedes compensarlo por otra vía.
    * **2 - Secundario:** Es un "plus", pero no define el éxito.
    * **1 - Ruido / Capricho / Ego:** Validación externa o el "qué dirán".
    
    ### 📊 Escala de Puntuación (1 al 10)
    *Cómo cumple cada opción con el criterio.*
    * **9 a 10:** Lo resuelve de inmediato, sin riesgos y con mínimo esfuerzo.
    * **6 a 8:** Cumple bien, pero exige un esfuerzo extra o disciplina.
    * **3 a 5:** Insuficiente. Apenas roza el mínimo o pone trabas.
    * **1 a 2:** Nulo o altamente riesgoso.
    """)

# --- SECCIÓN 1: DEFINIR OPCIONES ---
st.subheader("1. Define las Opciones a Evaluar")
col_op1, col_op2 = st.columns(2)
with col_op1:
    opcion_a = st.text_input("Nombre de la Opción A:", value="UNC + Foco Empresa")
with col_op2:
    opcion_b = st.text_input("Nombre de la Opción B:", value="Esperar + Extranjero")

st.markdown("---")

# --- SECCIÓN 2: ENTRADA DINÁMICA DE CRITERIOS ---
st.subheader("2. Define tus Criterios Personalizados")
st.write("Escribe abajo los criterios que vas a evaluar. Deja en blanco los que no uses.")

# Inicializamos 5 filas por defecto, pero puedes escribir los nombres que quieras
criterios_por_defecto = [
    "Impacto inmediato en mi empresa / negocio",
    "Factor Tiempo / Rapidez en obtener el grado",
    "Espacio para autoaprendizaje (Software/Programación)",
    "Viabilidad financiera actual",
    "Validación externa / Prestigio ante amigos (Ego)"
]

criterios_usuario = []

# Creamos los bloques de votación
for i in range(5):
    nombre_sugerido = criterios_por_defecto[i] if i < len(criterios_por_defecto) else ""
    nombre_crit = st.text_input(f"Criterio #{i+1}:", value=nombre_sugerido, key=f"nom_crit_{i}")
    
    if nombre_crit.strip() != "":
        # Si el usuario escribió un criterio, abrimos los controles para puntuarlo
        with st.container():
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                peso = st.slider(
                    f"Importancia de: '{nombre_crit}'", 
                    1, 5, 3, 
                    key=f"peso_{i}",
                    help="5 = Crítico, 3 = Deseable, 1 = Ruido/Ego"
                )
            with c2:
                nota_a = st.slider(
                    f"Nota para {opcion_a}", 
                    1, 10, 5, 
                    key=f"nota_a_{i}",
                    help="10 = Excelente/Inmediato, 1 = Nulo/Imposible"
                )
            with c3:
                nota_b = st.slider(
                    f"Nota para {opcion_b}", 
                    1, 10, 5, 
                    key=f"nota_b_{i}",
                    help="10 = Excelente/Inmediato, 1 = Nulo/Imposible"
                )
            
            criterios_usuario.append({
                "Criterio": nombre_crit,
                "Peso": peso,
                f"Nota {opcion_a}": nota_a,
                f"Puntaje {opcion_a}": peso * nota_a,
                f"Nota {opcion_b}": nota_b,
                f"Puntaje {opcion_b}": peso * nota_b
            })
            st.markdown("<br>", unsafe_allow_html=True)

# --- SECCIÓN 3: PROCESAMIENTO Y RESULTADOS ---
if len(criterios_usuario) > 0:
    df = pd.DataFrame(criterios_usuario)
    
    total_a = df[f"Puntaje {opcion_a}"].sum()
    total_b = df[f"Puntaje {opcion_b}"].sum()
    
    st.markdown("---")
    st.subheader("📊 Tabla de Resultados Finales")
    
    # Cartel del ganador destacado
    if total_a > total_b:
        st.success(f"🏆 **Decisión Óptima:** Elije **{opcion_a}** con **{total_a} puntos** (Frente a {total_b} de {opcion_b}). Esta opción se alinea mejor con lo que de verdad te importa hoy.")
    elif total_b > total_a:
        st.success(f"🏆 **Decisión Óptima:** Elije **{opcion_b}** con **{total_b} puntos** (Frente a {total_a} de {opcion_a}). Esta opción destaca en los pilares que ponderaste más alto.")
    else:
        st.warning(f"⚖️ **Empate Técnico:** Ambas opciones suman **{total_a} puntos**. Ve a la barra lateral, revisa los pesos y ajusta con más rigurosidad.")
        
    # Mostrar la tabla limpia en pantalla
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Escribe al menos un criterio arriba para calcular el resultado.")
