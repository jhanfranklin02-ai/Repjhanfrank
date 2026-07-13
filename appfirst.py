import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistente de Decisiones Críticas", layout="wide")

st.title("🎯 Mi Asistente de Decisiones con Propósito")
st.write("Neutraliza el ego y alinea tus decisiones diarias con tu realidad y principios.")

# --- BARRA LATERAL: PRINCIPIOS Y GUÍA ---
with st.sidebar:
    st.header("⚙️ Guía de Calibración")
    
    st.markdown("""
    ### 🧭 Criterios Esenciales
    Como adventista, considera incluir siempre filtros como:
    * **Alineación Espiritual:** ¿Esto afecta mi comunión con Dios o el sábado?
    * **Salud y Bienestar:** ¿Respeta el templo del Espíritu Santo?
    * **Propósito y Servicio:** ¿Me permite servir a los demás?
    
    ### ⚖️ Escala de Pesos (1 al 5)
    * **5 - Crítico / No negociable:** Principios de fe, valores inquebrantables, prioridades máximas.
    * **4 - Muy importante:** Impacto fuerte a corto plazo (estudios, empresa).
    * **3 - Deseable:** Es importante, pero flexible.
    * **2 - Secundario:** Un beneficio extra.
    * **1 - Ruido / Ego:** Validación externa, caprichos o el qué dirán.
    """)

# --- INICIALIZACIÓN DE LA MEMORIA DE LA APP (SESSION STATE) ---
if "lista_opciones" not in st.session_state:
    st.session_state.lista_opciones = ["UNC + Foco Empresa", "Esperar + Extranjero"]

if "lista_criterios" not in st.session_state:
    st.session_state.lista_criterios = [
        "Alineación con mis principios y fe (Adventista)",
        "Impacto inmediato en mi empresa / negocio",
        "Factor Tiempo / Rapidez en avanzar",
        "Espacio para autoaprendizaje (Software)",
        "Validación externa / Prestigio (Ego)"
    ]

# --- SECCIÓN 1: GESTIÓN DE OPCIONES ---
st.subheader("1. Opciones a Evaluar")
st.write("Añade las alternativas que estás comparando.")

# Layout para agregar opción
col_add_op, _ = st.columns([2, 2])
with col_add_op:
    nueva_opcion = st.text_input("Escribe una nueva opción:", key="input_nueva_op")
    if st.button("➕ Agregar Opción"):
        if nueva_opcion.strip() != "" and nueva_opcion not in st.session_state.lista_opciones:
            st.session_state.lista_opciones.append(nueva_opcion.strip())
            st.rerun()

# Mostrar opciones actuales con botón de eliminar
cols_opciones = st.columns(len(st.session_state.lista_opciones) if st.session_state.lista_opciones else 1)
opciones_a_eliminar = []

for idx, op in enumerate(st.session_state.lista_opciones):
    with cols_opciones[idx]:
        st.info(f"**{op}**")
        if st.button(f"🗑️ Eliminar", key=f"del_op_{idx}"):
            opciones_a_eliminar.append(op)

if opciones_a_eliminar:
    for op in opciones_a_eliminar:
        st.session_state.lista_opciones.remove(op)
    st.rerun()

st.markdown("---")

# --- SECCIÓN 2: GESTIÓN DE CRITERIOS ---
st.subheader("2. Criterios de Evaluación")
st.write("Define los filtros por los que pasarás esta decisión.")

col_add_crit, _ = st.columns([2, 2])
with col_add_crit:
    nuevo_criterio = st.text_input("Escribe un nuevo criterio:", key="input_nuevo_crit")
    if st.button("➕ Agregar Criterio"):
        if nuevo_criterio.strip() != "" and nuevo_criterio not in st.session_state.lista_criterios:
            st.session_state.lista_criterios.append(nuevo_criterio.strip())
            st.rerun()

st.markdown("### 📊 Panel de Votación")
criterios_datos = []
criterios_a_eliminar = []

# Crear los deslizadores dinámicamente para cada criterio y cada opción
for i, crit in enumerate(st.session_state.lista_criterios):
    with st.expander(f"🔹 {crit}", expanded=True):
        col_crit_info, col_controles = st.columns([1, 2])
        
        with col_crit_info:
            st.write(f"**Criterio #{i+1}**")
            if st.button("🗑️ Eliminar Criterio", key=f"del_crit_{i}"):
                criterios_a_eliminar.append(crit)
        
        with col_controles:
            # Deslizador para el peso del criterio
            peso = st.slider(f"Importancia / Peso", 1, 5, 3, key=f"peso_{i}", help="5 = Crítico (Principios), 1 = Ruido (Ego)")
            
            # Crear un deslizador de nota para cada opción disponible
            notas_opciones = {}
            cols_notas = st.columns(len(st.session_state.lista_opciones) if st.session_state.lista_opciones else 1)
            
            for j, op in enumerate(st.session_state.lista_opciones):
                with cols_notas[j]:
                    nota = st.slider(f"Nota para {op}", 1, 10, 5, key=f"nota_{i}_{j}")
                    notas_opciones[op] = nota

        # Guardar datos para los cálculos
        fila = {"Criterio": crit, "Peso": peso}
        for op, nota in notas_opciones.items():
            fila[f"Nota {op}"] = nota
            fila[f"Puntaje {op}"] = peso * nota
        criterios_datos.append(fila)

if criterios_a_eliminar:
    for crit in criterios_a_eliminar:
        st.session_state.lista_criterios.remove(crit)
    st.rerun()

# --- SECCIÓN 3: RESULTADOS ---
st.markdown("---")
st.subheader("📊 Resultados de la Matriz")

if len(st.session_state.lista_opciones) < 2:
    st.warning("⚠️ Necesitas al menos 2 opciones para poder realizar una comparación.")
elif len(criterios_datos) == 0:
    st.warning("⚠️ Agrega al menos un criterio para calcular los puntajes.")
else:
    df = pd.DataFrame(criterios_datos)
    
    # Calcular totales
    totales = {}
    for op in st.session_state.lista_opciones:
        totales[op] = df[f"Puntaje {op}"].sum()
    
    # Encontrar al ganador
    ganador = max(totales, key=totales.get)
    max_puntaje = totales[ganador]
    
    # Verificar si hay un empate
    valores = list(totales.values())
    if valores.count(max_puntaje) > 1:
        st.warning(f"⚖️ **Empate Técnico:** Varias opciones alcanzaron {max_puntaje} puntos. Revisa los pesos de tus principios espirituales o de negocio para desempatar.")
    else:
        st.success(f"🏆 **Decisión Óptima:** **{ganador}** con **{max_puntaje} puntos**. Esta opción es la que mejor protege tu esencia, tus metas y tu paz actual.")
        
    # Mostrar puntajes resumidos
    st.write("### Resumen de Puntajes:")
    for op, total in totales.items():
        st.write(f"* **{op}:** {total} puntos")
        
    # Mostrar tabla completa de ingeniería
    st.markdown("#### Detalle Analítico:")
    st.dataframe(df, use_container_width=True)
