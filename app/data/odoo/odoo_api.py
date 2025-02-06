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
        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common", context=context)
        self.uid = self.common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object", context=context)


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
            "ventas": ['id', 'name', 'partner_id', 'state', 'client_order_ref', 'date_order', 'validity_date', 'amount_untaxed', 'amount_tax', 'amount_total', 'currency_id', 'user_id', 'team_id', 'invoice_status', 'order_line', 'payment_term_id', 'pricelist_id', 'note'],
            "compras": ['id', 'name', 'partner_id', 'partner_ref', 'state', 'date_order', 'date_approve', 'currency_id', 'order_line', 'amount_untaxed', 'amount_tax', 'amount_total', 'invoice_status', 'invoice_count', 'payment_term_id', 'notes', 'user_id'],
            "contabilidad": ['id', 'name', 'ref', 'date', 'state', 'move_type', 'journal_id', 'partner_id', 'currency_id', 'amount_untaxed', 'amount_tax', 'amount_total', 'amount_residual', 'invoice_date', 'invoice_date_due', 'payment_state', 'invoice_user_id', 'invoice_origin', 'invoice_payment_term_id', 'payment_reference', 'narration'],
            "gastos": ['id', 'name', 'date', 'employee_id', 'product_id', 'product_description', 'quantity', 'description', 'state', 'total_amount', 'currency_id', 'price_unit', 'tax_amount', 'payment_mode', 'account_id', 'approved_by', 'approved_on'],
            "facturacion": ['id', 'name', 'ref', 'date', 'state', 'move_type', 'journal_id', 'company_id', 'partner_id', 'commercial_partner_id', 'invoice_date', 'invoice_date_due', 'payment_reference', 'currency_id', 'amount_untaxed', 'amount_tax', 'amount_total', 'amount_residual', 'tax_totals', 'payment_state', 'invoice_line_ids', 'invoice_origin', 'invoice_user_id', 'user_id', 'display_name', 'create_uid', 'create_date', 'write_uid', 'write_date'],
            "contactos": ['id', 'name', 'complete_name', 'company_name', 'is_company',  'email', 'phone', 'mobile', 'website', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id', 'vat', 'company_registry', 'category_id', 'user_id',  'commercial_partner_id', 'customer_rank', 'supplier_rank', 'credit', 'debit', 'credit_limit', 'total_invoiced', 'property_account_payable_id', 'property_account_receivable_id', 'sale_order_count', 'invoice_ids', 'purchase_order_count', 'contact_address', 'display_name', 'create_uid', 'create_date', 'write_uid', 'write_date'],
            "proyectos": ["name", "user_id", "company_id", "date_start", "date"],
            "tareas": ['id', 'name', 'description', 'priority', 'sequence',  'state', 'stage_id', 'tag_ids', 'create_date', 'write_date',  'date_deadline', 'date_assign', 'date_end', 'date_last_stage_update', 'project_id', 'partner_id', 'company_id', 'user_ids', 
                        'allocated_hours', 'effective_hours', 'remaining_hours', 'total_hours_spent',  
                        'progress', 'subtask_count', 'closed_subtask_count', 'parent_id', 'child_ids',  
                        'allow_task_dependencies', 'depend_on_ids', 'dependent_ids', 'dependent_tasks_count',  
                        'allow_timesheets', 'timesheet_ids', 'timesheet_product_id', 'analytic_account_id',  
                        'sale_order_id', 'sale_line_id', 'task_to_invoice', 'invoice_status', 'invoice_count',  
                        'quotation_count', 'currency_id', 'display_create_invoice_primary',  
                        'fsm_done', 'worksheet_count', 'worksheet_template_id', 'worksheet_signed_by',  
                        'create_uid', 'write_uid', 'display_name'
                    ],
            "inventario": [
                        'id', 'name', 'origin', 'note', 'state', 'priority',  
                        'scheduled_date', 'date_deadline', 'date_done', 'delay_alert_date',  
                        'location_id', 'location_dest_id', 'picking_type_id', 'picking_type_code',  
                        'partner_id', 'company_id', 'user_id', 'move_ids', 'move_line_ids',  
                        'product_id', 'lot_id', 'has_tracking', 'has_scrap_move', 'has_packages',  
                        'picking_properties', 'show_operations', 'show_reserved',  
                        'package_ids', 'weight', 'weight_uom_name', 'shipping_weight',  
                        'carrier_id', 'carrier_tracking_ref', 'carrier_tracking_url', 'delivery_type',  
                        'purchase_id', 'sale_id', 'is_return_picking', 'return_id', 'return_count',  
                        'quality_check_todo', 'quality_check_fail', 'quality_alert_count',  
                        'is_repairable', 'repair_ids', 'nbr_repairs',  
                        'create_uid', 'create_date', 'write_uid', 'write_date', 'display_name'
                    ],
            "produccion": ["name", "product_id", "product_qty", "state", "date_planned_start"],
            "empleados": [
                        'id', 'name', 'active', 'color', 'company_id', 'department_id', 'job_id', 'job_title',
                        'address_id', 'work_phone', 'mobile_phone', 'work_email', 'user_id', 'parent_id', 'coach_id',
                        'hr_presence_state', 'last_activity', 'last_activity_time', 'newly_hired', 'leave_manager_id',
                        'remaining_leaves', 'current_leave_state', 'leave_date_from', 'leave_date_to', 'is_absent',
                        'lang', 'gender', 'marital', 'spouse_complete_name', 'spouse_birthdate', 'children',
                        'place_of_birth', 'country_of_birth', 'birthday', 'ssnid', 'sinid', 'identification_id',
                        'passport_id', 'bank_account_id', 'permit_no', 'visa_no', 'visa_expire',
                        'work_permit_expiration_date', 'has_work_permit', 'study_field', 'study_school',
                        'emergency_contact', 'emergency_phone', 'km_home_work', 'employee_type', 'category_ids',
                        'notes', 'barcode', 'departure_reason_id', 'departure_description', 'departure_date',
                        'id_card', 'driving_license', 'private_car_plate', 'currency_id', 'next_appraisal_date',
                        'last_appraisal_date', 'related_partner_id', 'appraisal_count', 'attendance_manager_id',
                        'attendance_state', 'hours_last_month', 'hours_today', 'total_overtime', 'vehicle',
                        'contract_ids', 'contract_id', 'contracts_count', 'contract_warning', 'first_contract_date',
                        'employee_cars_count', 'license_plate', 'mobility_card', 'hourly_cost', 'equipment_ids',
                        'equipment_count', 'resume_line_ids', 'employee_skill_ids', 'skill_ids',
                        'has_work_entries', 'sign_request_ids', 'sign_request_count', 'default_planning_role_id',
                        'planning_role_ids', 'document_count', 'expense_manager_id', 'has_timesheet',
                        'payslip_count', 'registration_number', 'salary_attachment_count', 'mobile_invoice',
                        'sim_card', 'internet_invoice', 'is_non_resident', 'timesheet_manager_id',
                        'last_validated_timesheet_date', 'subscribed_courses', 'has_subscribed_courses',
                        'courses_completion_text', 'billable_time_target', 'display_name', 'create_uid',
                        'create_date', 'write_uid', 'write_date'
                    ],
            "nomina": [],
            "crm": []
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
                    'fields': [],
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
        modulo='crm')
    
    print(data[0].keys())
    
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
