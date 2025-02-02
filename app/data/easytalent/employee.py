import streamlit as st
import requests as r
from app.config import RRHH_HEADERS
import pandas as pd
from app.utils import base64_to_file_content

RRHH_BASE_URL = st.session_state.baseUrl

class Employee():
    def __init__(self):
        pass
    
    
    def convertir_empleado_a_dict_reducido(self, empleado):
        """
        Convierte el diccionario completo de un empleado en un diccionario reducido
        con solo la información más relevante.
        
        :param empleado: Diccionario con los datos completos del empleado.
        :return: Diccionario con los datos relevantes del empleado.
        """
        return {
            "idEmpleado": empleado.get("idEmpleado"),
            "nombre_completo": empleado.get("nombreCompletoEmpleado"),
            "nombre_compania": empleado.get("nombre_Compania"),
            "codigo_empleado": empleado.get("codigoEmpleado"),
            "departamento": empleado.get("nombre_Departamento"),
            "sucursal": empleado.get("nombre_Sucursal"),
            "puesto": empleado.get("nombre_Puesto"),
            "identificacion": empleado.get("datoIdentificacion"),
            "supervisor": empleado.get("nombre_Supervisor"),
            "estado_empleado": empleado.get("nombre_EstadoEmpleado"),
            "salario_base": empleado.get("salarioBase"),
            "email_personal": empleado.get("email"),
            "telefono_personal": empleado.get("telefonoPersonal"),
            "forma_pago": empleado.get("nombre_FormaPago"),
            "numero_cuenta_bancaria": empleado.get("numeroCuentaBanco"),
            "tipo_contrato": empleado.get("nombre_TipoContrato"),
            "fecha_ingreso": empleado.get("fechaIngreso", "").split("T")[0] if empleado.get("fechaIngreso") else None,
            "fecha_finalizacion": empleado.get("fechaFinalizacion", "").split("T")[0] if empleado.get("fechaFinalizacion") else None,
            "fecha_salida": empleado.get("fechaSalida", "").split("T")[0] if empleado.get("fechaSalida") else None,
            "tipo_salario": empleado.get("nombre_TipoSalario"),
            "genero": 'Masculino' if empleado.get("genero") == 1 else 'Femenino' if empleado.get("genero") == 2 else 'Otro',
            "dias_vacaciones_tomados": empleado.get("cantidadDiasVacacionesTomados"),
            "dias_vacaciones_pendientes": empleado.get("cantidadDiasVacacionesPendientes"),
            "telefono_contacto_emergencia": empleado.get("telefonoContactoEmergencia"),
            #"razón_salida": empleado.get("razonSalida"),
            #"ciudad_residencia": empleado.get("ciudadResidencia"),
            #"sector_residencia": empleado.get("sectorResidencia"),
            #"estatura_pies": empleado.get("estaturaPies"),
            #"tipo_sangre": empleado.get("tiposangre"),
            #"condición_médica": empleado.get("condicionMedica"),
            #"discapacidad": empleado.get("discapacidad"),
            #"riesgo_laboral": empleado.get("riesgo")
        }


    @st.cache_data(ttl=60*60, show_spinner=False) #Actualiza cada hora
    def get_employees(_self, employee_ids=[], identificaciones=[], names=[], key_words=[]):
        """ Obtiene la información de un empleado por su ID y puede incluir datos adicionales 
        basados en las acciones especificadas en el parámetro `context`.

        Args:
            employee_id (int): El ID único del empleado a consultar.
            context (list, opcional): Lista de cadenas que indican las acciones adicionales 
                                    a consultar. Puede incluir las siguientes acciones:
                                    - "prestamos": Para obtener información de préstamos del empleado.
                                    - "ausencias": Para obtener todas las ausencias del empleado (vacaciones, licencias, permisos).
                                    - "vacaciones", "licencias", "permisos": Específicos tipos de ausencias que se pueden consultar.

        Returns:
            dict: Un diccionario con la información del empleado que incluye:
                - Los datos básicos del empleado bajo la clave "result".
                - Las transacciones realizadas por el empleado bajo la clave "transacciones".
                - Los préstamos del empleado (si se solicita) bajo la clave "prestamos".
                - Las ausencias del empleado (si se solicita) bajo la clave "ausencias".
                
            En caso de error, retorna una lista vacía si la solicitud al API falla o no se encuentra el empleado.
        
        Ejemplo:
            ```python
            # Obtener empleado con ID 123 y consultar préstamos y ausencias
            employee_info = get_employee(123, context=["prestamos", "ausencias"])
            ```
        """
        employees = []
        
        if not employee_ids and not identificaciones and not names:
            response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados", headers=RRHH_HEADERS)
            if response.status_code == 200:
                empleado_list = response.json()['result']
                for empleado in empleado_list:
                    employees.append(_self.convertir_empleado_a_dict_reducido(empleado))
            else:
                return []        
        else:    
            for employee_id in employee_ids:
                response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/{employee_id}", headers=RRHH_HEADERS)
                if response.status_code == 200:
                    empleado = response.json()['result']
                    datos_empleado = _self.convertir_empleado_a_dict_reducido(empleado)
                    employees.append(datos_empleado)
                    
            
            for identificacion in identificaciones:    
                response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/identificacion/{identificacion}", headers=RRHH_HEADERS)
                if response.status_code == 200:
                    empleado = response.json()['result']
                    datos_empleado = _self.convertir_empleado_a_dict_reducido(empleado)
                    employees.append(datos_empleado)
                
            
            for name in names:
                response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/nombre/{name}", headers=RRHH_HEADERS)    
                if response.status_code == 200:
                    empleado_list = response.json()['result']
                    for empleado in empleado_list:
                        datos_empleado = _self.convertir_empleado_a_dict_reducido(empleado)
                        employees.append(datos_empleado)
            
   
        # Crear DataFrame de empleados
        df_empleados = pd.DataFrame(employees)
        

        if "prestamos" in key_words:
            df_prestamos = _self.get_aditional_employee_info(employees=employees,function_request=_self.get_prestamos) 
            if 'idEmpleado' in df_prestamos.columns:
                df_empleados = df_empleados.merge(df_prestamos, on='idEmpleado', how='left')
            
        if "habilidades" in key_words:
            df_habilidades = _self.get_aditional_employee_info(employees=employees,function_request=_self.habilidades) 
            if 'idEmpleado' in df_habilidades.columns:
                df_empleados = df_empleados.merge(df_habilidades, on='idEmpleado', how='left')
        
        if "herramientas" in key_words:
            df_herramientas = _self.get_aditional_employee_info(employees=employees,function_request=_self.herramientas) 
            if 'idEmpleado' in df_herramientas.columns:
                df_empleados = df_empleados.merge(df_herramientas, on='idEmpleado', how='left')
                
        if "capacitaciones" in key_words:
            df_capacitaciones = _self.get_aditional_employee_info(employees=employees,function_request=_self.capacitaciones) 
            if 'idEmpleado' in df_capacitaciones.columns:
                df_empleados = df_empleados.merge(df_capacitaciones, on='idEmpleado', how='left')
                
        if "centro_costos" in key_words:
            df_centrocostos = _self.get_aditional_employee_info(employees=employees,function_request=_self.centros_costos) 
            if 'idEmpleado' in df_centrocostos.columns:
                df_empleados = df_empleados.merge(df_centrocostos, on='idEmpleado', how='left')
        
        if "beneficios" in key_words:
            df_beneficios = _self.get_aditional_employee_info(employees=employees,function_request=_self.beneficios) 
            if 'idEmpleado' in df_beneficios.columns:
                df_empleados = df_empleados.merge(df_beneficios, on='idEmpleado', how='left')
                
        if "cambio_salario" in key_words:
            df_salarios = _self.get_aditional_employee_info(employees=employees,function_request=_self.get_acciones) 
            df_salarios = df_salarios[df_salarios["codigo_cambio"] == 8]
            if 'idEmpleado' in df_salarios.columns:
                df_empleados = df_empleados.merge(df_salarios, on='idEmpleado', how='left')
                
        if "cambio_sucursal" in key_words:
            df_sucursal = _self.get_aditional_employee_info(employees=employees,function_request=_self.get_acciones) 
            df_sucursal = df_sucursal[df_sucursal["codigo_cambio"] == 4]
            if 'idEmpleado' in df_sucursal.columns:
                df_empleados = df_empleados.merge(df_sucursal, on='idEmpleado', how='left')
        
        if "cambio_compania" in key_words:
            df_company = _self.get_aditional_employee_info(employees=employees,function_request=_self.get_acciones) 
            df_company = df_company[df_company["codigo_cambio"] == 3]
            if 'idEmpleado' in df_company.columns:
                df_empleados = df_empleados.merge(df_company, on='idEmpleado', how='left')
                
        if "desvinculación" in key_words:
            df_desvinculacion = _self.get_aditional_employee_info(employees=employees,function_request=_self.get_acciones) 
            df_desvinculacion = df_desvinculacion[df_desvinculacion["codigo_cambio"] == 10]
            if 'idEmpleado' in df_desvinculacion.columns:
                df_empleados = df_empleados.merge(df_desvinculacion, on='idEmpleado', how='left')
                
        if "amonestaciones" in key_words:
            df_amonestacion = _self.get_aditional_employee_info(employees=employees,function_request=_self.get_amonestaciones) 
            if 'idEmpleado' in df_amonestacion.columns:
                df_empleados = df_empleados.merge(df_amonestacion, on='idEmpleado', how='left')
        
        if "educacion" in key_words:
            df_educacion = _self.get_aditional_employee_info(employees=employees,function_request=_self.educacion) 
            if 'idEmpleado' in df_educacion.columns:
                df_empleados = df_empleados.merge(df_educacion, on='idEmpleado', how='left')
        
        if "experiencia" in key_words:
            df_experiencia = _self.get_aditional_employee_info(employees=employees,function_request=_self.experiencia) 
            if 'idEmpleado' in df_experiencia.columns:
                df_empleados = df_empleados.merge(df_experiencia, on='idEmpleado', how='left')
        
                
        ############################################################################
        
        key_words_dep = ["dependientes", "familiares"]
        if any(elem in key_words for elem in key_words_dep):
            df_dependientes = _self.get_aditional_employee_info(employees=employees,function_request=_self.dependientes) 
            if 'idEmpleado' in df_dependientes.columns:
                df_empleados = df_empleados.merge(df_dependientes, on='idEmpleado', how='left')
                
                
        ############################################################################   
                     
        key_words_acciones = ['promocion','cambio_puesto']
        if any(elem in key_words for elem in key_words_acciones):
            df_promociones = _self.get_aditional_employee_info(employees=employees,function_request=_self.get_acciones) 
            df_promociones = df_promociones[df_promociones["codigo_cambio"] == 7]
            if 'idEmpleado' in df_promociones.columns:
                df_empleados = df_empleados.merge(df_promociones, on='idEmpleado', how='left')
                
        ############################################################################

        key_words_ausencias = ["ausencias", "vacaciones", "licencias", "permisos"]
        if any(elem in key_words for elem in key_words_ausencias):
            df_ausencias= _self.get_aditional_employee_info(employees=employees,function_request=_self.get_ausencias) 
            if 'idEmpleado' in df_ausencias.columns:
                df_empleados = df_empleados.merge(df_ausencias, on='idEmpleado', how='left')
        ############################################################################
        
        key_words_nom = ["nomina", "pagos", "volantes"]
        if any(elem in key_words for elem in key_words_nom):
            df_pagos= _self.get_aditional_employee_info(employees=employees,function_request=_self.payments) 
            if 'idEmpleado' in df_pagos.columns:
                df_empleados = df_empleados.merge(df_pagos, on='idEmpleado', how='left')
        
        ############################################################################
        
        key_words_seg = ["seguros", "salud", "medicos", "planes"]
        if any(elem in key_words for elem in key_words_seg):
            df_seguros = _self.get_aditional_employee_info(employees=employees,function_request=_self.get_seguros) 
            if 'idEmpleado' in df_seguros.columns:
                df_empleados = df_empleados.merge(df_seguros, on='idEmpleado', how='left')
        ############################################################################
               
        

        # Eliminar columnas que solo contienen NaN después del merge
        df_cleaned = df_empleados.dropna(axis=1, how='all')
        
        # Eliminar columnas duplicadas
        df_cleaned = df_cleaned.T.drop_duplicates().T
        return df_cleaned.to_dict()
        
    def get_ausencias(self, employee_id):
        """Obtiene las ausencias de un empleado por id"""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/ausencias/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [
                {
                    "id": item["id"],
                    #"id_AccionWeb": item["id_AccionWeb"],
                    #"id_Registro_Relacionado": item["id_Registro_Relacionado"],
                    "fecha_Inicio": item["fecha_Inicio"],  
                    "fecha_Fin": item["fecha_Fin"],       
                    "cantidad": item["cantidad"],
                    "nombre_Tipo_Notificacion": item["nombre_Tipo_Notificacion"],
                    "reportado_Ley_Text": item["reportado_Ley_Text"],
                    "fecha_Registro": item["fecha_Registro"],
                    "codigo_Estado": item["codigo_Estado"],
                    "nombre_Tipo_Ausencia": item["nombre_Tipo_Ausencia"],
                    "comentario": item["comentario"]
                }
                for item in data
            ]            
            return new_data
        else:
            return []  
        
    def get_prestamos(self, employee_id):
        """Obtiene los prestamos de un empleado por id"""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/PrestamosEmpleado/detalle-prestamo/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']            
            return data
        else:
            return []  
        
    def get_seguros(self, employee_id):
        """Obtiene planes de seguros de el empleado"""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/detalle-planes-seguro/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']            
            return data
        else:
            return []  
        
    def get_acciones(self, employee_id):
        """Obtiene los acciones de un empleado por id"""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/TransaccionAccionPersonalEmpleado/AI/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [
                {
                    "id": item["id"],
                    "codigo_cambio": item["id_AccionWeb"],
                    "idEmpleado": employee_id,
                    "descripcion_cambio": item["descripcion_Accion"],
                    "valor_propuesto": item["conceptoPropuesto"],
                    "valor_anterior": item["conceptoAnterior"],
                    "fecha_Efectiva": item["fecha_Efectiva"].split("T")[0],  # Extraer solo la fecha
                    "fecha_Registro": item["fecha_Registro"],
                    "codigo_Estado": item["codigo_Estado"],
                    "estado": item["estado"],
                    "comentario": item["comentario"],
                    "solicitado_por": item["nombre_Usuario"]
                }
                for item in data
            ]    
            
             
            return new_data
        else:
            return []  
        
    def get_amonestaciones(self, employee_id):
        """Obtiene los acciones de un empleado por id"""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/transaccionaccionpersonalempleado/{employee_id}/11", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [
                {
                    "id": item["id"],
                    "idEmpleado": employee_id,
                    "Tipo_Notificacion": item["nombre_Tipo_Notificacion"],
                    "motivo_Razon": item["motivo_Razon"],
                    "fecha_Registro": item["fecha_Registro"],
                    "estado": item["estado"],
                    "comentario": item["comentario"],
                    "solicitado_por": item["nombre_Usuario"]
                }
                for item in data
            ]    
            
             
            return new_data
        else:
            return []  
          
    def get_image(self, employee_id):
        """Obtiene la foto del empleado por id
            
        # Mostramos la imagen usando Streamlit
        st.image(image, caption='Imagen cargada desde Base64', use_column_width=True)
        """
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/ArchivoEmpleado/{employee_id}", headers=RRHH_HEADERS)
        if response.status_code == 200:
            data = response.json()['result']
            archivoInBase64 = data['archivoInBase64']
            #extension = data['extension']
            #image = base64_to_image(archivoInBase64)
            return archivoInBase64
            return image
        else:
            return None
                   
    def payments(self, employee_id):
        """Obtiene pagos realizados al empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/nomina/UtilReporteNomina/pagos-empleado/{employee_id}", headers=RRHH_HEADERS)
                
        if response.status_code == 200:
            data = response.json()['result']
            new_pago = [
                {
                    "idEmpleado": pago.get("idEmpleado"),
                    "nombreDepartamento": pago.get("nombreDepartamento"),
                    "nombrePuestoTrabajo": pago.get("nombrePuestoTrabajo"),
                    "codigoDetallePeriodo": pago.get("codigoDetallePeriodo"),
                    "bancoNombre": pago.get("bancoNombre"),
                    "numeroCuentaDetallePagoNomina": pago.get("numeroCuentaDetallePagoNomina"),
                    "tipoNominaNombre": pago.get("tipoNominaNombre"),
                    "codigoTipoNomina": pago.get("codigoTipoNomina"),
                    "empleadoSalario": pago.get("empleadoSalario"),
                    "fechaInicioDetallePeriodo": pago.get("fechaInicioDetallePeriodo", "").split("T")[0] if pago.get("fechaInicioDetallePeriodo") else None,
                    "fechaFinDetallePeriodo": pago.get("fechaFinDetallePeriodo", "").split("T")[0] if pago.get("fechaFinDetallePeriodo") else None,
                    "descripcionDetallePeriodo": pago.get("descripcionDetallePeriodo"),
                    "codigoAltConcepto": pago.get("codigoAltConcepto"),
                    "nombreConcepto": pago.get("nombreConcepto"),
                    "montoConceptoDetalle": pago.get("montoConceptoDetalle"),
                    "origenConcepto": pago.get("origenConcepto"),
                    "balanceActual": pago.get("balanceActual"),
                    "balanceAnterior": pago.get("balanceAnterior"),
                    "formaPago": pago.get("formaPago")
                } for pago in data
            ]
            
            # Agrupación por `codigoDetallePeriodo` con conceptos como claves
            pagos_agrupados = {}
            for pago in new_pago:
                codigo = pago["codigoDetallePeriodo"]
                if codigo not in pagos_agrupados:
                    pagos_agrupados[codigo] = {
                        "idEmpleado": pago["idEmpleado"],
                        "nombreDepartamento": pago["nombreDepartamento"],
                        "nombrePuestoTrabajo": pago["nombrePuestoTrabajo"],
                        "banco": pago["bancoNombre"],
                        "cuenta_bancaria": pago["numeroCuentaDetallePagoNomina"],
                        "nomina": pago["tipoNominaNombre"],
                        "fecha_ini_periodo": pago["fechaInicioDetallePeriodo"],
                        "fecha_fin_periodo": pago["fechaFinDetallePeriodo"],
                        "periodo": pago["descripcionDetallePeriodo"],
                        "codigoDetallePeriodo": codigo,
                        #"salario_bruto": pago["empleadoSalario"],
                    }
                
                # Añadir el concepto como clave en el diccionario de conceptos
                nombre_concepto = pago["nombreConcepto"]
                monto_concepto = float(pago["montoConceptoDetalle"]) * int(pago["origenConcepto"])
                pagos_agrupados[codigo][nombre_concepto] = monto_concepto
            result = [v for k, v in pagos_agrupados.items()]
            
            return result
        
    def resumen(self, employee_id):
        """Obtiene experiencias y educacion del empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/resumenempleado/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [
                {
                    "tipo": item["nombre_Tipo_Resumen"],
                    "descripcion": item["nombre"],
                    "fecha_Inicio": item["fecha_Inicio"],
                    "fecha_Fin": item["fecha_Fin"]
                }
                for item in data
            ]  
            return new_data
        else:
            return [] 
         
    def educacion(self, employee_id):
        """Obtiene educacion del empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/resumenempleado/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [
                {
                    "tipo": item["nombre_Tipo_Resumen"],
                    "nombreProgramaEducativo": item["nombre"],
                    "descripcionPrograma": item["descripcion"],
                    "fecha_Inicio": item["fecha_Inicio"],
                    "fecha_Fin": item["fecha_Fin"],
                    "institucion": item["lugar"],

                }
                for item in data if item["iD_Tipo_Resumen"] == 2 #Educacion
            ]  
            return new_data
        else:
            return [] 
         
    def experiencia(self, employee_id):
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/resumenempleado/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [
                {
                    "tipo": item["nombre_Tipo_Resumen"],
                    "puesto": item["nombre"],
                    "descripcion": item["descripcion"],
                    "fecha_Inicio": item["fecha_Inicio"],
                    "fecha_Fin": item["fecha_Fin"],
                    "lugar": item["lugar"],

                }
                for item in data if item["iD_Tipo_Resumen"] == 1 #Educacion
            ]  
            return new_data
        else:
            return []  
        
    def beneficios(self, employee_id):
        """Obtiene  lista de beneficios del empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/detalleBeneficios/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            return data
        else:
            return []  
        
    def centros_costos(self, employee_id):
        """Obtiene centros de costos del empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/centrocostos/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            return data
        else:
            return []  
         
    def habilidades(self, employee_id):
        """Obtiene habilidades del empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/habilidadempleado/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            new_data = [
                {
                    "idHabilidad": item["iD_Habilidad_Empleado"],
                    "idEmpleado": employee_id,
                    "habilidad": item["tipo_Habilidad"],
                    "descripcion": item["descripcion"],
                    "nivel": item["nombre_Nivel_Habilidad"]
                }
                for item in data
            ]  
            return new_data
        else:
            return []   
        
    def dependientes(self, employee_id):
        """Obtiene dependientes del empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/detalleDependienteEmpleado/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            return data
        else:
            return []   
        
    def capacitaciones(self, employee_id):
        """Obtiene capacitaciones del empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/CapacitacionEmpleado/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            return data
        else:
            return []   
            
    def herramientas(self, employee_id):
        """Obtiene herramientas del empleado."""
        response = r.get(url=f"{RRHH_BASE_URL}/empleados/herramientasempleado/{employee_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            return data
        else:
            return []   
             
    def offert_detail(self, solicitud_id=4000):

        response = r.get(url=f"{RRHH_BASE_URL}/reclutamiento/SolicitudEmpleo/detalleArchivo/{solicitud_id}", headers=RRHH_HEADERS)
               
        if response.status_code == 200:
            data = response.json()['result']
            #content = base64_to_file_content(data[0][0]['archivoInBase64'])
            #print(f"Contenido decodificado (primeros 50 bytes): {content[:1000]}")
            
            # Ejemplo de uso:
            base64_string = f'data:image/{data[0][0]["extension"]};base64,/{data[0][0]["archivoInBase64"]}'  # Reemplaza con tu cadena Base64
            output_file = f'output_image{data[0][0]["extension"]}'  # Especifica el nombre y extensión del archivo deseado

            content = base64_to_file_content(base64_string, output_file)
            print(f"Contenido del archivo (primeros 50 bytes): {content[:100]}")
                        
            
            return content
        else:
            return []        
              
    def get_aditional_employee_info(self, employees, function_request) -> pd.DataFrame:
        """
        Obtiene información adicional de empleados y la organiza en un DataFrame de pandas.

        Esta función toma una lista de empleados y una función para obtener datos adicionales
        de cada empleado. Para cada empleado en la lista, llama a `function_request` para 
        recuperar información específica del empleado, como sus dependientes o cualquier otro 
        dato relacionado. Luego, los datos se consolidan en un DataFrame.

        Parámetros:
        - employees (list of dict): Una lista de diccionarios, donde cada diccionario representa 
        un empleado con al menos los siguientes campos:
            - 'idEmpleado' (int): Identificador único del empleado.
            - 'nombre_completo' (str): Nombre completo del empleado.
        - function_request (function): Una función que recibe el `idEmpleado` y retorna una lista 
        de diccionarios con información adicional del empleado (e.g., dependientes). Cada 
        diccionario en esta lista debe contener pares clave-valor que se incorporarán al resultado 
        final.

        Retorno:
        - pd.DataFrame: Un DataFrame de pandas donde cada fila contiene la información combinada 
        de un empleado junto con sus datos adicionales. Las columnas incluyen:
            - 'idEmpleado': Identificador del empleado.
            - 'nombre_completo': Nombre completo del empleado.
            - Otras columnas basadas en las claves de los datos adicionales recuperados.

        Ejemplo de uso:
        ```
        # Lista de empleados de ejemplo
        empleados = [
            {"idEmpleado": 1, "nombre_completo": "Juan Pérez"},
            {"idEmpleado": 2, "nombre_completo": "Ana García"}
        ]

        # Función de ejemplo para obtener datos adicionales de un empleado
        def obtener_dependientes(employee_id):
            # Ejemplo de datos retornados por cada empleado
            if employee_id == 1:
                return [
                    [{"nombre_dependiente": "Pedro Pérez", "relación": "Hijo"}],
                    [{"nombre_dependiente": "Laura Pérez", "relación": "Esposa"}]
                ]
            else:
                return [
                    [{"nombre_dependiente": "Carlos García", "relación": "Hijo"}]
                ]

        # Llamada a la función
        df = get_aditional_employee_info(empleados, obtener_dependientes)
        print(df)
        ```
        """
        
        data_result = []

        for empleado in employees: 
            employee_id = empleado['idEmpleado']   
            response_data = function_request(employee_id)

            # Agregar cada dependiente a la lista del empleado
            for data in response_data:
                combined_data = {
                    "idEmpleado": employee_id,
                    "nombre_completo": empleado['nombre_completo'],
                    **{k: v for k, v in data.items()}
                }
                data_result.append(combined_data)  

        df = pd.DataFrame(data_result)
        return df

    def get_employees_by_names(self, names):
        employees = []
        for name in names:
            response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/nombre/{name}", headers=RRHH_HEADERS)    
            if response.status_code == 200:
                empleado_list = response.json()['result']
                for empleado in empleado_list:
                    datos_empleado = self.convertir_empleado_a_dict_reducido(empleado)
                    employees.append(datos_empleado)
        return employees            