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
                                                    WHERE P.Estado <> 'Entregado';
                                  """,
    },

    "TEL_CLIENTE": {
        "Todos los teléfonos de clientes": "SELECT * FROM tel_cliente;",
        "Clientes con múltiples teléfonos": """ SELECT No_Id, COUNT(Telefono) AS Cantidad_Telefonos
                                                FROM TEL_CLIENTE
                                                GROUP BY No_Id
                                                HAVING COUNT(Telefono) > 1;
                                            """,
        "Clientes sin teléfono registrado": """ SELECT C.No_Id, C.Nombre
                                                FROM CLIENTE C
                                                LEFT JOIN TEL_CLIENTE TC ON C.No_Id = TC.No_Id
                                                WHERE TC.No_Id IS NULL;
                                            """,
    },

    "VENTA": {
        "Todas las ventas": "SELECT * FROM venta;",
        "Total ingresos de ventas": """ SELECT SUM(Total_Venta) AS Total_Ventas
                                        FROM VENTA;
                                    """,
        "Ventas por cliente": """ SELECT C.No_Id, C.Nombre, COUNT(V.Id_Venta) AS Cantidad_Ventas, SUM(V.Total_Venta) AS Total_Gastado
                                    FROM CLIENTE C
                                    JOIN VENTA V ON C.No_Id = V.No_Id
                                    GROUP BY C.No_Id, C.Nombre;
                                """,
        "Ventas por fecha": """ SELECT Fecha_Venta, COUNT(Id_Venta) AS Cantidad_Ventas, SUM(Total_Venta) AS Total_Ventas
                                FROM VENTA
                                GROUP BY Fecha_Venta;
                            """,
        "Ventas sin pedidos asociados": """ SELECT V.Id_Venta, V.Fecha_Venta, V.Total_Venta
                                            FROM VENTA V
                                            LEFT JOIN PEDIDO P ON V.Id_Venta = P.Id_Venta
                                            WHERE P.Id_Venta IS NULL;
                                        """,

    },

    "PEDIDO": {
        "Todos los pedidos": "SELECT * FROM pedido;",
        "Pedidos por estado": """ SELECT Estado, COUNT(*) AS Cantidad
                                    FROM PEDIDO
                                    GROUP BY Estado;
                                """,
        "Pedidos por cliente": """ SELECT C.No_Id, C.Nombre, COUNT(P.No_Pedido) AS Cantidad_Pedidos
                                    FROM CLIENTE C
                                    JOIN VENTA V ON C.No_Id = V.No_Id
                                    JOIN PEDIDO P ON V.Id_Venta = P.Id_Venta
                                    GROUP BY C.No_Id, C.Nombre;
                                """,
        
        
    },

    "PRODUCTO_TERMINADO": {
        "Todos los productos terminados": "SELECT * FROM producto_terminado;",
        "Productos pendiendes de entrega (ordenado por fecha)": """ SELECT
                                                                        P.NO_PEDIDO,
                                                                        PT.CODIGO_PROD,
                                                                        P.ESTADO,
                                                                        P.FECHA_ENCARGO
                                                                    FROM
                                                                        PEDIDO P
                                                                        JOIN PRODUCTO_TERMINADO PT ON P.NO_PEDIDO = PT.NO_PEDIDO
                                                                    WHERE
                                                                        P.ESTADO <> 'Entregado'
                                                                    ORDER BY
                                                                        P.FECHA_ENCARGO;
                                                                """,
        "Existencia real (descuenta encargados)":   """ SELECT PT.Codigo_Prod,
                                                        PT.Cant_Existencia - COUNT(P.No_Pedido) AS Existencia_Real
                                                        FROM PRODUCTO_TERMINADO PT
                                                        LEFT JOIN PEDIDO P ON PT.No_Pedido = P.No_Pedido AND P.Estado <> 'Entregado'
                                                        GROUP BY PT.Codigo_Prod, PT.Cant_Existencia;
                                                    """,        
        "Total productos vendidos por colegio": """ SELECT
                                                        C.NOMBRE,
                                                        COUNT(PT.CODIGO_PROD) AS TOTAL_PRODUCTOS
                                                    FROM
                                                        COLEGIO C
                                                        JOIN UNIFORME U ON C.NIT_COLEGIO = U.NIT_COLEGIO
                                                        JOIN PRODUCTO_TERMINADO PT ON U.CODIGO_PROD = PT.CODIGO_PROD
                                                        JOIN PEDIDO P ON PT.NO_PEDIDO = P.NO_PEDIDO
                                                        JOIN VENTA V ON P.ID_VENTA = V.ID_VENTA
                                                    GROUP BY
                                                        C.NOMBRE;
                                                """,   
        "Cantidad de productos por talla": """SELECT Talla, COUNT(*) AS Total_Productos
                                                FROM PRODUCTO_TERMINADO
                                                GROUP BY Talla;
                                            """,

    },

    "PRENDA_GENERAL": {
        "Todas las prendas generales": "SELECT * FROM prenda_general;",
        "Prendas generales por tipo": """ SELECT Tipo_Prenda, COUNT(*) AS Cantidad
                                        FROM PRENDA_GENERAL
                                        GROUP BY Tipo_Prenda;
                                    """,
    },

    "PROVEEDOR": {
        "Todos los proveedores": "SELECT * FROM proveedor;",
        "Proveedores y sus materias primas": """ SELECT 
                                                    P.Nit_Prov,
                                                    P.Nombre,
                                                    MP.Codigo_MatP,
                                                    MP.Tipo,
                                                    MP.Descripcion,
                                                    MP.Unidad_Med,
                                                    MP.Cantidad
                                                FROM 
                                                    PROVEEDOR P
                                                    JOIN SUMINISTRA S ON P.Nit_Prov = S.Nit_Prov
                                                    JOIN MATERIA_PRIMA MP ON S.Codigo_MatP = MP.Codigo_MatP;
                                            """
                                            
    },

    "MATERIA_PRIMA": {
        "Todas las materias primas": "SELECT * FROM materia_prima;",
        "Materias primas por proveedor": """ SELECT
                                                MP.Codigo_MatP,
                                                MP.Tipo,
                                                MP.Descripcion,
                                                MP.Unidad_Med,
                                                MP.Cantidad,
                                                P.Nit_Prov,
                                                P.Nombre AS Nombre_Proveedor
                                            FROM
                                                MATERIA_PRIMA MP
                                                JOIN SUMINISTRA S ON MP.Codigo_MatP = S.Codigo_MatP
                                                JOIN PROVEEDOR P ON S.Nit_Prov = P.Nit_Prov;
                                            """,
    },

    "SUMINISTRA": {
        "Todos los suministros": "SELECT * FROM suministra;",
    },

    "UTILIZA": {
        "Todos los usos de materia prima": "SELECT * FROM utiliza;",
        "Materia prima utilizada por uniforme": """ SELECT
                                                        U.Codigo_Prod,
                                                        MP.Codigo_MatP,
                                                        MP.Tipo,
                                                        MP.Descripcion,
                                                        MP.Unidad_Med,
                                                        MP.Cantidad AS Cantidad_Disponible
                                                    FROM
                                                        UTILIZA UTI
                                                        JOIN MATERIA_PRIMA MP ON UTI.Codigo_MatP = MP.Codigo_MatP
                                                        JOIN PRODUCTO_TERMINADO PT ON UTI.Codigo_Prod = PT.Codigo_Prod
                                                        JOIN UNIFORME U ON PT.Codigo_Prod = U.Codigo_Prod;
                                                """,
        
    },

    "UNIFORME": {
        "Todos los uniformes": "SELECT * FROM uniforme;",
        "Listado colegios para los que se fabrica": """ SELECT DISTINCT U.Nit_Colegio, C.Nombre
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
        "Cantidad de uniformes por colegio": """ SELECT
                                                    C.NOMBRE,
                                                    COUNT(U.Codigo_Prod) AS Cantidad_Uniformes
                                                FROM
                                                    COLEGIO C
                                                    JOIN UNIFORME U ON C.NIT_COLEGIO = U.NIT_COLEGIO
                                                GROUP BY
                                                    C.NOMBRE;
                                            """,
    },

    "USUARIO": {
        "Todos los usuarios": "SELECT * FROM usuario;",
        "Usuarios por rol": """ SELECT Rol, COUNT(*) AS Cantidad
                                FROM USUARIO
                                GROUP BY Rol;
                            """,
    },
}