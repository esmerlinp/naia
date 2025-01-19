import streamlit as st
from app.config import RRHH_HEADERS
from app.utils import jwt_decode
import os

# relative_path = './assets/logo.png'
# full_path = os.path.join(os.getcwd(), relative_path)
# path = os.path.abspath(full_path)
url_test_api = "http://rrhh.administracionapi.camsoft.com.do:8086"
if "sourceUrl" in st.query_params:   
    st.session_state.baseUrl = st.query_params.sourceUrl
    st.session_state.testVersion = False
    if st.session_state.baseUrl == url_test_api:
        st.session_state.testVersion = True
    
else:
    st.session_state.baseUrl = url_test_api
    st.session_state.testVersion = True


st.session_state.errorMessage =  ""

# Obtener los parámetros de la URL

if "embed" in st.query_params:
    is_embed = st.query_params.embed
    
    
if "is_auth" not in st.session_state:
    st.session_state.is_auth = False

def load_initial_data():
    if "token" in st.query_params:
        RRHH_HEADERS["Authorization"] = f"Bearer {st.query_params.token}"
        
        #Obtener info del usuario
        user = jwt_decode(st.query_params.token)
        
        if user:
            st.session_state.is_auth = True
            st.session_state.userId = user["userId"]
            st.session_state.userEmail = user["userEmail"]
            st.session_state.FullUserName = user["FullUserName"]
            st.session_state.userName = user["userName"]
            st.session_state.userCompany = user["userCompany"]
            st.session_state.userCompany = user["userCompany"]
            
    else:
        st.session_state.is_auth = False
        st.session_state.errorMessage = """
        **Error de autenticación:**  
        No puedes autenticarte o no tienes permisos para acceder a esta funcionalidad.  
        Por favor, contacta a un administrador para obtener más información o asistencia.
        """
        return
    
    RRHH_HEADERS["x-api-key"] = os.getenv("X_API_KEY")
    if not RRHH_HEADERS["x-api-key"]:
        st.session_state.is_auth = False
        st.session_state.errorMessage = """**Error de configuración:**  
        Debes agregar la variable de entorno X_API_KEY a tu servidor. contacta al administrador del sistema."""
        return
        
    
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY")
    if not st.session_state.openai_api_key:
        st.session_state.is_auth = False
        st.session_state.errorMessage = """**Error de configuración:**  
        Debes agregar la variable de entorno OPENAI_API_KEY a tu servidor. Contacta al administrador del sistema."""
        return
        

load_initial_data()

pages = {
    "Asistente de Recursos Humanos": [
        st.Page("./app/pages/chat.py", title="Chat experimental"),
        st.Page("./app/pages/roadmap.py", title="Roadmap"),
        #st.Page("./app/pages/chat_config.py", title="Configuración"),
    ]
}

pg = st.navigation(pages)
pg.run()


    


    