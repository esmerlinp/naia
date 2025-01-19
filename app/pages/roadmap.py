import streamlit as st
import os
import pandas as pd

# Título y descripción general del proyecto


st.set_page_config(
    page_title="Assistant",
    page_icon=":material/support_agent:",
    layout="wide",
    initial_sidebar_state="expanded",
)

relative_path = './assets/logo.png' 
full_path = os.path.join(os.getcwd(), relative_path)
path = os.path.abspath(full_path)


col1, _, _, _ = st.columns([0.3, 1, 1.5, 0.4])
with col1:
    st.image(f"{path}", width=100)

st.header("Assistant roadmap")

st.write(
    """
    Este roadmap detalla las fases de desarrollo y el progreso de cada funcionalidad clave del proyecto de chat con 
    inteligencia artificial, diseñado para interactuar con los datos de empleados, nóminas y reclutamiento. 
    """
)
st.success("v0.1.0", icon="💥")
# Descripción del orden de desarrollo
st.subheader("Orden de Desarrollo")
st.info(
    """
    El desarrollo seguirá el siguiente orden para optimizar los tiempos y asegurar la disponibilidad 
    de consultas clave antes de implementar acciones más complejas.
    """
)
st.write("""
1. **Consultas sobre empleados**: Implementar y probar funcionalidades para obtener información detallada de los empleados.
2. **Generación de histogramas**: Completar las funcionalidades para generar gráficos basados en los datos solicitados por los usuarios.
3. **Consultas sobre reclutamiento**: Implementar y probar funcionalidades para consultar información relacionada con los procesos de reclutamiento.
4. **Consultas sobre nómina**: Crear y probar funcionalidades para acceder a la información de nómina de los empleados.
5. **Acciones sobre empleados**: Permitir la realización de acciones específicas sobre empleados, como registrar ausencias para un empleado en particular.
6. **Acciones sobre reclutamiento**: Habilitar acciones específicas para candidatos, como asociar un candidato a una solicitud de empleo.
""")

#st.video("https://camsoftsrl-my.sharepoint.com/:v:/g/personal/epaniagua_camsoft_com_do/EaMAjcDsx5BMlpMMrQQfm3sBU6cYYGL-KQYzj6fftdjsFw")


st.success(body=":blue[NEW]  - :red[Amonestaciones]  -  :red[Desvinculación]", icon="🥳")
# Fases del Roadmap con su porcentaje de progreso
roadmap = {  
    "**Generación de histogramas (charts) y tablas** 👩🏽‍💻 **:green[Testing]** - DateLine 02/11/2024  - ✅ **:green[DONE]**": 100,# Progreso actual   
    "**Consultas sobre empleados**  👩🏽‍💻  **:green[Testing]** - DateLine 15/11/2024 - ✅ **:green[DONE]**": 100,  
    "**Consultas sobre reclutamiento** 👷 :blue[Development] - DateLine 23/12/2024": 5,
    "**Consultas sobre nóminas** 👷 :blue[Development] - DateLine 23/01/2025": 5,
    "**Realizar Acciones sobre empleado**s 👷 :blue[Development] - DateLine 30/03/2025": 1,       # Progreso actual
    "**Realizar acciones sobre reclutamiento** 👷 :blue[Development] - DateLine 25/03/2025 ": 0,
}


st.subheader("Progreso")
# Mostrar el progreso de cada fase
for fase, progreso in roadmap.items():
    st.markdown(fase)
    st.progress(progreso / 100, f"Progreso: **{progreso}%** completado")  
st.divider()
