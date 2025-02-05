

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

functions = [
    {
        "name": "consultar_ventas",
        "description": "Consulta órdenes de venta en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en las órdenes de venta."},
                "estado": {"type": "string", "enum": ["borrador", "en_proceso", "confirmado", "cancelado", "todos"], "description": "Estado de las órdenes ('confirmado', 'cancelado', etc.)."},
                "fecha_desde": {"type": "string", "format": "date", "description": "Fecha de inicio para la consulta."},
                "fecha_hasta": {"type": "string", "format": "date", "description": "Fecha de fin para la consulta."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "name", "description": "Campo para ordenar los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
    {
        "name": "consultar_compras",
        "description": "Consulta órdenes de compra en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en las órdenes de compra."},
                "estado": {"type": "string", "enum": ["borrador", "en_proceso", "confirmado", "cancelado", "todos"], "description": "Estado de las órdenes ('borrador', 'en_proceso', etc.)."},
                "fecha_desde": {"type": "string", "format": "date", "description": "Fecha de inicio para la consulta."},
                "fecha_hasta": {"type": "string", "format": "date", "description": "Fecha de fin para la consulta."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "name", "description": "Campo para ordenar los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
    {
        "name": "consultar_contabilidad",
        "description": "Consulta registros contables en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en los registros contables."},
                "estado": {"type": "string", "enum": ["borrador", "finalizado", "cancelado", "todos"], "description": "Estado de los registros contables."},
                "fecha_desde": {"type": "string", "format": "date", "description": "Fecha inicial para la consulta."},
                "fecha_hasta": {"type": "string", "format": "date", "description": "Fecha final para la consulta."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "date", "description": "Campo por el que se ordenarán los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
    {
        "name": "consultar_gastos",
        "description": "Consulta los gastos en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en los registros de gastos."},
                "estado": {"type": "string", "enum": ["pendiente", "pagado", "cancelado", "todos"], "description": "Estado de los gastos."},
                "fecha_desde": {"type": "string", "format": "date", "description": "Fecha inicial para la consulta."},
                "fecha_hasta": {"type": "string", "format": "date", "description": "Fecha final para la consulta."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "date", "description": "Campo por el que se ordenarán los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
    {
        "name": "consultar_facturacion",
        "description": "Consulta facturas y documentos contables en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en las facturas."},
                "estado": {"type": "string", "enum": ["borrador", "pagado", "cancelado", "todos"], "description": "Estado de las facturas."},
                "fecha_desde": {"type": "string", "format": "date", "description": "Fecha inicial para la consulta."},
                "fecha_hasta": {"type": "string", "format": "date", "description": "Fecha final para la consulta."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "date", "description": "Campo por el que se ordenarán los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
    {
        "name": "consultar_contactos",
        "description": "Consulta contactos en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en los contactos."},
                "estado": {"type": "string", "enum": ["activo", "inactivo", "todos"], "description": "Estado de los contactos."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "name", "description": "Campo por el que se ordenarán los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
    {
        "name": "consultar_proyectos",
        "description": "Consulta proyectos en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en los proyectos."},
                "estado": {"type": "string", "enum": ["nuevo", "en_proceso", "finalizado", "todos"], "description": "Estado de los proyectos."},
                "fecha_desde": {"type": "string", "format": "date", "description": "Fecha inicial para la consulta."},
                "fecha_hasta": {"type": "string", "format": "date", "description": "Fecha final para la consulta."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "date", "description": "Campo por el que se ordenarán los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
    {
        "name": "consultar_tareas",
        "description": "Consulta tareas dentro de proyectos en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en las tareas."},
                "estado": {"type": "string", "enum": ["pendiente", "en_proceso", "completado", "todos"], "description": "Estado de las tareas."},
                "fecha_desde": {"type": "string", "format": "date", "description": "Fecha inicial para la consulta."},
                "fecha_hasta": {"type": "string", "format": "date", "description": "Fecha final para la consulta."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "date", "description": "Campo por el que se ordenarán los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
    {
        "name": "consultar_inventario",
        "description": "Consulta movimientos de inventario en Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {"type": "string", "description": "Texto para buscar en los movimientos de inventario."},
                "estado": {"type": "string", "enum": ["entrada", "salida", "todos"], "description": "Tipo de movimiento (entrada, salida, etc.)."},
                "fecha_desde": {"type": "string", "format": "date", "description": "Fecha inicial para la consulta."},
                "fecha_hasta": {"type": "string", "format": "date", "description": "Fecha final para la consulta."},
                "limite": {"type": "integer", "default": 100, "description": "Cantidad máxima de registros a recuperar."},
                "ordenar_por": {"type": "string", "default": "date", "description": "Campo por el que se ordenarán los resultados."},
                "orden": {"type": "string", "default": "asc", "enum": ["asc", "desc"], "description": "Orden de los resultados."}
            },
            "required": []
        }
    },
        {
        "name": "consultar_empleados",
        "description": "Consulta información de empleados en el sistema Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {
                    "type": "string",
                    "description": "Criterio de búsqueda para filtrar empleados. Puede ser un nombre, correo electrónico, departamento, o posición."
                },
                "campos_a_recuperar": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Lista de campos que se desean recuperar, como 'nombre', 'email', 'departamento', 'puesto', 'estado'."
                },
                "estado": {
                    "type": "string",
                    "enum": ["activo", "inactivo", "todos"],
                    "description": "Estado del empleado para filtrar. Puede ser 'activo', 'inactivo' o 'todos'."
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de empleados a devolver en la consulta."
                },
                "ordenar_por": {
                    "type": "string",
                    "enum": ["nombre", "email", "departamento", "puesto", "fecha_contratacion"],
                    "description": "Campo por el cual se ordenarán los resultados. Por defecto se ordena por 'nombre'."
                },
                "orden": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Dirección del orden. Puede ser ascendente ('asc') o descendente ('desc')."
                }
            },
            "required": ["filtro"]
        }
    }, 
]




functions2 = [
    {
        "name": "consultar_empleados_odoo",
        "description": "Consulta información de empleados en el sistema Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {
                    "type": "string",
                    "description": "Criterio de búsqueda para filtrar empleados. Puede ser un nombre, correo electrónico, departamento, o posición."
                },
                "campos_a_recuperar": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Lista de campos que se desean recuperar, como 'nombre', 'email', 'departamento', 'puesto', 'estado'."
                },
                "estado": {
                    "type": "string",
                    "enum": ["activo", "inactivo", "todos"],
                    "description": "Estado del empleado para filtrar. Puede ser 'activo', 'inactivo' o 'todos'."
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de empleados a devolver en la consulta."
                },
                "ordenar_por": {
                    "type": "string",
                    "enum": ["nombre", "email", "departamento", "puesto", "fecha_contratacion"],
                    "description": "Campo por el cual se ordenarán los resultados. Por defecto se ordena por 'nombre'."
                },
                "orden": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Dirección del orden. Puede ser ascendente ('asc') o descendente ('desc')."
                }
            },
            "required": ["filtro"]
        }
    }, 
    {
        "name": "consultar_compras_odoo",
        "description": "Consulta información relacionada con órdenes de compra en el módulo de Purchase de Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {
                    "type": "string",
                    "description": "Criterio de búsqueda para filtrar órdenes de compra. Puede ser un número de orden, proveedor o producto."
                },
                "estado": {
                    "type": "string",
                    "enum": ["borrador", "en_proceso", "confirmado", "cancelado", "todos"],
                    "description": "Estado de las órdenes de compra para filtrar. Puede ser 'borrador', 'en_proceso', 'confirmado', 'cancelado' o 'todos'."
                },
                "campos_a_recuperar": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Lista de campos que se desean recuperar, como 'número de orden', 'proveedor', 'total', 'estado', 'fecha de creación'."
                },
                "fecha_desde": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha inicial para filtrar órdenes de compra (formato YYYY-MM-DD)."
                },
                "fecha_hasta": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha final para filtrar órdenes de compra (formato YYYY-MM-DD)."
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de órdenes de compra a devolver en la consulta."
                },
                "ordenar_por": {
                    "type": "string",
                    "enum": ["número de orden", "proveedor", "total", "fecha_creación", "estado"],
                    "description": "Campo por el cual se ordenarán los resultados. Por defecto se ordena por 'número de orden'."
                },
                "orden": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Dirección del orden. Puede ser ascendente ('asc') o descendente ('desc')."
                }
            },
            "required": ["filtro"]
        }
    },
        {
        "name": "consultar_ventas_odoo",
        "description": "Consulta información relacionada con órdenes de venta en el módulo de Sales de Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {
                    "type": "string",
                    "description": "Criterio de búsqueda para filtrar órdenes de venta. Puede ser un número de orden, cliente o producto."
                },
                "estado": {
                    "type": "string",
                    "enum": ["borrador", "en_proceso", "confirmado", "facturado", "cancelado", "todos"],
                    "description": "Estado de las órdenes de venta para filtrar. Puede ser 'borrador', 'en_proceso', 'confirmado', 'facturado', 'cancelado' o 'todos'."
                },
                "campos_a_recuperar": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Lista de campos que se desean recuperar, como 'número de orden', 'cliente', 'total', 'estado', 'fecha de creación'."
                },
                "fecha_desde": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha inicial para filtrar órdenes de venta (formato YYYY-MM-DD)."
                },
                "fecha_hasta": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha final para filtrar órdenes de venta (formato YYYY-MM-DD)."
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de órdenes de venta a devolver en la consulta."
                },
                "ordenar_por": {
                    "type": "string",
                    "enum": ["número de orden", "cliente", "total", "fecha_creación", "estado"],
                    "description": "Campo por el cual se ordenarán los resultados. Por defecto se ordena por 'número de orden'."
                },
                "orden": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Dirección del orden. Puede ser ascendente ('asc') o descendente ('desc')."
                }
            },
            "required": ["filtro"]
        }
    },

    {
        "name": "consultar_contabilidad_odoo",
        "description": "Consulta información relacionada con el módulo de Contabilidad en Odoo, como facturas, pagos y movimientos contables.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {
                    "type": "string",
                    "description": "Criterio de búsqueda para filtrar registros contables. Puede ser un número de factura, cliente o proveedor."
                },
                "tipo": {
                    "type": "string",
                    "enum": ["factura", "pago", "movimiento"],
                    "description": "Tipo de registro contable que se desea consultar: 'factura', 'pago' o 'movimiento'."
                },
                "estado": {
                    "type": "string",
                    "enum": ["borrador", "publicado", "pagado", "cancelado", "todos"],
                    "description": "Estado del registro contable. Puede ser 'borrador', 'publicado', 'pagado', 'cancelado' o 'todos'."
                },
                "fecha_desde": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha inicial para filtrar registros (formato YYYY-MM-DD)."
                },
                "fecha_hasta": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha final para filtrar registros (formato YYYY-MM-DD)."
                },
                "campos_a_recuperar": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Lista de campos que se desean recuperar, como 'número de factura', 'cliente', 'monto', 'estado', 'fecha'."
                },
                "moneda": {
                    "type": "string",
                    "description": "Moneda en la que se deben filtrar los registros, por ejemplo, 'USD', 'EUR', etc."
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de registros a devolver en la consulta."
                },
                "ordenar_por": {
                    "type": "string",
                    "enum": ["fecha", "número", "cliente", "monto", "estado"],
                    "description": "Campo por el cual se ordenarán los resultados. Por defecto se ordena por 'fecha'."
                },
                "orden": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Dirección del orden. Puede ser ascendente ('asc') o descendente ('desc')."
                }
            },
            "required": ["tipo"]
        }
    },
    {
        "name": "consultar_gastos_odoo",
        "description": "Consulta información relacionada con reportes de gastos en el módulo de Expenses de Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {
                    "type": "string",
                    "description": "Criterio de búsqueda para filtrar reportes de gastos. Puede ser un número de reporte, empleado o categoría."
                },
                "estado": {
                    "type": "string",
                    "enum": ["borrador", "aprobado", "rechazado", "pagado", "todos"],
                    "description": "Estado de los reportes de gastos para filtrar. Puede ser 'borrador', 'aprobado', 'rechazado', 'pagado' o 'todos'."
                },
                "campos_a_recuperar": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Lista de campos que se desean recuperar, como 'número de reporte', 'empleado', 'total', 'estado', 'fecha de creación'."
                },
                "fecha_desde": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha inicial para filtrar reportes de gastos (formato YYYY-MM-DD)."
                },
                "fecha_hasta": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha final para filtrar reportes de gastos (formato YYYY-MM-DD)."
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de reportes de gastos a devolver en la consulta."
                },
                "ordenar_por": {
                    "type": "string",
                    "enum": ["número de reporte", "empleado", "total", "fecha_creación", "estado"],
                    "description": "Campo por el cual se ordenarán los resultados. Por defecto se ordena por 'número de reporte'."
                },
                "orden": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Dirección del orden. Puede ser ascendente ('asc') o descendente ('desc')."
                }
            },
            "required": ["filtro"]
        }
    },
    {
        "name": "consultar_inventarios_odoo",
        "description": "Consulta información relacionada con productos y movimientos en el módulo de Inventarios de Odoo.",
        "parameters": {
            "type": "object",
            "properties": {
                "filtro": {
                    "type": "string",
                    "description": "Criterio de búsqueda para filtrar productos o movimientos de inventario. Puede ser un nombre de producto, referencia o categoría."
                },
                "estado": {
                    "type": "string",
                    "enum": ["disponible", "reservado", "agotado", "todos"],
                    "description": "Estado de los productos en inventario. Puede ser 'disponible', 'reservado', 'agotado' o 'todos'."
                },
                "campos_a_recuperar": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Lista de campos que se desean recuperar, como 'nombre del producto', 'cantidad disponible', 'ubicación', 'costo', 'categoría'."
                },
                "almacen": {
                    "type": "string",
                    "description": "Nombre del almacén en el que se desea filtrar los productos o movimientos de inventario."
                },
                "fecha_desde": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha inicial para filtrar movimientos de inventario (formato YYYY-MM-DD)."
                },
                "fecha_hasta": {
                    "type": "string",
                    "format": "date",
                    "description": "Fecha final para filtrar movimientos de inventario (formato YYYY-MM-DD)."
                },
                "limite": {
                    "type": "integer",
                    "description": "Número máximo de productos o movimientos de inventario a devolver en la consulta."
                },
                "ordenar_por": {
                    "type": "string",
                    "enum": ["nombre", "cantidad", "ubicación", "fecha", "costo"],
                    "description": "Campo por el cual se ordenarán los resultados. Por defecto se ordena por 'nombre'."
                },
                "orden": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Dirección del orden. Puede ser ascendente ('asc') o descendente ('desc')."
                }
            },
            "required": ["filtro"]
        }
    }


]