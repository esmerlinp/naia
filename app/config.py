import streamlit as st

RRHH_BASE_URL = "http://rrhh.administracionapi.camsoft.com.do:8086"
authorization = ""
RRHH_HEADERS = {'Content-type': 'application/json',
               'x-api-key': '002002032323232320002SSS',
               'x-ui-culture': 'es-DO',
               'Authorization':  authorization,  
            }

DISCLAIMER = """El asistente de recursos humanos ha sido diseñado exclusivamente para asistir a empleados de Recursos Humanos y a la gerencia en la gestión de operaciones relacionadas con el empleo, la nómina y el reclutamiento. Aunque el asistente proporciona información y facilita ciertas tareas, no sustituye la revisión o validación de los procesos por parte del equipo de Recursos Humanos ni garantiza la exactitud absoluta de la información proporcionada.
\nToda acción realizada o consulta resuelta por el asistente debe ser revisada y aprobada conforme a las políticas y procedimientos internos de la empresa. Las decisiones finales, como la aprobación de solicitudes, la gestión de pagos o cualquier asunto contractual, están bajo la autoridad del Departamento de Recursos Humanos.
\nImportante: El uso del asistente implica la aceptación de los términos y condiciones del servicio, así como el respeto a la confidencialidad y seguridad de la información personal y de la empresa. Para asuntos complejos o críticos, se recomienda contactar directamente con el equipo de Recursos Humanos."""


LOREM_IPSU = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

INITIAL_MSG = """**Hola**, soy tu asistente virtual.\n 
Mi función es proporcionar asistencia y responder preguntas relacionadas exclusivamente con la gestión de recursos humanos, especialmente sobre los empleados de la empresa y el registro de ausencias, como licencias, vacaciones y permisos. Actualmente, no tengo acceso a información sobre nómina, reclutamiento o políticas de la empresa, ya que están en proceso de revisión. Por lo tanto, no puedo proporcionar datos sobre esos temas.

**Puedes hacerme preguntas como:**

¿Cuántas ausencias tiene un empleado?\n
¿Cuántos días de vacaciones le quedan a un empleado?\n
Muestra una tabla con el nombre, departamento y salario de cada empleado ordenados por el salario de mayor a menor.\n
Genera un gráfico de barras del número de empleados por departamento.\n
Muestra una tabla de empleados que han sido promovidos en los últimos 2 años, incluyendo fecha de promoción, puesto actual y anterior.\n
"""