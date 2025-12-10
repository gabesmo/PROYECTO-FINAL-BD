import customtkinter as ctk
from tkinter import ttk, messagebox
from clear import limpiar
from db import ejecutar_consulta
from datetime import date

def mostrar_venta(root):
    limpiar(root)

    # Crear TabView para separar las dos funcionalidades
    tabview = ctk.CTkTabview(root, width=680, height=550)
    tabview.pack(pady=10, padx=10, fill="both", expand=True)

    tab_pedidos = tabview.add("📦 Entregar Encargos")
    tab_directa = tabview.add("💰 Venta Directa")

    # =========================================================================
    # PESTAÑA 1: ENTREGAR ENCARGOS (Tu lógica original mejorada)
    # =========================================================================
    ctk.CTkLabel(tab_pedidos, text="Pedidos Pendientes de Entrega", font=("Arial", 16, "bold")).pack(pady=5)

    frame_pedidos = ctk.CTkFrame(tab_pedidos)
    frame_pedidos.pack(fill="both", expand=True, padx=5, pady=5)

    # Scrollbars para la tabla
    scrollbar_y = ttk.Scrollbar(frame_pedidos)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x = ttk.Scrollbar(frame_pedidos, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(
        frame_pedidos,
        columns=("No_Pedido", "No_Id", "Nombre_Cliente", "Artículo", "Estado", "Abono", "Fecha_Encargo"),
        show="headings",
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set,
    )
    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    # Configuración de columnas
    columnas = [
        ("No_Pedido", 80), ("No_Id", 100), ("Nombre_Cliente", 150),
        ("Artículo", 100), ("Estado", 100), ("Abono", 100), ("Fecha_Encargo", 100)
    ]
    for col, ancho in columnas:
        tree.heading(col, text=col.replace("_", " "))
        tree.column(col, width=ancho)

    selected_pedido = {"id": None}

    def cargar_pedidos():
        tree.delete(*tree.get_children())
        sql = """
            SELECT P.No_Pedido, C.No_Id, C.Nombre, COALESCE(PT.Codigo_Prod, 'N/A'), 
                   P.Estado, P.Abono, P.Fecha_Encargo
            FROM PEDIDO P
            JOIN VENTA V ON P.Id_Venta = V.Id_Venta
            JOIN CLIENTE C ON V.No_Id = C.No_Id
            LEFT JOIN PRODUCTO_TERMINADO PT ON P.No_Pedido = PT.No_Pedido
            WHERE P.Estado <> 'Entregado'
            ORDER BY P.Fecha_Encargo ASC
        """
        resultado = ejecutar_consulta(sql)
        if resultado and resultado[0]:
            for fila in resultado[0]:
                tree.insert("", "end", values=fila)

    def on_tree_select(_event):
        selection = tree.selection()
        if selection:
            selected_pedido["id"] = tree.item(selection[0])["values"][0]

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def procesar_entrega():
        if not selected_pedido["id"]:
            messagebox.showwarning("Aviso", "Seleccione un pedido para entregar")
            return
        
        no_pedido = selected_pedido["id"]
        # Buscar datos para finalizar venta
        sql = """
            SELECT P.Id_Venta, PT.Precio_Venta, PT.Codigo_Prod, P.Abono
            FROM PEDIDO P
            LEFT JOIN PRODUCTO_TERMINADO PT ON P.No_Pedido = PT.No_Pedido
            WHERE P.No_Pedido = %s
        """
        res = ejecutar_consulta(sql, (no_pedido,))
        if not res or not res[0]:
            messagebox.showerror("Error", "No se encontraron datos del pedido")
            return
            
        id_venta, precio, cod_prod, abono = res[0][0]
        
        if not precio: 
            precio = 0.0

        saldo_pendiente = float(precio) - float(abono)

        if messagebox.askyesno("Confirmar Entrega", f"Total: ${precio}\nAbonado: ${abono}\n\nSaldo a Pagar: ${saldo_pendiente}\n¿Confirmar entrega y pago?"):
            # Actualizar Venta
            ejecutar_consulta("UPDATE venta SET total_venta = %s, fecha_venta = %s, tipo_pago = 'Efectivo' WHERE id_venta = %s", 
                            (precio, date.today(), id_venta))
            # Actualizar Pedido
            ejecutar_consulta("UPDATE pedido SET estado = 'Entregado' WHERE no_pedido = %s", (no_pedido,))
            # Descontar Stock
            ejecutar_consulta("UPDATE producto_terminado SET cant_existencia = cant_existencia - 1 WHERE codigo_prod = %s", (cod_prod,))
            
            messagebox.showinfo("Éxito", "Pedido entregado y venta registrada.")
            cargar_pedidos()
            cargar_productos_stock() # Actualizar también la otra pestaña

    btn_frame_1 = ctk.CTkFrame(tab_pedidos)
    btn_frame_1.pack(fill="x", pady=10)
    ctk.CTkButton(btn_frame_1, text="Procesar Entrega", command=procesar_entrega).pack(side="left", padx=10, expand=True)
    ctk.CTkButton(btn_frame_1, text="Actualizar Lista", command=cargar_pedidos).pack(side="left", padx=10, expand=True)

    cargar_pedidos()

    # =========================================================================
    # PESTAÑA 2: VENTA DIRECTA (Nueva funcionalidad)
    # =========================================================================
    ctk.CTkLabel(tab_directa, text="Nueva Venta de Stock", font=("Arial", 16, "bold")).pack(pady=5)
    
    # --- Selección de Cliente ---
    frame_cliente = ctk.CTkFrame(tab_directa)
    frame_cliente.pack(fill="x", padx=10, pady=5)
    
    ctk.CTkLabel(frame_cliente, text="Cliente:").pack(side="left", padx=5)
    
    def get_clientes():
        res = ejecutar_consulta("SELECT no_id, nombre FROM cliente")
        return [f"{r[0]} - {r[1]}" for r in res[0]] if res and res[0] else []

    cb_clientes = ctk.CTkComboBox(frame_cliente, values=get_clientes(), width=300)
    cb_clientes.pack(side="left", padx=5)

    # --- Selección de Producto ---
    frame_prod = ctk.CTkFrame(tab_directa)
    frame_prod.pack(fill="both", expand=True, padx=10, pady=5)
    
    ctk.CTkLabel(frame_prod, text="Seleccione Producto del Inventario:", anchor="w").pack(fill="x", padx=5)

    # Tabla de productos para seleccionar
    tree_stock = ttk.Treeview(frame_prod, columns=("Codigo", "Descripcion", "Talla", "Precio", "Stock"), show="headings", height=8)
    tree_stock.pack(fill="both", expand=True, pady=5)
    
    for col in ["Codigo", "Descripcion", "Talla", "Precio", "Stock"]:
        tree_stock.heading(col, text=col)
        tree_stock.column(col, width=100)

    selected_stock = {"codigo": None, "precio": 0}

    def cargar_productos_stock():
        tree_stock.delete(*tree_stock.get_children())
        # Solo mostrar productos con stock > 0
        sql = "SELECT codigo_prod, descripcion, talla, precio_venta, cant_existencia FROM producto_terminado WHERE cant_existencia > 0"
        res = ejecutar_consulta(sql)
        if res and res[0]:
            for row in res[0]:
                tree_stock.insert("", "end", values=row)

    def on_stock_select(_event):
        sel = tree_stock.selection()
        if sel:
            vals = tree_stock.item(sel[0])["values"]
            selected_stock["codigo"] = vals[0]
            selected_stock["precio"] = vals[3]
            lbl_resumen.configure(text=f"Producto: {vals[1]} | Precio: ${vals[3]}")

    tree_stock.bind("<<TreeviewSelect>>", on_stock_select)

    # --- Botones y Resumen ---
    frame_resumen = ctk.CTkFrame(tab_directa)
    frame_resumen.pack(fill="x", padx=10, pady=10)

    lbl_resumen = ctk.CTkLabel(frame_resumen, text="Seleccione un producto...", font=("Arial", 14))
    lbl_resumen.pack(pady=5)

    def registrar_venta_directa():
        cliente_val = cb_clientes.get()
        if not cliente_val:
            messagebox.showwarning("Error", "Seleccione un cliente")
            return
        if not selected_stock["codigo"]:
            messagebox.showwarning("Error", "Seleccione un producto de la tabla")
            return

        no_id = cliente_val.split(" - ")[0]
        codigo = selected_stock["codigo"]
        precio = float(selected_stock["precio"])

        if messagebox.askyesno("Confirmar", f"¿Registrar venta por ${precio}?"):
            # 1. Insertar Venta
            sql_venta = "INSERT INTO venta (no_id, total_venta, fecha_venta, tipo_pago) VALUES (%s, %s, %s, %s) RETURNING id_venta"
            res = ejecutar_consulta(sql_venta, (no_id, precio, date.today(), "Efectivo"))
            
            if res and res[0]:
                # 2. Descontar Inventario
                sql_upd = "UPDATE producto_terminado SET cant_existencia = cant_existencia - 1 WHERE codigo_prod = %s"
                ejecutar_consulta(sql_upd, (codigo,))
                
                messagebox.showinfo("Éxito", "Venta registrada correctamente")
                cargar_productos_stock()
                lbl_resumen.configure(text="Seleccione un producto...")
                selected_stock["codigo"] = None
            else:
                messagebox.showerror("Error", "No se pudo registrar la venta")

    ctk.CTkButton(frame_resumen, text="💰 Registrar Venta Directa", command=registrar_venta_directa, fg_color="#2CC985", hover_color="#26A86F").pack(pady=10)
    
    cargar_productos_stock()

    # Botón Volver General
    ctk.CTkButton(root, text="Volver al Menú", command=lambda: volver(root)).pack(pady=5)

def volver(root):
    from menu_view import mostrar_menu
    mostrar_menu(root)