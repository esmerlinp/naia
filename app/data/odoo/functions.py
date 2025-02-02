functions = [
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
    }
]