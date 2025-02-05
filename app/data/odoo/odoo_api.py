import xmlrpc.client
import ssl

class OdooAPI:
    def __init__(self, url=None, db=None, username=None, password=None):
        """
        Inicializa la conexión al sistema Odoo.
        
        :param url: URL del servidor Odoo.
        :param db: Base de datos de Odoo.
        :param username: Usuario para autenticar.
        :param password: Contraseña del usuario.
        """
        context = ssl._create_unverified_context()
        #info = xmlrpc.client.ServerProxy('https://demo-do.digitalgroup.net', context=context).start()
        #url, db, username, password = info['host'], info['database'], info['user'], info['password']

        self.url = "https://demo-do.digitalgroup.net"
        self.db = "demo-do"
        self.username = "admin"
        self.password = "admin"


        
        # Conexión y autenticación
        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.uid = self.common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")


    def consultar_modulos(self) -> list:
            
        installed_modules = self.models.execute_kw(
            self.db, self.uid, self.password,
            "ir.module.module", "search_read",
            [[["state", "=", "installed"]]],  # Filtrar solo módulos instalados
            {"fields": ["name", "shortdesc", "state"]}
        )


        return installed_modules
    
        # for module in installed_modules:
        #     print(f"Nombre: {module['name']}, Descripción: {module['shortdesc']}, Estado: {module['state']}")


    def consultar_odoo(self, modulo, filtro=None, campos_a_recuperar=None, estado="todos", 
                   fecha_desde=None, fecha_hasta=None, limite=100, ordenar_por="name", orden="asc"):
        """Consulta registros en diferentes módulos de Odoo."""

        # Definir el modelo de Odoo según el módulo seleccionado
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

        if modulo not in modelos_odoo:
            return f"Módulo '{modulo}' no soportado. Debe ser: {', '.join(modelos_odoo.keys())}"
            #raise ValueError(f"Módulo '{modulo}' no soportado. Debe ser: {', '.join(modelos_odoo.keys())}")

        modelo = modelos_odoo[modulo]
        domain = []

        # Filtros comunes
        if filtro:
            domain.append(["name", "ilike", filtro])
        if estado != "todos":
            domain.append(["state", "=", estado])
        if fecha_desde:
            domain.append(["date_order" if modulo in ["ventas", "compras"] else "date", ">=", fecha_desde])
        if fecha_hasta:
            domain.append(["date_order" if modulo in ["ventas", "compras"] else "date", "<=", fecha_hasta])

        print(domain)

        # Definir los campos predeterminados por módulo

        campos_por_defecto = {
            "ventas": ["name", "partner_id", "amount_total", "state", "date_order"],
            "compras": ["name", "partner_id", "amount_total", "state", "date_order"],
            "contabilidad": ["name", "partner_id", "amount_total", "state", "invoice_date"],
            "gastos": ["name", "employee_id", "total_amount", "state", "date"],
            "facturacion": ["name", "partner_id", "amount_total", "state", "invoice_date"],
            "contactos": ["name", "email", "phone", "company_id", "customer_rank"],
            "proyectos": ["name", "user_id", "company_id", "date_start", "date"],
            "tareas": ["name", "project_id", "user_id", "stage_id", "date_deadline"],
            "inventario": ["name", "partner_id", "scheduled_date", "state", "move_type"],
            "produccion": ["name", "product_id", "product_qty", "state", "date_planned_start"],
            "empleados": ["name", "job_title",  "department_id", "company_id", "hourly_cost"],
            "nomina": ["name", "employee_id", "state", "date_from", "date_to", "net_wage"],
            "crm": ["name", "partner_id", "stage_id", "expected_revenue", "date_open"]
        }


        campos_a_recuperar = campos_a_recuperar or campos_por_defecto[modulo]

        # Ejecutar la consulta en Odoo
        registros = self.models.execute_kw(
            self.db, self.uid, self.password,
            modelo, 'search_read',
            [domain],  # Aplicar los filtros
            {
                'fields': campos_a_recuperar,
                'limit': limite,
                'order': f"{ordenar_por} {orden}"
            }
        )

        # Formatear listas dentro de los resultados
        for i, registro in enumerate(registros):
            for key, value in registro.items():
                if isinstance(value, list):
                    registros[i][key] = "-".join(map(str, value))

        return registros


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
    

    def consultar_ventas(self, filtro, campos_a_recuperar=None, estado="todos", fecha_desde=None, fecha_hasta=None, limite=100, ordenar_por="name", orden="asc"):
        """Consulta órdenes de venta en el módulo de Ventas."""
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
        
        # Llamada al modelo 'sale.order'
        ventas = self.models.execute_kw(
            self.db, self.uid, self.password,
            'sale.order', 'search_read',
            [domain],  # Domain filters
            {
                'fields': campos_a_recuperar or ['name', 'partner_id', 'amount_total', 'state', 'date_order'],
                'limit': limite,
                'order': f"{ordenar_por} {orden}",
            }
        )

        # Convertir listas en strings para evitar listas anidadas
        for i, venta in enumerate(ventas):
            for key, value in venta.items():
                if isinstance(value, list):
                    ventas[i][key] = "-".join(map(str, value))

        return ventas

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


    def consultar_contabilidad(self, tipo, filtro=None, estado="todos", fecha_desde=None, fecha_hasta=None, 
                            campos_a_recuperar=None, moneda=None, limite=100, ordenar_por="date", orden="asc"):
        """
        Consulta registros contables del módulo de contabilidad en Odoo.

        :param tipo: Tipo de registro ('factura', 'pago', 'movimiento', 'diario', 'banco').
        :param filtro: Criterio de búsqueda.
        :param estado: Estado del registro ('borrador', 'publicado', 'pagado', 'cancelado', 'todos').
        :param fecha_desde: Fecha inicial (YYYY-MM-DD).
        :param fecha_hasta: Fecha final (YYYY-MM-DD).
        :param campos_a_recuperar: Lista de campos a recuperar.
        :param moneda: Moneda de los registros ('USD', 'EUR', etc.).
        :param limite: Número máximo de registros a devolver.
        :param ordenar_por: Campo para ordenar los resultados ('fecha', 'número', etc.).
        :param orden: Dirección del orden ('asc', 'desc').
        :return: Lista de registros contables.
        """
        # Mapear tipos a modelos y configuraciones específicas
        model_map = {
            "factura": {"model": "account.move", "filter": [("move_type", "in", ["out_invoice", "in_invoice"])]},
            "pago": {"model": "account.payment", "filter": []},
            "movimiento": {"model": "account.move.line", "filter": []},
            "diario": {"model": "account.move", "filter": [("state", "=", "posted")]},
            "banco": {"model": "account.payment", "filter": [("payment_method_id.code", "ilike", "bank")]},
        }

        if tipo not in model_map:
            raise ValueError("El parámetro 'tipo' debe ser uno de: 'factura', 'pago', 'movimiento', 'diario', 'banco'.")

        # Obtener modelo y filtros base para el tipo
        model_info = model_map[tipo]
        model_name = model_info["model"]
        domain = model_info["filter"]

        # Agregar filtros personalizados
        if filtro:
            domain.append(["name", "ilike", filtro])
        if estado != "todos":
            state_field = "state" if tipo != "movimiento" else "reconciled"
            domain.append([state_field, "=", estado])
        if fecha_desde:
            domain.append(["date", ">=", fecha_desde])
        if fecha_hasta:
            domain.append(["date", "<=", fecha_hasta])
        if moneda:
            domain.append(["currency_id.name", "=", moneda])

        # Campos por defecto si no se especifican
        default_fields = {
            "factura": ["name", "partner_id", "amount_total", "state", "date"],
            "pago": ["name", "partner_id", "amount", "state", "date"],
            "movimiento": ["name", "account_id", "debit", "credit", "date"],
            "diario": ["name", "journal_id", "amount_total", "state", "date"],
            "banco": ["name", "partner_id", "amount", "payment_date", "state"],
        }
        fields = campos_a_recuperar or default_fields.get(tipo, ["name", "date"])

        # Llamada al modelo de Odoo
        try:
            registros = self.models.execute_kw(
                self.db, self.uid, self.password,
                model_name, 'search_read',
                [domain],
                {
                    'fields': fields,
                    'limit': limite,
                    'order': f"{ordenar_por} {orden}",
                }
            )
            return registros

        except Exception as e:
            print(f"Error al consultar {tipo}: {e}")
            raise


    def consultar_gastos(self, filtro, campos_a_recuperar=None, estado="todos", fecha_desde=None, fecha_hasta=None, limite=100, ordenar_por="name", orden="asc"):
        """Consulta reportes de gastos en el módulo de Gastos."""
        domain = []

        # Filtros según los parámetros
        if filtro:
            domain.append(["name", "ilike", filtro])
        if estado != "todos":
            domain.append(["state", "=", estado])
        if fecha_desde:
            domain.append(["date", ">=", fecha_desde])
        if fecha_hasta:
            domain.append(["date", "<=", fecha_hasta])
        
        # Llamada al modelo 'hr.expense'
        gastos = self.models.execute_kw(
            self.db, self.uid, self.password,
            'hr.expense', 'search_read',
            [domain],  # Domain filters
            {
                'fields': campos_a_recuperar or ['name', 'employee_id', 'total_amount', 'state', 'date'],
                'limit': limite,
                'order': f"{ordenar_por} {orden}",
            }
        )

        # Convertir listas en strings para evitar listas anidadas
        for i, gasto in enumerate(gastos):
            for key, value in gasto.items():
                if isinstance(value, list):
                    gastos[i][key] = "-".join(map(str, value))

        return gastos
    
    def consultar_inventarios(self, filtro, campos_a_recuperar=None, estado="todos", almacen=None, fecha_desde=None, fecha_hasta=None, limite=100, ordenar_por="name", orden="asc"):
        """Consulta productos y movimientos de inventario en el módulo de Inventarios de Odoo."""
        domain = []

        # Filtros según los parámetros
        if filtro:
            domain.append(["name", "ilike", filtro])
        if estado != "todos":
            if estado == "disponible":
                domain.append(["qty_available", ">", 0])
            elif estado == "reservado":
                domain.append(["reserved_quantity", ">", 0])
            elif estado == "agotado":
                domain.append(["qty_available", "=", 0])
        if almacen:
            domain.append(["warehouse_id", "ilike", almacen])
        if fecha_desde:
            domain.append(["write_date", ">=", fecha_desde])
        if fecha_hasta:
            domain.append(["write_date", "<=", fecha_hasta])

        # Llamada al modelo 'stock.quant' (inventario disponible)
        inventarios = self.models.execute_kw(
            self.db, self.uid, self.password,
            'stock.quant', 'search_read',
            [domain],  # Domain filters
            {
                'fields': campos_a_recuperar or ['name', 'product_id', 'location_id', 'qty_available', 'reserved_quantity', 'warehouse_id'],
                'limit': limite,
                'order': f"{ordenar_por} {orden}",
            }
        )

        # Convertir listas en strings para evitar listas anidadas
        for i, inventario in enumerate(inventarios):
            for key, value in inventario.items():
                if isinstance(value, list):
                    inventarios[i][key] = "-".join(map(str, value))

        return inventarios


# Ejemplo de uso
if __name__ == "__main__":
    # Configuración
    url = "https://miodoo.com"
    db = "mi_base_datos"
    username = "mi_usuario"
    password = "mi_contraseña"
    
    # Instancia de la API
    odoo_api = OdooAPI(url, db, username, password)
    #modules = odoo_api.consultar_modulos()
    #print(modules[0:3])
    # # Consulta de empleados
    # empleados = odoo_api.consultar_compras(
    #     filtro=None
    # )
    # Consulta de empleados


    data = odoo_api.consultar_odoo(
        modulo='ventas')
    
    print(data)
    
    # # Imprimir resultados
    # for emp in empleados:
    #     print(emp)
    
    # facturas = odoo_api.consultar_contabilidad(
    #     tipo="factura",
    #     filtro="INV123",
    #     estado="publicado",
    #     fecha_desde="2024-01-01",
    #     fecha_hasta="2024-12-31",
    #     campos_a_recuperar=["name", "partner_id", "amount_total", "state", "date"],
    #     moneda="USD",
    #     limite=10,
    #     ordenar_por="date",
    #     orden="desc"
    # )
    # print(facturas)


    # movimientos = odoo_api.consultar_contabilidad(
    #     tipo="movimiento",
    #     fecha_desde="2024-01-01",
    #     fecha_hasta="2024-12-31",
    #     limite=20
    #     )
    
    # print(movimientos)


    # pagos = odoo_api.consultar_contabilidad(
    #     tipo="pago",
    #     filtro=None,
    #     estado="pagado",
    #     fecha_desde="2024-01-01",
    #     fecha_hasta="2024-12-31",
    #     limite=5
    # )
    # print(pagos)
