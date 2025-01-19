from openai import OpenAI
import json
import streamlit as st
import requests as r
from app.config import RRHH_HEADERS
from app.data.employee.employee import Employee
from app.data.reclutamiento.reclutamiento import Reclutamiento
from app.data.payroll.payroll import Payroll
from app.data.odoo_employee_api import OdooEmployeeAPI
from app.functions import functions
from datetime import datetime
from app.utils import es_ruta, png_to_base64, validate_params, clear_history
from pandasai.llm import OpenAI as POpenAI
from pandasai import SmartDataframe
import numpy as np
import pandas as pd
import os

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
bllm = POpenAI(api_token=OPENAI_API_KEY)
#bllm = POpenAI(api_token=OPENAI_API_KEY, temperature=0.7, seed=42)


class LLM():
    """
    Clase LLM para interactuar con un modelo de lenguaje y gestionar información relacionada con empleados.
    
    Esta clase se utiliza para validar parámetros, procesar respuestas del modelo y manejar interacciones
    relacionadas con recursos humanos, como obtener información de empleados y registrar ausencias.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase LLM.
        
        Se configura el rol del asistente virtual y el modelo a utilizar. También se crea una instancia
        de la clase Employee para interactuar con los datos de los empleados.
        """
        # gpt-3.5-turbo
        self.rol = '''Mi función es proporcionar asistencia y responder preguntas exclusivamente relacionadas con la gestión de recursos humanos. Nunca debes ofrecer información fuera de estos temas ni tratar asuntos que no formen parte de tus responsabilidades principales.'''
        self.model = "gpt-4o"
        #self.model = "gpt-3.5-turbo"
        self.employee = Employee()
        self.odoo_api = OdooEmployeeAPI()
        self.reclutamiento = Reclutamiento()
        self.payroll = Payroll()

        # Crear el SmartDataframe con el DataFrame vacío
       

    def proccess_message(self, text, historial=[]):
        """
        Procesa un mensaje de entrada y ejecuta funciones según sea necesario.

        Args:
            text (str): El mensaje de entrada del usuario.
            historial (list): Lista de mensajes anteriores en la conversación.

        Returns:
            str: La respuesta generada tras procesar el mensaje.
        """
        
        filtered_messages = clear_history(historial)
        print(text, end="\n\n")
        
        function_name, args, message = self.process_functions(text, filtered_messages)
        print( function_name, args, message)
        
        if function_name is not None:
            key_words = args.get("key_words", []) 
            
            #Obtener Requisiciones
            if function_name == "get_requisiciones":
                data = self.reclutamiento.get_requisiciones()
                return self.process_call(question=text, data=data, name="requisiciones", description="datos de las requisiciones de personal de la empresa")
           
            if function_name == "consultar_empleados_odoo":
                filtro = args['filtro']
                #campos_a_recuperar = args['campos_a_recuperar']
                #estado = args['estado']
                #limite = args['limite']
                data = self.odoo_api.consultar_empleados(
                    filtro=filtro,
                    campos_a_recuperar=[],
                    estado="activo",
                    limite=1000,
                    ordenar_por="name",
                    orden="asc"
                )
                #print("DATA", data)
                return self.process_call(question=text, data=data, name="requisiciones", description="datos de las requisiciones de personal de la empresa")
            
            if function_name == "consultar_compras_odoo":
                
                filtro = args.get('filtro', None)
                campos_a_recuperar = args.get('campos_a_recuperar', [])
                estado = args.get("estado", "todos")
                fecha_desde= args.get('fecha_desde', None),
                fecha_hasta= args.get('fecha_hasta', None),
                limite = args.get("limite", 100)
                ordenar_por = args.get('ordenar_por', 'name')
                orden = args.get('orden', 'asc')
                
                data = self.odoo_api.consultar_compras(filtro=None)
                #print("DATA", data)
                return self.process_call(question=text, data=data, name="requisiciones", description="datos de las requisiciones de personal de la empresa")
            
            if function_name == "get_solicitudes_empleo":
                data = self.reclutamiento.get_solicitudes()
                return self.process_call(question=text, data=data, name="Solicitudes de empleo", description="Lista de solicitudes de empleo recibidas")
            
            if function_name == "get_employee_image":
                
                employee_ids = []
                if "employee_ids" in args:
                    employee_ids = args['employee_ids']
                    base64_image = self.employee.get_image(employee_ids[0])
                    if base64_image:
                        return base64_image
                    else:
                        return "El empleado no tiene una imagen de perfil asignada."
                
                employee_names = []   
                if "employee_names" in args:
                    employee_names = args['employee_names']
                    data = self.employee.get_employees_by_names(names=employee_names) 
                    if data:
                        base64_image = self.employee.get_image(data[0]['idEmpleado'])
                        if base64_image:
                            return base64_image
                        else:
                            return "El empleado no tiene una imagen de perfil asignada."
                    else:
                        return "El empleado especificado no se encuentra en nuestros registros."
              
            #Candidatos del banco de candidatos    
            if function_name == "get_candidatos":
                data = self.reclutamiento.get_elegibles()
                return self.process_call(question=text, data=data, name="candidatos", description="candidatos elegibles para una posiscion dentro de la empresa")

            #consultar empleados por id, nombres o identificacion
            if function_name == "get_employees":
                print('get_employees')

                employee_ids = []
                if "employee_ids" in args:
                    employee_ids = args['employee_ids'] 
                    
                identificaciones = []
                if "identificaciones" in args:
                    identificaciones = args['identificaciones'] 
                    
                employee_names = []   
                if "employee_names" in args:
                    employee_names = args['employee_names']     


                data = self.employee.get_employees(employee_ids=employee_ids, identificaciones=identificaciones, names=employee_names, key_words=key_words)
                return self.process_call(question=text, data=data, name="empleados", description="datos de algunos empleados de la empresa", key_words=key_words)

            
            #Consultar periodos de nomina
            if function_name == "get_nominas":
                
                
                # Fecha inicial del año actual
                fecha_inicial_ano = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%dT%H:%M:%S')

                if 'from_date' in args:
                    fecha_inicial_ano = args['from_date']

                # Fecha actual
                fecha_actual = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                if 'to_date' in args:
                    fecha_actual = args['to_date']

                data = self.payroll.get_nomina(periodoInicial=fecha_inicial_ano, periodoFinal=fecha_actual)
                return self.process_call(question=text, data=data, name="nominas", description="datos de algunos periodos de nomina", key_words=key_words)
                
        
                    #Registrar una ausencia
                     
            #Registrar una ausencia
            if function_name == "set_ausencia":
                
                # Validar parámetros requeridos
                is_valid, error_message = validate_params(args, ["employee_id", "from_date", "to_date"])
                if not is_valid:
                    return error_message
                
                employeeID = args['employee_id']
                comment = args.get("comment", "creado via Asistant")
                

                key_words = args.get("key_words", [])

                # Mapa de palabras clave a códigos de razón
                reason_codes = {
                    "vacaciones": 1,
                    "licencia": 2,
                    "permiso_dias": 3,
                    "permiso_horas": 4,
                    "excusa": 5
                }

                # Buscar el código correspondiente al primer valor coincidente
                reason_code = next((reason_codes[k] for k in key_words if k in reason_codes), 0)


                
                body = [{
                    "Id_AccionWeb": 12,
                    "Id_Registro_Relacionado": employeeID,
                    "Fecha_Inicio": args['from_date'],
                    "Fecha_Fin": args['to_date'],
                    "Comentario": comment,
                    "Tipo_Ausencia": reason_code
                }]
                response = r.post(url=f"{st.session_state.baseUrl}/empleados/TransaccionAccionPersonalEmpleado", headers=RRHH_HEADERS, data=json.dumps(body))
                
                if response.status_code == 200:
                    return "La ausencia ha sido registrada."
                else:
                    return f"Error al registrar la ausencia: {response.status_code} {response.text}", None
        
            return self.get_response(question=text, historial=filtered_messages)
        else:
            return self.get_response(question=text, historial=filtered_messages)
    
   
    def process_functions(self, text, historial=[]):
        """
        Maneja la llamada de funciones por el asistente.

        Args:
            text (str): El texto de entrada del usuario.
            historial (list): Lista de mensajes anteriores en la conversación.

        Returns:
            tuple: Contiene el nombre de la función, los argumentos y el mensaje de respuesta.
        """
        
        
        # Se realiza una llamada a la API de OpenAI (debe reemplazarse 'client' con la instancia correcta de OpenAI)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.rol},
                {"role": "user", "content": text},
                *historial,
            ],
            functions=functions,
            function_call="auto"
        )

        choice = response.choices[0]
        function_call = choice.message.function_call
        message = choice.message


        if function_call is not None:
            function_name = function_call.name
            args = json.loads(function_call.arguments.replace("'", '"')) 
            print(function_name, args, message)
            return function_name, args, message
        else:
            return None, None, message
    
    def process_call(self, question, data, name=None, description=None, key_words = [], output_type=None):
        """
        Procesa la pregunta del usuario usando pandasai.
        Args:
            :param question: texto a consultar por el usuario a la IA.
            :type:str
            
            :param data: diccionario de datos con la informacion a consultar.
            :type: dic
            
            :param name (opcional): nombre que se le asignara al dataframe generado desde data. 
            :type: str
            
            :param desciption (opcional): descripcion que se le asignara al dataframe generado desde data. 
            :type: str
        
        return:
            response: retorna respuesta del modelo str    
        
        """
        df = pd.DataFrame(data)
        print(df)
        self.sdf = SmartDataframe(df, config={"llm": bllm, "open_charts":False}, name=name, description=description)
        df.to_markdown
        response = None
        if output_type:
            response = self.sdf.chat(question, output_type=output_type)
        else:
            response = self.sdf.chat(question)
            

        if isinstance(response, pd.DataFrame): 
                return response

        # Lista de tipos de datos enteros en NumPy
        tipos_enteros = (int, np.int8, np.int16, np.int32, np.int64)
        if isinstance(response, tipos_enteros): 
            return str(response)
        
        # Lista de tipos de datos enteros en NumPy
        tipos_floats = (float, np.float16, np.float32, np.float64)
        if isinstance(response, tipos_floats): 
            return str(response)
        
            
        if es_ruta(response):
            img_base64 = png_to_base64(response)
            return img_base64
        

        return response

        
            
            
             
        
    def get_response(self, question, historial=[]):
        """ Procesa la pregunta del usuario sin analizar datos solo el historial"""
        
        filtered_messages = clear_history(historial)
        
        messages = [
            {"role": "system", "content": self.rol},
            *filtered_messages,
            {"role": "user", "content": question},
            
        ]
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message.content
