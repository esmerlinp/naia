from app.database import Database


employees_keywords = ["prestamos", "ausencias", "transacciones", "licencias", "permisos", "beneficios", "volantes_pagos", "habilidades", 
                      "herramientas", "capacitaciones", "dependientes", "familiares", "amonestaciones", "seguros", "salud", "medicos", "planes", 
                      "promocion", "cambio_puesto", "centro_costos", "educacion", "experiencia", "tabla", "grafico", "cambio_salario", "cambio_sucursal", "cambio_compania"]

functions = [
                {
                    "name": "get_employee_image",
                    "description": "Recupera la foto de perfil del empleado por su id o nombre",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "employee_ids": {
                                "type": "array",
                                "description": "Lista de ids de empleados",
                                "items": {
                                    
                                    "type": "integer",
                                    "description": "id del sistema del empleado"
                                }
                            },
                            "employee_names": {
                                "type": "array",
                                "description": "Lista de nombres de empleados",
                                "items": {
                                    "type": "string",
                                    "description": "Nombre del empleado"
                                }
                            }
                         },
                        #"required": ["employee_ids"],  
                    }
                },
                {
                    "name": "get_employees",
                    "description": "Recupera una lista de empleados del sistema.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "employee_ids": {
                                "type": "array",
                                "description": "Lista de ids de empleados",
                                "items": {
                                    "type": "integer",
                                    "description": "id del sistema del empleado"
                                }
                            },
                            "identificaciones": {
                                "type": "array",
                                "description": "Lista Pasaportes o cédulas de empleados",
                                "items": {
                                    "type": "string",
                                    "description": "Pasaporte o cédula del empleado"
                                }
                            },
                            "employee_names": {
                                "type": "array",
                                "description": "Lista de nombres de empleados",
                                "items": {
                                    "type": "string",
                                    "description": "Nombre del empleado"
                                }
                            },
                            "key_words": {
                                "type": "array",
                                "description": "Lista de acciones que se desean consultar. Ejemplo: 'prestamos', 'ausencias' (vacaciones, licencias, permisos), 'beneficios'.",
                                "items": {
                                    "type": "string",
                                    "enum": employees_keywords,
                                    "description": "Acción específica a consultar"
                                },
                                "minItems": 1,  # Asegura que la lista tenga al menos una acción
                                "uniqueItems": True  # Evita que se repitan las acciones en la lista
                            }
                        },
                        #"required": ["employee_id"],  # 'accion' es opcional, pero si está presente debe ser válida
                        "additionalProperties": True  # Evita que se añadan propiedades no definidas
                    }
                },
                {
                    "name": "set_ausencia",
                    "description": "Registra una ausencia para un empleado, incluyendo licencias médicas, excusas, y permisos (días completos o por horas). Esta funcionalidad permite gestionar las ausencias del personal indicando fechas, horas y una razón específica.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "employee_id": {
                                "type": "integer",
                                "description": "El identificador único del empleado que está registrando la ausencia."
                            },
                            "from_date": {
                                "type": "string",
                                "description": "Fecha de inicio de la ausencia, en formato mes/dia/año (mm/dd/yyyy)."
                            },
                            "to_date": {
                                "type": "string",
                                "description": "Fecha de finalización de la ausencia, en formato mes/dia/año (mm/dd/yyyy)."
                            },
                            "from_hour": {
                                "type": "string",
                                "description": "Hora de inicio del permiso (si aplica a horas). Especificar en formato de 24 horas (HH:mm)."
                            },
                            "to_hour": {
                                "type": "string",
                                "description": "Hora de finalización del permiso (si aplica a horas). Especificar en formato de 24 horas (HH:mm)."
                            },
                            "comment": {
                                "type": "string",
                                "description": "Comentario opcional sobre la ausencia o motivo adicional relacionado con la solicitud."
                            },
                            "key_words": {
                                "type": "array",
                                "description": "Lista de tipos de ausencia que se pueden aplicar. Ejemplos: 'vacaciones', 'licencia', 'excusa', 'permiso_dias' o 'permiso_hora'. Los permisos por día abarcan una jornada completa, mientras que los permisos por horas cubren solo una parte del día, como 4 horas.",
                                "items": {
                                    "type": "string",
                                    "enum": ["vacaciones", "licencia", "excusa", "permiso_dias", "permiso_hora"],
                                    "description": "Tipo de permiso o ausencia que se aplica. Permiso por días cubre toda una jornada laboral, y permiso por horas cubre una fracción del día laboral."
                                },
                                "minItems": 1,
                                "uniqueItems": True
                            }
                        },
                        "required": ["employee_id", "reason", "from_date", "to_date"]
                    }
                },
                {
                    "name": "get_candidatos",
                    "description": "Recupera una lista de candidatos elegibles que han aplicado para una posición específica o varias posiciones abiertas en la empresa. Esta búsqueda puede incluir detalles como el nombre del candidato, su experiencia, competencias, estado de la aplicación y otros datos relevantes que permitan evaluar su adecuación para el puesto.",
                    "parameters": {
                        "type": "object",
                        "properties": { }
                    }
                },
                {
                    "name": "get_requisiciones",
                    "description": "Recupera una lista de requisiciones de personal activas en la empresa. Estas requisiciones representan posiciones abiertas que la organización está buscando cubrir. El resultado puede incluir información como el título del puesto, la fecha de publicación, el departamento solicitante, el estado de la requisición, y otros detalles relevantes.",
                    "parameters": {
                        "type": "object",
                        "properties": { }
                    }
                },
                {
                    "name": "get_solicitudes_empleo",
                    "description": "Recupera una lista solicitudes de empleo realizadas a la compañía.",
                    "parameters": {
                        "type": "object",
                        "properties": { }
                    }
                },
                {
                    "name": "get_nominas",
                    "description": "Recupera una lista  de datos de nominas generadas.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "from_date": {
                                "type": "string",
                                "description": "Fecha de inicio, en formato ISO 8601  (yyyy-MM-ddTHH:mm:ss)."
                            },
                            "to_date": {
                                "type": "string",
                                "description": "Fecha de finalización, en formato ISO 8601  (yyyy-MM-ddTHH:mm:ss)."
                            },
                            "key_words": {
                                "type": "array",
                                "description": "Lista de acciones que se desean consultar.",
                                "items": {
                                    "type": "string",
                                    "enum": ["tabla", "grafico"],
                                    "description": "Acción específica a consultar"
                                },
                                "minItems": 1,  # Asegura que la lista tenga al menos una acción
                                "uniqueItems": True  # Evita que se repitan las acciones en la lista
                            }
                         }
                    }
                },
    
            ]


# def get_funtions():
#     db = Database()
#     fuentes = db.get_fuentes_externas()
    
#     # Inicializar la lista de funciones externas
#     external_functions = []
    
#     if fuentes:
#         for fuente in fuentes:
#             # Construir la descripción incluyendo el tipo de archivo y contexto adicional
#             description = f"{fuente[2]}: csv : {fuente[4]}"
            
#             # Crear el diccionario de parámetros para cada fuente
#             f = {
#                 "name": fuente[1],  # Nombre de la fuente
#                 "description": description,
#                 "parameters": {
#                     "type": "object",
#                     "properties": { 
#                         "key_words": {
#                             "type": "array",
#                             "description": "Lista de acciones que se desean consultar del archivo.",
#                             "items": {
#                                 "type": "string",
#                                 "enum": fuente[3].split(","),
#                                 "description": "Acción específica a consultar"
#                             },
#                             "minItems": 1,  # Asegura que la lista tenga al menos una acción
#                             "uniqueItems": True  # Evita que se repitan las acciones en la lista
#                         }    
#                     }
#                 }
#             }
#             # Añadir la función configurada a la lista de funciones externas
#             external_functions.append(f)

#     # Devolver la lista de funciones configuradas o una lista vacía si no hay fuentes
#     functions.extend(external_functions)
#     return functions

    
