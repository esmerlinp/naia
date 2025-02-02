import requests as r
from app.config import RRHH_HEADERS
import streamlit as st

class Reclutamiento():
    def __init__(self):
        pass
    
    RRHH_BASE_URL = st.session_state.baseUrl

    
    def get_elegibles(self):
        "Obtener candidatos del banco de elegibles"
        response = r.get(url=f"{RRHH_BASE_URL}/reclutamiento/bancoElegiblesYDescartados/1", headers=RRHH_HEADERS)
            
        if response.status_code == 200:
            data = response.json()['result']
            return data
                
        return None
    
    def get_requisiciones(self):
        "Obtener requisiciones de personal"
        response = r.get(url=f"{RRHH_BASE_URL}/reclutamiento/Requisicion/compania/{st.session_state.userCompany}", headers=RRHH_HEADERS)
            
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [{ 
                         "id": item.get("id"),
                         "nombre": item.get("nombre_Requisicion"),
                         "compania": item.get("nombreCompania"),
                         "puesto": item.get("nombre_Puesto"),
                         "requisitos": item.get("requisitosPuesto"),
                         "responsabilidades": item.get("responsabilidadesPuesto"),
                         "descripcion": item.get("descripcion"),
                         "comentario": item.get("comentario"),
                         "departamento": item.get("nombreDepartamento"),
                         "supervisor": item.get("nombre_Supervisor"),
                         "estado": item.get("nombre_Estado"),
                         "fechaCreacion": item.get("fecha_Creacion"),
                         "fechaCierre": item.get("fecha_Cierre"),
                
                } for item in data if item['ind_Estado'] == 3]
            
            activas = [req for req in data if req['ind_Estado'] == 3]
            
            return new_data
                
        return None
    
    def get_solicitudes(self):
        "Obtener solicitudes de empleo"
        response = r.get(url=f"{RRHH_BASE_URL}/reclutamiento/SolicitudEmpleo/compania/{st.session_state.userCompany}", headers=RRHH_HEADERS)
            
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [{ 
                         "id": item.get("id"),
                         "solicitante": item.get("nombre_Solicitud"),
                         "identificacion": item.get("identificacion"),
                         "origenSolicitud": item.get("nombre_Origen_Solicitante"),
                         "email": item.get("email"),
                         "telefono": item.get("telefono"),
                         "nombreRequisicion": item.get("nombre_Requisicion"),
                         "puesto": item.get("nombre_Puesto"),
                         "etapaSolicitud": item.get("nombre_Etapa"),
                         "estadoSolicitud": item.get("nombre_Estado"),
                         "apreciacion": item.get("apreciacion"),
                         "fechaSolicitud": item.get("fecha_Solicitud"),
                         "Reclutador": item.get("nombre_Reclutador"),
                
                } for item in data ]
            
            
            return new_data
                
        return None