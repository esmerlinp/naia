import xmlrpc.client
import ssl
import json

class OdooEmployeeAPI:
    def __init__(self, url=None, db=None, username=None, password=None):
        """
        Inicializa la conexión al sistema Odoo.
        
        :param url: URL del servidor Odoo.
        :param db: Base de datos de Odoo.
        :param username: Usuario para autenticar.
        :param password: Contraseña del usuario.
        """
        context = ssl._create_unverified_context()
        info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start', context=context).start()
        url, db, username, password = info['host'], info['database'], info['user'], info['password']

        self.url = url
        self.db = db
        self.username = username
        self.password = password


        
        # Conexión y autenticación
        self.common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        self.uid = self.common.authenticate(db, username, password, {})
        self.models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    


    def consultar_compras(self, filtro, campos_a_recuperar=None, estado="todos", fecha_desde=None, fecha_hasta=None, limite=100, ordenar_por="name", orden="asc"):
        """Consulta órdenes de compra en el módulo de Compras."""
        domain = []

        # Filtros según los parámetros
        if filtro:
            domain.append(["name", "ilike", filtro])
        if estado != "todos":
            domain.append(["state", "=", estado])
        if fecha_desde:
            domain.append(["date_order", ">=", fecha_desde])
        if fecha_hasta:
            domain.append(["date_order", "<=", fecha_hasta])
        
        # Llamada al modelo 'purchase.order'
        compras = self.models.execute_kw(
            self.db, self.uid, self.password,
            'purchase.order', 'search_read',
            [domain],  # Domain filters
            {
                'fields': campos_a_recuperar or ['name', 'partner_id', 'amount_total', 'state', 'date_order'],
                'limit': limite,
                'order': f"{ordenar_por} {orden}",
            }
        )

        for i, compra in enumerate(compras):
                for key, value in compra.items():
                    if isinstance(value, list):
                        compras[i][key] = "-".join(map(str, value))

        return compras
    

    def consultar_empleados(self, filtro, campos_a_recuperar=None, estado="todos", limite=100, ordenar_por="nombre", orden="asc"):
        """
        Consulta información de empleados en el sistema Odoo.
        
        :param filtro: Criterio de búsqueda (nombre, email, departamento, etc.).
        :param campos_a_recuperar: Lista de campos que se desean recuperar.
        :param estado: Filtrar empleados por 'activo', 'inactivo' o 'todos'.
        :param limite: Número máximo de resultados a devolver.
        :param ordenar_por: Campo por el cual ordenar los resultados.
        :param orden: Dirección del orden ('asc' o 'desc').
        :return: Lista de empleados que coinciden con los criterios.
        """


        relevant_properties = [
            # Identificación básica
            'id',                  # ID del empleado
            'name',                # Nombre del empleado
            'legal_name',          # Nombre legal del empleado

            # Puesto y compañía
            'job_title',           # Título del puesto
            'department_id',       # Departamento al que pertenece
            'company_id',          # Empresa asociada

            # Contacto laboral
            'work_email',          # Correo electrónico laboral
            'work_phone',          # Teléfono laboral
            'address_id',          # Dirección laboral
            'work_location_name',  # Nombre de la ubicación laboral

            # Estado laboral y permisos
            #'manager_id',          # Gerente asociado
            'hr_presence_state',   # Estado de presencia
            'is_absent',           # Indicador de ausencia
            'remaining_leaves',    # Días restantes de permisos

            # Datos personales
            'birthday',            # Fecha de nacimiento
            'gender',              # Género
            'marital',             # Estado civil
            'spouse_complete_name',# Nombre del cónyuge
            'children',            # Número de hijos
            'place_of_birth',      # Lugar de nacimiento
            'country_of_birth',    # País de nacimiento

            # Contacto personal
            'private_email',       # Correo personal
            'private_phone',       # Teléfono personal

            # Dirección personal
            'private_street',      # Calle de la dirección personal
            'private_street2',     # Complemento de la dirección personal
            'private_city',        # Ciudad de la dirección personal
            'private_state_id',    # Estado o región de la dirección personal
            'private_zip',         # Código postal de la dirección personal
            'private_country_id',  # País de la dirección personal

            # Otros datos
            'employee_type',       # Tipo de empleado
            'currency_id',         # Moneda
            'hourly_cost',         # Costo por hora
            'related_partners_count', # Cantidad de socios relacionados
            'create_date',         # Fecha de creación del registro
            'write_date',          # Última modificación del registro
            'passport_id',         # Representa el número de pasaporte del empleado
            'sinid',               # Social Insurance Number (SIN), que es un número único utilizado en Canadá.
            'ssnid'                # Social Security Number (SSN), utilizado en los Estados Unidos
        ]

        domain = []
        
        # Filtro por nombre o campo general
        if filtro:
            domain.append(['name', 'ilike', filtro])
        
        # Filtro por estado
        if estado == "activo":
            domain.append(['active', '=', True])
        elif estado == "inactivo":
            domain.append(['active', '=', False])
        
        # Campos a recuperar
        if not campos_a_recuperar:
            campos_a_recuperar = relevant_properties
        
        # Ordenar resultados
        order = f"{ordenar_por} {orden}"
        
        # Llamada al modelo de empleados
        try:
            empleados = self.models.execute_kw(
                self.db,
                self.uid,
                self.password,
                'hr.employee',  # Modelo de empleados en Odoo
                'search_read',  # Método para buscar y leer datos
                [domain],
                {
                    'fields': campos_a_recuperar,
                    'limit': limite,
                    'order': order
                }
            )
            
            for i, empleado in enumerate(empleados):
                for key, value in empleado.items():
                    if isinstance(value, list):
                        empleados[i][key] = "-".join(map(str, value))

            print(empleados[0])
            return empleados
        except Exception as e:
            print(f"Error al consultar empleados: {e}")
            return []

# Ejemplo de uso
if __name__ == "__main__":
    # Configuración
    url = "https://miodoo.com"
    db = "mi_base_datos"
    username = "mi_usuario"
    password = "mi_contraseña"
    
    # Instancia de la API
    odoo_api = OdooEmployeeAPI(url, db, username, password)
    
    # Consulta de empleados
    empleados = odoo_api.consultar_compras(
        filtro=None
    )
    
    # Imprimir resultados
    for emp in empleados:
        print(emp)
