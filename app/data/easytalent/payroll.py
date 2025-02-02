import streamlit as st
import requests as r
from app.config import RRHH_HEADERS
import json
import pandas as pd 
from datetime import datetime

RRHH_BASE_URL = st.session_state.baseUrl


class Payroll():
    def __init__(self):
        pass
    
    
    def __extraer_datos_relevantes(self, nomina):
        campos_relevantes = {
            "infoNomina": nomina.get("infoNomina"),
            "infoPeriodo": nomina.get("infoPeriodo"),
            "empresa": nomina.get("nombreEmpresa"),
            "tipoSalario": nomina.get("tipoSalario"),
            "departamento": nomina.get("departamento"),
            "fechaActual": nomina.get("fechaActual"),
            "empleado": nomina.get("empleado"),
            "puesto": nomina.get("puesto"),
            "salario": nomina.get("salario"),
            "ingresos": nomina.get("ingresos"),
            "descuentos": nomina.get("descuentos"),
            "descuentosLey": nomina.get("descuentosLey"),
            "totalDescuentos": nomina.get("totalDescuentos"),
            "neto": nomina.get("neto"),
            "formaSalario": nomina.get("formaSalario"),
        }
        return campos_relevantes
    
   
    @st.cache_data(ttl=3600, show_spinner=False)
    def get_resumen(_self, periodoInicial="2024-01-01T00:00:00", periodoFinal="2024-09-30T09:00:00"):
        """
        Realiza una solicitud POST para obtener un reporte de nómina entre un periodo de tiempo específico.

        Parámetros:
        - periodoInicial (str): Fecha de inicio del periodo en formato ISO8601. Por defecto, es "2024-01-01T00:00:00".
        - periodoFinal (str): Fecha de fin del periodo en formato ISO8601. Por defecto, es "2024-09-30T09:00:00".

        Retorno:
        - nominas_relevantes (list): Lista de diccionarios con los campos relevantes de cada nómina.
        - []: Si la solicitud falla o no se encuentran datos relevantes.
        
        Ejemplo de uso:
        
        reporte_nomina = obj.get_nomina(periodoInicial="2024-01-01T00:00:00", periodoFinal="2024-09-30T09:00:00")
        """
        
                # Fecha inicial del año actual
        if not periodoInicial:
            periodoInicial = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%dT%H:%M:%S')
        
        # Fecha actual
        if not periodoFinal:
            periodoFinal = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            
        body = {
            "type": 4,
            "DetalleGeneralModel": {
                "compania": 2,
                "tipoNomina": 115,
                "periodoInicial": periodoInicial,
                "periodoFinal": periodoFinal,
                "idiomaFormaPago": "es-DO",
                "idiomaTipoContrato": "es-DO"
            }, 
            "json": True
        }

        response = r.post(url=f"{RRHH_BASE_URL}/nomina/UtilReporteNomina/generar-reporte-nomina", headers=RRHH_HEADERS, data=json.dumps(body))

        if response.status_code == 200:
            data = response.json()
            nominas_relevantes = [_self.__extraer_datos_relevantes(nomina) for nomina in data]
            
            df = pd.read_json(json.dumps(nominas_relevantes))
            # Resumen estadístico de columnas numéricas
            df_resumen = df.groupby('infoPeriodo')
            df_resumen = df.to_dict()
            #salario_por_departamento  = df.groupby('departamento')['salario'].mean()
            #df_resumen["Salarios_por_departamento"] = salario_por_departamento.to_dict()
            

            # Análisis de Ingresos y Descuentos
            total_ingresos = df['ingresos'].sum()
            total_descuentos = df['totalDescuentos'].sum()
            ingresos_promedio = df['ingresos'].mean()
            
            df_resumen["total_Ingresos"] = total_ingresos
            df_resumen["total_descuentos"] = total_descuentos
            df_resumen["Ingreso_promedio"] = ingresos_promedio

            # Desglose por Departamento
            #ingresos_por_departamento = df.groupby('departamento')['ingresos'].sum()
            
            #df_resumen["Ingreso_por_departamento"] = ingresos_por_departamento.to_dict()

            # Desglose por Puesto
            #ingresos_por_puesto = df.groupby('puesto')['ingresos'].sum()
            
            #df_resumen["Ingreso_por_puesto"] = ingresos_por_puesto.to_dict()

            # Distribución de Tipo de Salario
            #tipo_salario_counts = df['tipoSalario'].value_counts()
            
            #df_resumen["tipos_salarios"] = tipo_salario_counts.to_dict()
            # Control de Auditoría y Validación de Datos (identificar datos faltantes o inconsistentes)
            #inconsistencias = df[(df['ingresos'] == 0) & (df['descuentos'] > 0)]

            
            #df_resumen["inconsistencias"] = inconsistencias.to_dict()
                        
            return df_resumen
        else:
            return []
  
        
    @st.cache_data(ttl=3600, show_spinner=False)
    def get_nomina(_self, periodoInicial=None, periodoFinal=None):
        """
        Realiza una solicitud POST para obtener un reporte de nómina entre un periodo de tiempo específico.

        Parámetros:
        - periodoInicial (str): Fecha de inicio del periodo en formato ISO8601. Por defecto, es "2024-01-01T00:00:00".
        - periodoFinal (str): Fecha de fin del periodo en formato ISO8601. Por defecto, es "2024-09-30T09:00:00".

        Retorno:
        - nominas_relevantes (list): Lista de diccionarios con los campos relevantes de cada nómina.
        - []: Si la solicitud falla o no se encuentran datos relevantes.
        
        Ejemplo de uso:
        
        reporte_nomina = obj.get_nomina(periodoInicial="2024-01-01T00:00:00", periodoFinal="2024-09-30T09:00:00")
        """
        
        # Fecha inicial del año actual
        if not periodoInicial:
            periodoInicial = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%dT%H:%M:%S')
        
        # Fecha actual
        if not periodoFinal:
            periodoFinal = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')



        body = {
            "type": 4,
            "DetalleGeneralModel": {
                "compania": 2,
                "tipoNomina": 115,
                "periodoInicial": periodoInicial,
                "periodoFinal": periodoFinal,
                "idiomaFormaPago": "es-DO",
                "idiomaTipoContrato": "es-DO"
            }, 
            "json": True
        }

        response = r.post(url=f"{RRHH_BASE_URL}/nomina/UtilReporteNomina/generar-reporte-nomina", headers=RRHH_HEADERS, data=json.dumps(body))

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return []
  
        
