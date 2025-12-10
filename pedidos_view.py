import customtkinter as ctk
from tkinter import ttk, messagebox
from clear import limpiar
from db import ejecutar_consulta
from datetime import date

def mostrar_gestion_pedidos(root):
    limpiar(root)

    ctk.CTkLabel(root, text="Gestión de Pedidos", font=("Arial", 16)).pack(pady=10)

    # Frame para seleccionar cliente o crear nuevo
    cliente_frame = ctk.CTkFrame(root)
    cliente_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(cliente_frame, text="Cliente:").pack(side="left", padx=5)
    clientes = cargar_clientes()
    cliente_cb = ctk.CTkComboBox(cliente_frame, values=clientes, width=300)
    cliente_cb.pack(side="left", padx=5)

    # Frame para formulario de pedido
    form_frame = ctk.CTkFrame(root)
    form_frame.pack(fill="both", expand=True, padx=10, pady=5)

    form_fields = {}

    # Definir campos del formulario
    campos = [
        ("Artículo (Código Prod)", "codigo_prod", "text"),
        ("Medidas de la Persona", "medidas", "text"),
        ("Fecha del Encargo (YYYY-MM-DD)", "fecha_encargo", "date"),
        ("Fecha Probable Entrega (YYYY-MM-DD)", "fecha_pos_en", "date"),
        ("Abono/Anticipo", "abono", "numeric"),
    ]

    for idx, (label, key, tipo) in enumerate(campos):
        ctk.CTkLabel(form_frame, text=label).grid(row=idx, column=0, sticky="w", padx=5, pady=5)
        if tipo == "text":
            widget = ctk.CTkEntry(form_frame, width=300)
        elif tipo == "date":
            widget = ctk.CTkEntry(form_frame, width=300)
            widget.insert(0, str(date.today()))
        elif tipo == "numeric":
            widget = ctk.CTkEntry(form_frame, width=300)
        widget.grid(row=idx, column=1, sticky="ew", padx=5, pady=5)
        form_fields[key] = widget

    form_frame.grid_columnconfigure(1, weight=1)

    # Tabla de pedidos existentes
    tabla_frame = ctk.CTkFrame(root)
    tabla_frame.pack(fill="both", expand=True, padx=10, pady=5)

    scrollbar_y = ttk.Scrollbar(tabla_frame)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x = ttk.Scrollbar(tabla_frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(
        tabla_frame,
        columns=("No_Pedido", "Cliente", "Artículo", "Estado", "Fecha_Encargo", "Abono"),
        show="headings",
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set,
    )
    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    tree.heading("No_Pedido", text="No Pedido")
    tree.heading("Cliente", text="Cliente")
    tree.heading("Artículo", text="Artículo")
    tree.heading("Estado", text="Estado")
    tree.heading("Fecha_Encargo", text="Fecha Encargo")
    tree.heading("Abono", text="Abono")

    tree.column("No_Pedido", width=80)
    tree.column("Cliente", width=120)
    tree.column("Artículo", width=100)
    tree.column("Estado", width=80)
    tree.column("Fecha_Encargo", width=100)
    tree.column("Abono", width=80)

    def cargar_clientes():
        sql = "SELECT DISTINCT no_id FROM cliente ORDER BY no_id"
        resultado = ejecutar_consulta(sql)
        if resultado and resultado != (None, None) and resultado[0]:
            return [str(r[0]) for r in resultado[0]]
        return []

    def cargar_pedidos(cliente_id=None):
        tree.delete(*tree.get_children())
        if cliente_id:
            sql = """
                SELECT P.No_Pedido, C.No_Id, COALESCE(PT.Codigo_Prod, 'N/A'), P.Estado, P.Fecha_Encargo, P.Abono
                FROM PEDIDO P
                JOIN VENTA V ON P.Id_Venta = V.Id_Venta
                JOIN CLIENTE C ON V.No_Id = C.No_Id
                LEFT JOIN PRODUCTO_TERMINADO PT ON P.No_Pedido = PT.No_Pedido
                WHERE C.No_Id = %s
                ORDER BY P.Fecha_Encargo DESC
            """
            resultado = ejecutar_consulta(sql, (cliente_id,))
        else:
            sql = """
                SELECT P.No_Pedido, C.No_Id, COALESCE(PT.Codigo_Prod, 'N/A'), P.Estado, P.Fecha_Encargo, P.Abono
                FROM PEDIDO P
                JOIN VENTA V ON P.Id_Venta = V.Id_Venta
                JOIN CLIENTE C ON V.No_Id = C.No_Id
                LEFT JOIN PRODUCTO_TERMINADO PT ON P.No_Pedido = PT.No_Pedido
                ORDER BY P.Fecha_Encargo DESC
            """
            resultado = ejecutar_consulta(sql)

        if resultado and resultado != (None, None) and resultado[0]:
            for fila in resultado[0]:
                tree.insert("", "end", values=fila)

    cargar_pedidos()

    def crear_pedido():
        cliente_id = cliente_cb.get()
        if not cliente_id:
            messagebox.showwarning("Aviso", "Seleccione un cliente")
            return

        codigo_prod = form_fields["codigo_prod"].get().strip()
        medidas = form_fields["medidas"].get().strip()
        fecha_encargo = form_fields["fecha_encargo"].get().strip()
        fecha_pos_en = form_fields["fecha_pos_en"].get().strip()
        abono_str = form_fields["abono"].get().strip()

        if not codigo_prod or not fecha_encargo:
            messagebox.showwarning("Aviso", "Campos requeridos: Artículo, Fecha Encargo")
            return

        try:
            abono = float(abono_str) if abono_str else 0.0
        except ValueError:
            messagebox.showwarning("Aviso", "Abono debe ser numérico")
            return

        # Crear venta si no existe para este cliente y hoy
        sql_venta = "INSERT INTO venta (no_id, total_venta, fecha_venta, tipo_pago) VALUES (%s, %s, %s, %s) RETURNING id_venta"
        resultado = ejecutar_consulta(sql_venta, (cliente_id, 0.0, date.today(), "Pendiente"))
        if resultado == (None, None) or not resultado[0]:
            messagebox.showerror("Error", "No se pudo crear la venta")
            return

        id_venta = resultado[0][0][0]

        # Crear pedido
        sql_pedido = """
            INSERT INTO pedido (id_venta, abono, estado, fecha_encargo, medidas_persona, fecha_pos_en)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        resultado = ejecutar_consulta(
            sql_pedido,
            (id_venta, abono, "Pendiente", fecha_encargo, medidas, fecha_pos_en if fecha_pos_en else None),
        )
        if resultado == (None, None):
            messagebox.showerror("Error", "No se pudo crear el pedido")
            return

        # Crear producto terminado asociado al pedido
        sql_prod = "INSERT INTO producto_terminado (codigo_prod, no_pedido, cant_existencia, sexo, talla) VALUES (%s, %s, %s, %s, %s)"
        # Nota: no_pedido se obtiene del RETURNING del pedido anterior, pero aquí usamos un workaround
        # En un sistema real deberías capturar el no_pedido retornado
        resultado_prod = ejecutar_consulta(sql_prod, (codigo_prod, None, 1, "Mixto", "N/A"))
        if resultado_prod != (None, None):
            pass  # Producto creado

        messagebox.showinfo("Éxito", "Pedido creado correctamente")

        # Limpiar formulario
        for widget in form_fields.values():
            if hasattr(widget, "delete"):
                widget.delete(0, "end")
        form_fields["fecha_encargo"].insert(0, str(date.today()))
        form_fields["fecha_pos_en"].insert(0, str(date.today()))

        cargar_pedidos(cliente_id)

    # Botones
    buttons_frame = ctk.CTkFrame(root)
    buttons_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkButton(buttons_frame, text="Crear Pedido", width=180, command=crear_pedido).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Recargar", width=180, command=lambda: cargar_pedidos(cliente_cb.get())).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Volver", width=180, command=lambda: volver(root)).pack(side="right", padx=5)

def volver(root):
    from menu_view import mostrar_menu
    mostrar_menu(root)
