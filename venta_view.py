import customtkinter as ctk
from tkinter import ttk, messagebox
from clear import limpiar
from db import ejecutar_consulta
from datetime import date

def mostrar_venta(root):
    limpiar(root)

    ctk.CTkLabel(root, text="Procesar Venta / Entrega de Producto", font=("Arial", 16)).pack(pady=10)

    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar_y = ttk.Scrollbar(frame)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(
        frame,
        columns=("No_Pedido", "No_Id", "Nombre_Cliente", "Artículo", "Estado", "Abono", "Fecha_Encargo"),
        show="headings",
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set,
    )
    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    tree.heading("No_Pedido", text="No Pedido")
    tree.heading("No_Id", text="No Id")
    tree.heading("Nombre_Cliente", text="Cliente")
    tree.heading("Artículo", text="Artículo")
    tree.heading("Estado", text="Estado")
    tree.heading("Abono", text="Abono")
    tree.heading("Fecha_Encargo", text="Fecha Encargo")

    tree.column("No_Pedido", width=80)
    tree.column("No_Id", width=100)
    tree.column("Nombre_Cliente", width=150)
    tree.column("Artículo", width=100)
    tree.column("Estado", width=100)
    tree.column("Abono", width=100)
    tree.column("Fecha_Encargo", width=100)

    info_frame = ctk.CTkFrame(root)
    info_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(info_frame, text="Detalles del Pedido", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

    info_labels = {}
    fields = [
        ("No Pedido", "no_pedido"),
        ("Cliente", "cliente"),
        ("Artículo", "articulo"),
        ("Estado", "estado"),
        ("Abono", "abono"),
        ("Fecha Encargo", "fecha_encargo"),
    ]
    for idx, (label, key) in enumerate(fields, 1):
        ctk.CTkLabel(info_frame, text=f"{label}:").grid(row=idx, column=0, sticky="w", padx=5, pady=2)
        info_labels[key] = ctk.CTkLabel(info_frame, text="")
        info_labels[key].grid(row=idx, column=1, sticky="w", padx=5, pady=2)

    buttons_frame = ctk.CTkFrame(root)
    buttons_frame.pack(fill="x", padx=10, pady=10)

    selected_pedido = {"id": None}

    def cargar_pedidos():
        tree.delete(*tree.get_children())
        sql = """
            SELECT 
                P.No_Pedido,
                C.No_Id,
                C.Nombre,
                COALESCE(PT.Codigo_Prod, 'N/A') AS Articulo,
                P.Estado,
                P.Abono,
                P.Fecha_Encargo
            FROM PEDIDO P
            JOIN VENTA V ON P.Id_Venta = V.Id_Venta
            JOIN CLIENTE C ON V.No_Id = C.No_Id
            LEFT JOIN PRODUCTO_TERMINADO PT ON P.No_Pedido = PT.No_Pedido
            WHERE P.Estado <> 'Entregado'
            ORDER BY P.Fecha_Encargo DESC
        """
        resultado = ejecutar_consulta(sql)
        if resultado and resultado != (None, None):
            filas = resultado[0]
            if filas:
                for fila in filas:
                    tree.insert("", "end", values=fila)

    cargar_pedidos()

    def on_tree_select(_event):
        selection = tree.selection()
        if not selection:
            return
        valores = tree.item(selection[0])["values"]
        no_pedido = valores[0]
        selected_pedido["id"] = no_pedido

        for key, label in info_labels.items():
            label.configure(text="")

        sql = """
            SELECT 
                P.No_Pedido,
                C.Nombre,
                COALESCE(PT.Codigo_Prod, 'N/A'),
                P.Estado,
                P.Abono,
                P.Fecha_Encargo
            FROM PEDIDO P
            JOIN VENTA V ON P.Id_Venta = V.Id_Venta
            JOIN CLIENTE C ON V.No_Id = C.No_Id
            LEFT JOIN PRODUCTO_TERMINADO PT ON P.No_Pedido = PT.No_Pedido
            WHERE P.No_Pedido = %s
        """
        resultado = ejecutar_consulta(sql, (no_pedido,))
        if resultado and resultado != (None, None) and resultado[0]:
            fila = resultado[0][0]
            info_labels["no_pedido"].configure(text=str(fila[0]))
            info_labels["cliente"].configure(text=str(fila[1]))
            info_labels["articulo"].configure(text=str(fila[2]))
            info_labels["estado"].configure(text=str(fila[3]))
            info_labels["abono"].configure(text=str(fila[4]))
            info_labels["fecha_encargo"].configure(text=str(fila[5]))

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def procesar_venta():
        if not selected_pedido["id"]:
            messagebox.showwarning("Aviso", "Seleccione un pedido")
            return

        no_pedido = selected_pedido["id"]

        # Obtener datos del pedido
        sql = """
            SELECT P.Id_Venta, V.No_Id, P.Abono, PT.Codigo_Prod, PT.Precio_Venta, PT.Cant_Existencia
            FROM PEDIDO P
            JOIN VENTA V ON P.Id_Venta = V.Id_Venta
            LEFT JOIN PRODUCTO_TERMINADO PT ON P.No_Pedido = PT.No_Pedido
            WHERE P.No_Pedido = %s
        """
        resultado = ejecutar_consulta(sql, (no_pedido,))
        if not resultado or resultado == (None, None) or not resultado[0]:
            messagebox.showerror("Error", "No se encontraron datos del pedido")
            return

        fila = resultado[0][0]
        id_venta, no_id, abono, codigo_prod, precio_venta, cant_existencia = fila

        if not codigo_prod or not precio_venta:
            messagebox.showerror("Error", "El pedido no tiene producto o precio definido")
            return

        # Generar factura (actualizar VENTA con total, actualizar PEDIDO a "Entregado", descontar stock)
        total_venta = float(precio_venta)

        # 1. Actualizar VENTA
        sql_venta = "UPDATE venta SET total_venta = %s, fecha_venta = %s WHERE id_venta = %s"
        resultado = ejecutar_consulta(sql_venta, (total_venta, date.today(), id_venta))
        if resultado == (None, None):
            messagebox.showerror("Error", "No se pudo actualizar la venta")
            return

        # 2. Actualizar PEDIDO estado a "Entregado"
        sql_pedido = "UPDATE pedido SET estado = %s WHERE no_pedido = %s"
        resultado = ejecutar_consulta(sql_pedido, ("Entregado", no_pedido))
        if resultado == (None, None):
            messagebox.showerror("Error", "No se pudo actualizar el pedido")
            return

        # 3. Descontar stock
        nueva_cantidad = int(cant_existencia) - 1
        sql_stock = "UPDATE producto_terminado SET cant_existencia = %s WHERE codigo_prod = %s"
        resultado = ejecutar_consulta(sql_stock, (nueva_cantidad, codigo_prod))
        if resultado == (None, None):
            messagebox.showerror("Error", "No se pudo actualizar el inventario")
            return

        # Mostrar factura
        factura_text = f"""
        ╔════════════════════════════════════╗
        ║         FACTURA DE VENTA           ║
        ╚════════════════════════════════════╝
        
        No Venta:     {id_venta}
        No Pedido:    {no_pedido}
        Cliente:      {no_id}
        Fecha:        {date.today()}
        
        Producto:     {codigo_prod}
        Precio:       ${precio_venta}
        Abono:        ${abono}
        ─────────────────────────────────────
        TOTAL VENTA:  ${total_venta}
        
        Estado:       ENTREGADO
        
        ════════════════════════════════════
        """
        messagebox.showinfo("Factura Generada", factura_text)

        # Recargar listado
        cargar_pedidos()
        for key, label in info_labels.items():
            label.configure(text="")
        selected_pedido["id"] = None

    ctk.CTkButton(buttons_frame, text="Procesar Venta", width=180, command=procesar_venta).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Recargar", width=180, command=cargar_pedidos).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Volver", width=180, command=lambda: volver(root)).pack(side="right", padx=5)

def volver(root):
    from menu_view import mostrar_menu
    mostrar_menu(root)
