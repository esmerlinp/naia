from app.config import RRHH_BASE_URL, RRHH_HEADERS
import requests as r
import streamlit as st



def authenticate(user, password):
    data = {"UserName":user, "Password":password}
    response = r.post(f'{st.session_state.baseUrl}/administracion/fmk/users/Authenticate', json=data, headers=RRHH_HEADERS)
    if response.status_code == 200:
        data_obj = response.json()
        return data_obj, 200
    if response.status_code == 400:
         data_obj = response.json()
         return data_obj['message'], 400
    else:
        return "", response.status_code

    