import streamlit as st

def main():
     # Configurar la página
    st.set_page_config(page_title="Chat IA - Integración API & WhatsApp", layout="wide")
        
    if not "page" in st.session_state:
        st.session_state.page = "index"
    
    if st.session_state.page == "index":    
        

        _, colmain, _ = st.columns([0.5,3,0.5])
        with colmain:
            # Menú de navegación
            colimage, colmenu = st.columns([0.2, 5])
            with colimage:
                 st.image("connect.svg", width=50)
            with colmenu:
                st.markdown(
                    """
                    <style>
                        .menu-container {
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            padding: 10px 50px;
                            
                        }
                        .menu-links a {
                            margin-right: 20px;
                            text-decoration: none;
                            color: black;
                            
                        }
                        .menu-auth a {
                            margin-left: 30px;
                            text-decoration: none;
                            color: black;
                            
                        }
                    </style>
                    <div class="menu-container">
                        <div class="menu-links">
                            <a href="#">Cloud</a>
                            <a href="#">Gallery</a>
                            <a href="#">Components</a>
                            <a href="#">Generative AI</a>
                            <a href="#">Community</a>
                            <a href="#">Docs</a>
                            <a href="#">Blog</a>
                        </div>
                        <div class="menu-auth">
                            <a href="#">Login</a>
                            <a href="#">Signup</a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
            # Logo de la empresa (puedes cambiarlo por tu logo)
            st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=200)
            
            # Título principal
            st.markdown("# Conecta tu Negocio con IA")
            st.markdown("## Integra tus APIs y Bases de Datos con un Chat Inteligente")
            
            # Botón de acción
            if st.button("Comenzar Ahora", type="primary"):
                st.session_state.page = "singup"
                st.rerun()
            
           
            
            # Sección de características
            st.markdown("---")
            #st.markdown("## ¿Qué ofrecemos?")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.image("chain.svg", width=100)
                st.markdown("### Conexión con APIs REST")
                st.write("Integra fácilmente tus servicios mediante API REST para que tus clientes interactúen con tu negocio desde un chat inteligente.")
            
            with col2:
                st.image("database.svg", width=100)
                st.markdown("### Conexión a Bases de Datos")
                st.write("Permite consultas y actualizaciones en tiempo real a tus bases de datos a través del chat con IA.")
            
            with col3:
                st.image("whatsapp.svg", width=100)
                st.markdown("### Integración con WhatsApp")
                st.write("Conecta tu negocio a WhatsApp para brindar soporte automatizado y procesar solicitudes sin necesidad de intervención humana.")
            
            st.markdown("---")
            st.video("hero-video.mp4")
            
            
            # Sección de contacto
            st.markdown("---")
            st.markdown("## ¿Interesado en probarlo?")
            st.write("Contáctanos para más información y descubre cómo podemos ayudar a digitalizar tu negocio.")
            
            st.button("Solicitar una Demostración")
    elif st.session_state.page == "singup":
        st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=200)

        
    
if __name__ == "__main__":
    main()
