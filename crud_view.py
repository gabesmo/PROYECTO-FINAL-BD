import customtkinter as ctk
from tkinter import ttk, messagebox
from clear import limpiar
from db import ejecutar_consulta
from session import is_admin

# Definición de esquemas para construir formularios y sentencias dinámicamente
TABLE_SCHEMAS = {
    "colegio": {
        "label": "Colegios",
        "order_by": ["nit_colegio"],
        "columns": [
            {"name": "nit_colegio", "label": "Nit Colegio", "type": "text", "pk": True, "required": True},
            {"name": "direccion", "label": "Direccion", "type": "text"},
            {"name": "nombre", "label": "Nombre", "type": "text"},
        ],
    },
    "cliente": {
        "label": "Clientes",
        "order_by": ["no_id"],
        "columns": [
            {"name": "no_id", "label": "No Id", "type": "text", "pk": True, "required": True},
            {"name": "nombre", "label": "Nombre", "type": "text"},
        ],
    },
    "tel_cliente": {
        "label": "Telefonos de Cliente",
        "order_by": ["no_id", "telefono"],
        "columns": [
            {"name": "no_id", "label": "No Id", "type": "text", "pk": True, "required": True},
            {"name": "telefono", "label": "Telefono", "type": "text", "pk": True, "required": True},
        ],
    },
    "venta": {
        "label": "Ventas",
        "order_by": ["id_venta"],
        "columns": [
            {"name": "id_venta", "label": "Id Venta", "type": "serial", "pk": True},
            {"name": "no_id", "label": "No Id (Cliente)", "type": "text"},
            {"name": "total_venta", "label": "Total Venta", "type": "numeric"},
            {"name": "fecha_venta", "label": "Fecha Venta (YYYY-MM-DD)", "type": "date"},
            {"name": "tipo_pago", "label": "Tipo Pago", "type": "text"},
        ],
    },
    "pedido": {
        "label": "Pedidos",
        "order_by": ["no_pedido"],
        "columns": [
            {"name": "no_pedido", "label": "No Pedido", "type": "serial", "pk": True},
            {"name": "id_venta", "label": "Id Venta", "type": "int"},
            {"name": "abono", "label": "Abono", "type": "numeric"},
            {"name": "estado", "label": "Estado", "type": "text"},
            {"name": "fecha_encargo", "label": "Fecha Encargo (YYYY-MM-DD)", "type": "date"},
            {"name": "medidas_persona", "label": "Medidas Persona", "type": "text"},
            {"name": "fecha_pos_en", "label": "Fecha Pos Entrega (YYYY-MM-DD)", "type": "date"},
        ],
    },
    "producto_terminado": {
        "label": "Producto Terminado",
        "order_by": ["codigo_prod"],
        "columns": [
            {"name": "codigo_prod", "label": "Codigo Prod", "type": "text", "pk": True, "required": True},
            {"name": "no_pedido", "label": "No Pedido", "type": "int"},
            {"name": "cant_existencia", "label": "Cant Existencia", "type": "int"},
            {"name": "precio_venta", "label": "Precio Venta", "type": "numeric"},
            {"name": "sexo", "label": "Sexo", "type": "text"},
            {"name": "talla", "label": "Talla", "type": "text"},
            {"name": "descripcion", "label": "Descripcion", "type": "text"},
        ],
    },
    "prenda_general": {
        "label": "Prenda General",
        "order_by": ["codigo_prod"],
        "columns": [
            {"name": "codigo_prod", "label": "Codigo Prod", "type": "text", "pk": True, "required": True},
            {"name": "tipo_prenda", "label": "Tipo Prenda", "type": "text"},
        ],
    },
    "proveedor": {
        "label": "Proveedor",
        "order_by": ["nit_prov"],
        "columns": [
            {"name": "nit_prov", "label": "Nit Prov", "type": "text", "pk": True, "required": True},
            {"name": "nombre", "label": "Nombre", "type": "text"},
            {"name": "telefono", "label": "Telefono", "type": "text"},
            {"name": "nombre_cont", "label": "Nombre Contacto", "type": "text"},
            {"name": "direccion", "label": "Direccion", "type": "text"},
        ],
    },
    "materia_prima": {
        "label": "Materia Prima",
        "order_by": ["codigo_matp"],
        "columns": [
            {"name": "codigo_matp", "label": "Codigo MatP", "type": "text", "pk": True, "required": True},
            {"name": "cantidad", "label": "Cantidad", "type": "int"},
            {"name": "tipo", "label": "Tipo", "type": "text"},
            {"name": "descripcion", "label": "Descripcion", "type": "text"},
            {"name": "unidad_med", "label": "Unidad Med", "type": "text"},
        ],
    },
    "suministra": {
        "label": "Suministra",
        "order_by": ["nit_prov", "codigo_matp"],
        "columns": [
            {"name": "nit_prov", "label": "Nit Prov", "type": "text", "pk": True, "required": True},
            {"name": "codigo_matp", "label": "Codigo MatP", "type": "text", "pk": True, "required": True},
        ],
    },
    "utiliza": {
        "label": "Utiliza",
        "order_by": ["codigo_matp", "codigo_prod"],
        "columns": [
            {"name": "codigo_matp", "label": "Codigo MatP", "type": "text", "pk": True, "required": True},
            {"name": "codigo_prod", "label": "Codigo Prod", "type": "text", "pk": True, "required": True},
        ],
    },
    "uniforme": {
        "label": "Uniforme",
        "order_by": ["codigo_prod"],
        "columns": [
            {"name": "codigo_prod", "label": "Codigo Prod", "type": "text", "pk": True, "required": True},
            {"name": "nit_colegio", "label": "Nit Colegio", "type": "text"},
            {"name": "bordes_color", "label": "Bordes Color", "type": "text"},
            {"name": "tipo_bord", "label": "Tipo Bord", "type": "text"},
            {"name": "tipo_tela", "label": "Tipo Tela", "type": "text"},
            {"name": "lugar_bord", "label": "Lugar Bord", "type": "text"},
            {"name": "color", "label": "Color", "type": "text"},
        ],
    },
    "usuario": {
        "label": "Usuario",
        "order_by": ["id_usuario"],
        "columns": [
            {"name": "id_usuario", "label": "Id Usuario", "type": "serial", "pk": True},
            {"name": "nombre_usuario", "label": "Nombre Usuario", "type": "text", "required": True},
            {"name": "nombre_completo", "label": "Nombre Completo", "type": "text", "required": True},
            {"name": "clave_hash", "label": "Clave Hash", "type": "text", "required": True},
            {"name": "rol", "label": "Rol (ADMIN/VENDEDOR)", "type": "text", "required": True},
            {"name": "estado", "label": "Estado (true/false)", "type": "bool"},
        ],
    },
}


def mostrar_crud_general(root):
    if not is_admin():
        messagebox.showerror("Acceso Denegado", "Solo administradores pueden acceder al CRUD general")
        from menu_view import mostrar_menu
        mostrar_menu(root)
        return

    limpiar(root)

    ctk.CTkLabel(root, text="CRUD Tablas", font=("Arial", 18)).pack(pady=10)

    selector_frame = ctk.CTkFrame(root)
    selector_frame.pack(fill="x", padx=10)
    ctk.CTkLabel(selector_frame, text="Tabla:").pack(side="left", padx=5)

    table_keys = sorted(TABLE_SCHEMAS.keys())
    tabla_cb = ctk.CTkComboBox(selector_frame, values=table_keys, width=200)
    tabla_cb.pack(side="left", padx=5)

    form_frame = ctk.CTkFrame(root)
    form_frame.pack(fill="x", padx=10, pady=10)

    table_frame = ctk.CTkFrame(root)
    table_frame.pack(fill="both", expand=True, padx=10, pady=5)

    scrollbar_y = ttk.Scrollbar(table_frame)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(
        table_frame,
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set,
        show="headings",
    )
    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    buttons_frame = ctk.CTkFrame(root)
    buttons_frame.pack(fill="x", padx=10, pady=10)

    field_widgets = {}
    current_table = {"name": None}

    def get_widget_text(widget):
        if hasattr(widget, "get"):
            return widget.get().strip()
        return ""

    def set_widget_value(widget, value, disabled=False):
        if isinstance(widget, ctk.CTkComboBox):
            widget.set("" if value is None else str(value))
            if disabled:
                widget.configure(state="disabled")
            return

        state = getattr(widget, "cget", lambda x: None)("state") if hasattr(widget, "cget") else None
        if state == "disabled":
            widget.configure(state="normal")
        try:
            if hasattr(widget, "delete"):
                widget.delete(0, "end")
            if value is None:
                value = ""
            if hasattr(widget, "insert"):
                widget.insert(0, str(value))
        finally:
            if disabled:
                widget.configure(state="disabled")

    def parse_value(raw, col_type):
        if raw is None:
            return None
        raw = raw.strip()
        if raw == "":
            return None
        if col_type in ("int", "serial"):
            return int(raw)
        if col_type in ("numeric", "decimal"):
            return float(raw)
        if col_type == "bool":
            return str(raw).lower() in ("true", "1", "t", "yes", "si", "y")
        return raw

    def build_form(table_key):
        for widget in form_frame.winfo_children():
            widget.destroy()
        field_widgets.clear()

        schema = TABLE_SCHEMAS[table_key]
        for idx, col in enumerate(schema["columns"]):
            ctk.CTkLabel(form_frame, text=col["label"]).grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            if col["type"] == "bool":
                widget = ctk.CTkComboBox(form_frame, values=["true", "false"], width=200)
            else:
                widget = ctk.CTkEntry(form_frame, width=250)
                if col["type"] == "serial":
                    widget.insert(0, "AUTO")
                    widget.configure(state="disabled")
            widget.grid(row=idx, column=1, sticky="ew", padx=5, pady=2)
            field_widgets[col["name"]] = widget

        form_frame.grid_columnconfigure(1, weight=1)

    def load_data(table_key):
        schema = TABLE_SCHEMAS[table_key]
        col_names = [c["name"] for c in schema["columns"]]
        order = schema.get("order_by") or [c["name"] for c in schema["columns"] if c.get("pk")]
        sql = f"SELECT {', '.join(col_names)} FROM {table_key}"
        if order:
            sql += " ORDER BY " + ", ".join(order)

        resultado = ejecutar_consulta(sql)
        tree.delete(*tree.get_children())

        if not resultado or resultado == (None, None):
            tree["columns"] = col_names
            for col, meta in zip(col_names, schema["columns"]):
                tree.heading(col, text=meta["label"])
                tree.column(col, width=140)
            return

        filas, _columnas = resultado
        tree["columns"] = col_names
        for col, meta in zip(col_names, schema["columns"]):
            tree.heading(col, text=meta["label"])
            tree.column(col, width=140)

        for fila in filas:
            tree.insert("", "end", values=fila)

    def on_select_table(choice):
        current_table["name"] = choice
        build_form(choice)
        load_data(choice)

    tabla_cb.configure(command=on_select_table)
    if table_keys:
        tabla_cb.set(table_keys[0])
        on_select_table(table_keys[0])

    def read_form_data(table_key):
        schema = TABLE_SCHEMAS[table_key]
        data = {}
        for col in schema["columns"]:
            widget = field_widgets[col["name"]]
            raw = get_widget_text(widget)
            data[col["name"]] = parse_value(raw, col["type"])
        return data

    def ensure_pk_present(schema, data):
        for col in schema["columns"]:
            if col.get("pk") and col["type"] != "serial":
                if data.get(col["name"]) is None:
                    return False, f"Falta clave: {col['label']}"
        return True, None

    def insert_record():
        table_key = current_table["name"]
        if not table_key:
            messagebox.showwarning("Aviso", "Seleccione una tabla")
            return
        schema = TABLE_SCHEMAS[table_key]
        data = read_form_data(table_key)

        for col in schema["columns"]:
            if col["type"] == "serial":
                continue
            if col.get("required") and (data.get(col["name"]) is None):
                messagebox.showwarning("Aviso", f"Campo requerido: {col['label']}")
                return

        cols = [c for c in schema["columns"] if c["type"] != "serial"]
        col_names = [c["name"] for c in cols]
        values = [data[name] for name in col_names]

        placeholders = ", ".join(["%s"] * len(values))
        sql = f"INSERT INTO {table_key} ({', '.join(col_names)}) VALUES ({placeholders})"

        resultado = ejecutar_consulta(sql, tuple(values))
        if resultado == (None, None):
            messagebox.showerror("Error", "No se pudo insertar el registro")
            return
        load_data(table_key)
        messagebox.showinfo("Éxito", "Registro insertado")

    def update_record():
        table_key = current_table["name"]
        if not table_key:
            messagebox.showwarning("Aviso", "Seleccione una tabla")
            return
        schema = TABLE_SCHEMAS[table_key]
        data = read_form_data(table_key)

        ok, msg = ensure_pk_present(schema, data)
        if not ok:
            messagebox.showwarning("Aviso", msg)
            return

        set_cols = [c for c in schema["columns"] if not c.get("pk") and c["type"] != "serial"]
        if not set_cols:
            messagebox.showinfo("Info", "No hay columnas para actualizar en esta tabla")
            return

        set_part = ", ".join([f"{c['name']}=%s" for c in set_cols])
        where_cols = [c for c in schema["columns"] if c.get("pk")]
        where_part = " AND ".join([f"{c['name']}=%s" for c in where_cols])

        values = [data[c["name"]] for c in set_cols]
        values += [data[c["name"]] for c in where_cols]

        sql = f"UPDATE {table_key} SET {set_part} WHERE {where_part}"
        resultado = ejecutar_consulta(sql, tuple(values))
        if resultado == (None, None):
            messagebox.showerror("Error", "No se pudo actualizar el registro")
            return
        load_data(table_key)
        messagebox.showinfo("Éxito", "Registro actualizado")

    def delete_record():
        table_key = current_table["name"]
        if not table_key:
            messagebox.showwarning("Aviso", "Seleccione una tabla")
            return
        schema = TABLE_SCHEMAS[table_key]
        data = read_form_data(table_key)

        ok, msg = ensure_pk_present(schema, data)
        if not ok:
            messagebox.showwarning("Aviso", msg)
            return

        where_cols = [c for c in schema["columns"] if c.get("pk")]
        where_part = " AND ".join([f"{c['name']}=%s" for c in where_cols])
        values = [data[c["name"]] for c in where_cols]

        if not messagebox.askyesno("Confirmar", "¿Desea eliminar este registro?"):
            return

        sql = f"DELETE FROM {table_key} WHERE {where_part}"
        resultado = ejecutar_consulta(sql, tuple(values))
        if resultado == (None, None):
            messagebox.showerror("Error", "No se pudo eliminar el registro")
            return
        load_data(table_key)
        messagebox.showinfo("Éxito", "Registro eliminado")

    def on_tree_select(_event):
        table_key = current_table["name"]
        if not table_key:
            return
        schema = TABLE_SCHEMAS[table_key]
        selection = tree.selection()
        if not selection:
            return
        valores = tree.item(selection[0])["values"]
        for col, valor in zip(schema["columns"], valores):
            widget = field_widgets[col["name"]]
            disabled = col["type"] == "serial"
            set_widget_value(widget, valor, disabled=disabled)

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    ctk.CTkButton(buttons_frame, text="Insertar", width=180, command=insert_record).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Actualizar", width=180, command=update_record).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Eliminar", width=180, command=delete_record).pack(side="left", padx=5)
    ctk.CTkButton(buttons_frame, text="Volver", width=180, command=lambda: volver(root)).pack(side="right", padx=5)


def mostrar_crud_cliente(root):
    # Alias para compatibilidad con el menú existente
    mostrar_crud_general(root)


def volver(root):
    from menu_view import mostrar_menu
    mostrar_menu(root)
