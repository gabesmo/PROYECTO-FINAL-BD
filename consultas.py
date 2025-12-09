consultas_predef = {
    "COLEGIO": {
        "Todos los colegios": "SELECT * FROM colegio;",
    },

    "CLIENTE": {
        "Todos los clientes": "SELECT * FROM cliente;",
        "Productos sin entregar": """ SELECT C.No_Id, C.Nombre, P.No_Pedido, PT.Codigo_Prod, P.Estado
                                                    FROM CLIENTE C
                                                    JOIN VENTA V ON C.No_Id = V.No_Id
                                                    JOIN PEDIDO P ON V.Id_Venta = P.Id_Venta
                                                    JOIN PRODUCTO_TERMINADO PT ON P.No_Pedido = PT.No_Pedido
                                                    WHERE P.Estado != 'Finalizado';
                                  """,
    },

    "TEL_CLIENTE": {
        "Todos los teléfonos de clientes": "SELECT * FROM tel_cliente;",
    },

    "VENTA": {
        "Todas las ventas": "SELECT * FROM venta;",
        "Total ingresos de ventas": """ SELECT SUM(Total_Venta) AS Total_Ventas
                                        FROM VENTA;
                                    """,
    },

    "PEDIDO": {
        "Todos los pedidos": "SELECT * FROM pedido;",
    },

    "PRODUCTO_TERMINADO": {
        "Todos los productos terminados": "SELECT * FROM producto_terminado;",
        "Productos pendiendes de entrega (ordenado por fecha)": """ SELECT No_Pedido, Estado, Fecha_Encargo
                                                                    FROM PEDIDO
                                                                    WHERE Estado != 'Finalizado'
                                                                    ORDER BY Fecha_Encargo;
                                                                """,
        "Existencia real (descuenta encargados)":   """ SELECT Codigo_Prod,
                                                        Cant_Existencia - COUNT(P.No_Pedido) AS Existencia_Real
                                                        FROM PRODUCTO_TERMINADO PT
                                                        LEFT JOIN PEDIDO P ON PT.No_Pedido = P.No_Pedido AND P.Estado != 'Finalizado'
                                                        GROUP BY Codigo_Prod, Cant_Existencia;
                                                    """,        
        "Total productos vendidos por colegio": """ SELECT C.Nombre, COUNT(PT.Codigo_Prod) AS Total_Productos
                                                    FROM COLEGIO C
                                                    JOIN UNIFORME U ON C.Nit_Colegio = U.Nit_Colegio
                                                    JOIN PRODUCTO_TERMINADO PT ON U.Codigo_Prod = PT.Codigo_Prod
                                                    GROUP BY C.Nombre;
                                                """,                                                  
    },

    "PRENDA_GENERAL": {
        "Todas las prendas generales": "SELECT * FROM prenda_general;",
    },

    "PROVEEDOR": {
        "Todos los proveedores": "SELECT * FROM proveedor;",
    },

    "MATERIA_PRIMA": {
        "Todas las materias primas": "SELECT * FROM materia_prima;",
    },

    "SUMINISTRA": {
        "Todos los suministros": "SELECT * FROM suministra;",
    },

    "UTILIZA": {
        "Todos los usos de materia prima": "SELECT * FROM utiliza;",
    },

    "UNIFORME": {
        "Todos los uniformes": "SELECT * FROM uniforme;",
        "Listado colegios para los que se fabrica": """ SELECT DISTINCT C.Nit_Colegio, C.Nombre
                                                        FROM COLEGIO C
                                                        JOIN UNIFORME U ON C.Nit_Colegio = U.Nit_Colegio;
                                                    """,
        "Características uniforme por colegio": """ SELECT
                                                        C.NIT_COLEGIO,
                                                        C.NOMBRE,
                                                        U.BORDES_COLOR,
                                                        U.TIPO_BORD,
                                                        U.TIPO_TELA,
                                                        U.LUGAR_BORD,
                                                        U.COLOR
                                                    FROM
                                                        COLEGIO C
                                                        JOIN UNIFORME U ON C.NIT_COLEGIO = U.NIT_COLEGIO
                                                """,
    },

    "USUARIO": {
        "Todos los usuarios": "SELECT * FROM usuario;",
    },
}