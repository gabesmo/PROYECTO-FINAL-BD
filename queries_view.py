import customtkinter as ctk
from tkinter import ttk, messagebox
from consultas import consultas_predef
from db import ejecutar_consulta
from clear import limpiar

def mostrar_consultas(root):
    limpiar(root)


    ctk.CTkLabel(root, text="Tabla:").grid(row=0, column=0, padx=5, pady=5)

    def actualizar_consultas(tabla_seleccionada):
        """Cargar lista de consultas según la tabla"""
        if tabla_seleccionada in consultas_predef:
            valores = list(consultas_predef[tabla_seleccionada].keys())
            consulta_cb.configure(values=valores)
            consulta_cb.set("")  # IRefrescar selección

    tabla_cb = ctk.CTkComboBox(
        root, 
        values=list(consultas_predef.keys()),
        width=200,
        command=actualizar_consultas 
    )
    tabla_cb.grid(row=0, column=1, padx=5)

    
    ctk.CTkLabel(root, text="Consulta:").grid(row=1, column=0, padx=5, pady=5)

    consulta_cb = ctk.CTkComboBox(root, values=[], width=400)
    consulta_cb.grid(row=1, column=1, padx=5)

    
    frame = ctk.CTkFrame(root)
    frame.grid(row=3, columnspan=2, sticky="nsew", padx=5, pady=10)

    scrollbar_y = ttk.Scrollbar(frame)
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(
        frame,
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )
    tree.pack(side="left", fill="both", expand=True)

    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    
    def ejecutar():
        tabla = tabla_cb.get()
        con_name = consulta_cb.get()

        if not tabla or not con_name:
            messagebox.showwarning("Aviso", "Seleccione tabla y consulta")
            return

        sql = consultas_predef[tabla][con_name]
        resultado = ejecutar_consulta(sql)

        if resultado is None or resultado == (None, None):
            messagebox.showerror("Error", "Error al ejecutar la consulta")
            return

        filas, columnas = resultado

        tree.delete(*tree.get_children())

        if not filas or not columnas:
            messagebox.showinfo("Información", "La consulta no retornó datos")
            tree["columns"] = []
            return

        tree["columns"] = columnas
        tree["show"] = "headings"

        ancho = max(120, 700 // len(columnas))

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=ancho)

        for fila in filas:
            tree.insert("", "end", values=fila)

    ctk.CTkButton(root, text="Ejecutar", command=ejecutar).grid(row=2, columnspan=2, pady=10)
    ctk.CTkButton(root, text="Volver", command=lambda: volver(root)).grid(row=4, columnspan=2, pady=5)

def volver(root):
    from menu_view import mostrar_menu
    mostrar_menu(root)
