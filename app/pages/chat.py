import streamlit as st
import time 
from app.llm import LargeLanguageModel
from app.config import DISCLAIMER, INITIAL_MSG
from app.database import Database
from app.utils import is_base64, display_base64_image, es_json_valido
import os
import pandas as pd
import base64
from streamlit_extras.tags import tagger_component
import openai   



st.set_page_config(
    page_title="Assistant",
    page_icon=":material/support_agent:",
    layout="centered",
    initial_sidebar_state="expanded",
)
   
modelos_odoo = {
            "ventas": "sale.order",
            "compras": "purchase.order",
            "contabilidad": "account.move",
            "gastos": "hr.expense",
            "facturacion": "account.move",
            "contactos": "res.partner",
            "proyectos": "project.project",
            "tareas": "project.task",
            "inventario": "stock.picking",
            "produccion": "mrp.production",
            "empleados": "hr.employee",
            "nomina": "hr.payslip",
            "crm": "crm.lead"
        }

if not st.session_state.is_auth:

    # Mensaje de error usando 
    st.markdown(st.session_state.errorMessage, unsafe_allow_html=True)
    
else:       
    
    db = Database()

    # Cargar la última sesión del usuario o crear una nueva si no existe
    if "CURRENT_SESION" not in st.session_state:
        db.get_last_sesion(userId=st.session_state.userId,  userEmail=st.session_state.userEmail)
        st.session_state.CURRENT_SESION = db.CURRENT_SESION

    # Obtener la conversación actual de la sesión
    msgs = db.get_conversation(st.session_state.CURRENT_SESION)
    
    with st.sidebar:
        apikey = st.text_input(label="API KEY", type="password",placeholder="Enter your api key")
        for module in modelos_odoo.keys():
            st.checkbox(module, value=True, disabled=True)


##################################################################################
#CHAT HISTORY  
##################################################################################
    @st.dialog("Chat History")
    def History():
        sesiones = db.get_sesion(userId=st.session_state.userId)
        
        if st.button("Nueva conversación", use_container_width=True):
            # Crear una nueva sesión de chat
            if len(st.session_state.messages) <= 0:
                db.delete_sesion(st.session_state.CURRENT_SESION)
            else:    
                #llm = LargeLanguageModel(api_key=apikey)
                #sesion_title = llm.get_response("genera un titulo relacionado al historial de esta conversacion, solo muestrame el titulo generado", st.session_state.messages)
                sesion_title = st.session_state.messages[0]
                db.update_sesion_description(st.session_state.CURRENT_SESION, sesion_title)
                
            db.create_sesion(userId=st.session_state.userId, userEmail=st.session_state.userEmail)
            st.session_state.CURRENT_SESION = db.CURRENT_SESION
            st.session_state.messages = []
            st.rerun()  # Recargar la interfaz
        
        #st.write("Seleccione o cree un nuevo chat")
        
        search = st.text_input("Buscar conversación...", placeholder="Ingresa texto de la conversación")
        filtered_sesiones = [s for s in sesiones if search.lower() in s[1].lower()]

        if not filtered_sesiones:
            st.write("No se encontraron resultados.")
        else:
            with st.container(height=300):
                for sesion in filtered_sesiones:
                    current_chat = st.session_state.CURRENT_SESION == sesion[0]
                    #print(sesion)
                    if st.button(str(sesion[0]) +"-"+ sesion[1][:35] + "...", help=sesion[1], use_container_width=True, disabled=current_chat):
                        st.session_state.CURRENT_SESION = sesion[0]
                        st.session_state.messages = db.get_conversation(st.session_state.CURRENT_SESION)
                        st.rerun()  # Recargar la interfaz con la nueva conversación
            if st.button(":red[Eliminar historial]", type="primary"):
                delete_history()
    
    
    @st.fragment
    def delete_history():
        st.markdown("""Al confirmar esta acción, se eliminará de forma permanente todo el historial de conversaciones con el asistente.
                    **¿Estás seguro de que deseas continuar?**""")
        _, col_accept, col_cancel = st.columns([2,1,1])
        with col_accept:
            if st.button(":blue[Aceptar]"):
                db.delete_history(st.session_state.userId)
                st.rerun()
        with col_cancel:
            if st.button(":red[Cancelar]"):
                st.rerun()
                
                        



##################################################################################
    # Título central de la página
##################################################################################
    relative_path = './assets/logo.png'
    full_path = os.path.join(os.getcwd(), relative_path)
    path = os.path.abspath(full_path)


    col_image, col_title, col_version, col_button = st.columns([0.3, 1, 1.5, 0.25])
    with col_image:
        st.image(f"{path}", width=40)
    with col_title:
        st.markdown('<h1 style="color:#61a1af; margin-top: -25px;">Assistant</h1>', unsafe_allow_html=True)
    
    if st.session_state.testVersion:
        with col_version:
            tagger_component("", ["🚩 v1.0.0-Testing"], color_name=["lightblue"])
            
    with col_button:
        if st.button("", icon=":material/edit_note:", help="New Chat", use_container_width=True):
            History()
            #st.balloons()
            #delete_history()

    # Sección de Disclaimer
    with st.expander("Disclaimer - Asistente de Recursos Humanos", icon=":material/info:"):
        st.markdown(DISCLAIMER, unsafe_allow_html=True)


    
    # _, col1, col2, col3, _ = st.columns(5)
    # col1.metric("Nómina de Viáticos", "9.5K", "1.2 %", delta_color="inverse")
    # col2.metric("Nómina de Viáticos", "8.5K", "-10%",  delta_color="inverse")
    # col3.metric("Nómina de Viáticos", "12.3K", "4%",  delta_color="inverse")
    
##################################################################################
    # Config Inicial
##################################################################################
    # Mostrar mensajes de la conversación seleccionada
    if "messages" not in st.session_state:
        st.session_state.messages = msgs
        
    #Carga y muestra todos los mensajes 
    for i, message in enumerate(st.session_state.messages):
        role = message['role']
        #image_path =  f"{path}" if role == 'assistant' else "https://www.allprodad.com/wp-content/uploads/2021/03/05-12-21-happy-people.jpg"
        with st.chat_message(role):
            content = message['content']
            if role == 'assistant':
                if is_base64(content):
                    image = display_base64_image(content)                
                    st.image(image, use_column_width=True)
                elif es_json_valido(content):
                    try:
                        df = pd.read_json(content)    
                        st.dataframe(df)
                    except ValueError as e:
                        st.json(content)
                        #print(content)    
                else:    
                    st.caption(content)
            else: 
                st.markdown(content)
            
            if i == (len(st.session_state.messages) -1) and role == 'user' and apikey:
                llm = LargeLanguageModel(api_key=apikey)
                choices = llm.proccess_message(content, st.session_state.messages)
                if isinstance(choices, openai.types.chat.chat_completion.Choice):
                   
                    if choices.message.audio:
                        transcript = choices.message.audio.transcript
                        message = transcript
                        
                        st.caption(transcript)
                        db.insert_conversation(st.session_state.CURRENT_SESION, 'assistant', transcript)
                        st.session_state.messages.append({"role": "assistant", "content": transcript})
                    else:
                        message = choices.message.content
                        st.caption(message)
                        db.insert_conversation(st.session_state.CURRENT_SESION, 'assistant', message)
                        st.session_state.messages.append({"role": "assistant", "content": message})
                        
                elif isinstance(choices, str):
                    message = choices
                    st.caption(message)
                    db.insert_conversation(st.session_state.CURRENT_SESION, 'assistant', message)
                    st.session_state.messages.append({"role": "assistant", "content": message})
                


                
            
            
    #Muestra mensaje inicial del asistente 
    if not st.session_state.messages: 
        with st.chat_message("assistant"):
            placeholder = st.empty()  
            display_text = ""
            for char in INITIAL_MSG:
                display_text += char
                placeholder.markdown(display_text)
                #time.sleep(0.005)   
            st.session_state.messages.append({"role": "assistant", "content": INITIAL_MSG})  
            

##################################################################################
    # INTERACION CON EL USUARIO
##################################################################################
    # Entrada de texto del usuario
       
    prompt = st.chat_input(f"{st.session_state.FullUserName.split()[0]}, escribe tu pregunta o solicitud aquí...", max_chars=12000)
    if prompt:
        
        if not apikey:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        
        
        init_t = time.time()
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            db.insert_conversation(st.session_state.CURRENT_SESION, 'user', prompt)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            timeholder = st.empty()
            audio_placeholder = st.empty()
            message = None
            choices: openai.types.chat.chat_completion.Choice = None
            
            with placeholder:
                with st.spinner("Thinking ..."):
                    llm = LargeLanguageModel(api_key=apikey)
                    choices = llm.proccess_message(prompt, st.session_state.messages)
                    
                if isinstance(choices, openai.types.chat.chat_completion.Choice):
                   
                    if choices.message.audio:
                        transcript = choices.message.audio.transcript
                        message = transcript
                        placeholder.caption(transcript)
                        
                        total = time.time() - init_t
                        timeholder.caption(f"{int(total)}s")
                        
                        wav_bytes = base64.b64decode(choices.message.audio.data)
                        audio_placeholder.audio(data=wav_bytes, autoplay=False)
                    else:
                        message = choices.message.content
                        display_text = ""
                        for char in message:
                            display_text += char
                            placeholder.caption(display_text)
                            time.sleep(0.01)
                        total = time.time() - init_t
                        timeholder.caption(f"{int(total)}s")

                else: 
                    message = choices
                    if is_base64(message):
                        image = display_base64_image(message)                
                        placeholder.image(image, use_column_width=True)
                        total = time.time() - init_t
                        timeholder.caption(f"{int(total)}s")



                    elif isinstance(message, pd.DataFrame):
                        placeholder.dataframe(message)
                        message = message.to_json()
                        total = time.time() - init_t
                        timeholder.caption(f"{int(total)}s")

                    elif isinstance(message, str):
                        # Simular escritura fluida
                        #audio_placeholder = st.empty()
                        display_text = ""
                        for char in message:
                            display_text += char
                            placeholder.caption(display_text)
                            time.sleep(0.01)
                        total = time.time() - init_t
                        timeholder.caption(f"{int(total)}s")

                        

                    else:
                        placeholder.error("Error inesperado en el tipo de respuesta.")
                    
                
                
                st.session_state.messages.append({"role": "assistant", "content": message})
                db.insert_conversation(st.session_state.CURRENT_SESION, 'assistant', message)
                
                

    #esto es un hack para applicar estilo a los botones del sidebar
    st.sidebar.markdown(
    """
        <style>
        button[kind="primary"] {
            background: none!important;
            border: none;
            padding: -5px 10px; /* Puedes ajustar estos valores según tus necesidades */
            color: black !important;
            text-decoration: none;
            cursor: pointer;
            border: none !important;
            margin: -8px -8px; /* Puedes ajustar estos valores según tus necesidades */
        }
        button[kind="primary"]:hover {
            text-decoration: none;
            color: red !important;
        }
        button[kind="primary"]:focus {
            outline: none !important;
            box-shadow: none !important;
            color: black !important;
        }
        </style>    
    """,
    unsafe_allow_html=True,
    )            
    