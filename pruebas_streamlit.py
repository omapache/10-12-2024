import streamlit as st
import pandas as pd
import numpy as np

# Título principal
st.title("🧪 Laboratorio de Pruebas Streamlit")

# Sidebar (menú lateral)
with st.sidebar:
    st.header("Configuración")
    nombre = st.text_input("¿Cómo te llamas?")
    edad = st.slider("Edad", 0, 100, 25)
    me_gusta_pizza = st.checkbox("¿Te gusta la pizza?")

# Tabs (pestañas)
tab1, tab2, tab3 = st.tabs(["Textos", "Datos", "Widgets"])

# Pestaña 1: Textos
with tab1:
    st.header("Ejemplos de Texto")
    
    st.write("### Texto normal")
    st.write("Esto es un texto normal")
    
    st.markdown("### Markdown")
    st.markdown("**negrita** y *cursiva*")
    
    with st.expander("Haz clic para ver más"):
        st.write("¡Contenido oculto!")

# Pestaña 2: Datos
with tab2:
    st.header("Ejemplos con Datos")
    
    # Crear un DataFrame de ejemplo
    df = pd.DataFrame({
        'nombre': ['Ana', 'Juan', 'María'],
        'edad': [25, 30, 35],
        'ciudad': ['Madrid', 'Barcelona', 'Sevilla']
    })
    
    st.write("### DataFrame:")
    st.dataframe(df)
    
    st.write("### Gráfica:")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )
    st.line_chart(chart_data)

# Pestaña 3: Widgets
with tab3:
    st.header("Widgets Interactivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Inputs Básicos")
        texto = st.text_input("Escribe algo")
        numero = st.number_input("Elige un número", 0, 100)
        fecha = st.date_input("Selecciona una fecha")
    
    with col2:
        st.write("### Selecciones")
        opcion = st.selectbox(
            "Elige una opción",
            ["Opción 1", "Opción 2", "Opción 3"]
        )
        opciones = st.multiselect(
            "Selecciona varios",
            ["A", "B", "C", "D"]
        )

# Botones y Mensajes
st.header("Botones y Mensajes")
if st.button("¡Haz clic!"):
    st.balloons()
    st.success("¡Éxito!")
    st.warning("Advertencia")
    st.error("Error")
    st.info("Información")

# Mostrar los datos de la sidebar
st.header("Datos del Usuario")
if nombre:
    st.write(f"👋 Hola {nombre}!")
    st.write(f"🎂 Tienes {edad} años")
    st.write(f"🍕 {'Te gusta' if me_gusta_pizza else 'No te gusta'} la pizza") 