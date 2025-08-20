import streamlit as st
import requests
import os

# Define la URL de tu backend
BACKEND_URL = "http://127.0.0.1:5000/process-excel"

# Configuración de la página web
st.set_page_config(page_title="Agente IA para Excel", page_icon="🤖")
st.title("🤖 Agente IA para Excel")
st.markdown("Sube un archivo de Excel (.xlsx) y dame una instrucción en lenguaje natural.")

# Interfaz de usuario para subir el archivo y escribir la instrucción
uploaded_file = st.file_uploader("Sube tu archivo de Excel:", type=["xlsx"])
instruction = st.text_area("Instrucción para el Agente IA:", height=100)

# El botón que inicia el proceso
if st.button("Procesar Archivo"):
    if uploaded_file is not None and instruction:
        with st.spinner('Procesando... esto puede tomar un momento.'):
            files = {'file': uploaded_file.getvalue()}
            data = {'instruction': instruction}
            
            # Envía la petición al backend de Flask
            try:
                response = requests.post(BACKEND_URL, files=files, data=data)
                
                if response.status_code == 200:
                    st.success("¡Archivo procesado con éxito!")
                    
                    # Botón para descargar el archivo modificado
                    st.download_button(
                        label="Descargar Archivo Modificado",
                        data=response.content,
                        file_name="archivo_modificado.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error(f"Error en el servidor: {response.json().get('error', 'Error desconocido')}")
            
            except requests.exceptions.ConnectionError:
                st.error("No se pudo conectar al backend. Asegúrate de que el servidor Flask esté corriendo.")
    else:
        st.warning("Por favor, sube un archivo e ingresa una instrucción.")