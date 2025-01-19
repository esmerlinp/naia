import streamlit as st
import pandas as pd
import os
from app.database import Database


st.set_page_config(
    page_title="config",
    page_icon=":material/support_agent:",
    layout="centered",
)

@st.dialog("Add data")
def new_external(file_name):
    name = st.text_input("name", value=file_name)
    description = st.text_input("description")
    key_words = st.text_input("key words", help="palabras claves para ayudar al asistente a identificar el contenido del archivo, separadas por comas, eje:  empleados, nomina_externa")
    _, _, col, col1 = st.columns(4)
    with col:
        if st.button("save"):
            db = Database()
            
            relative_path = f'./app/data/external/{name}.csv'
            full_path = os.path.join(os.getcwd(), relative_path)
            ruta = os.path.abspath(full_path)
            df.to_csv(ruta, index=False)  # index=False para no guardar el índice en el archivo
            db.insert_fuente_datos(name=name, description=description, key_words=key_words, path_file=relative_path)
            st.rerun()
            st.toast('Su fuente de datos ha sido guardada!', icon='✅')
            
        
    with col1:
        if st.button("cancel"):
            pass
            
    
        
st.header("Fuente de datos externa")
uploaded_file = st.file_uploader("Carga tu archivo CSV y el asistente responderá preguntas detalladas")
if uploaded_file is not None:

    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    
    # Guardar el DataFrame en una ruta local como archivo CSV
    if st.button("save file"):
        new_external(file_name=uploaded_file.name)
