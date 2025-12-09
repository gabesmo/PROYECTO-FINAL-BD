import tkinter as tk
from tkinter import ttk, messagebox
from consultas import consultas_predef
from db import ejecutar_consulta
from clear import limpiar

def mostrar_consultas(root):
    limpiar(root)

    tk.Label(root, text="Tabla:").grid(row=0, column=0, padx=5, pady=5)
    tabla_cb = ttk.Combobox(root, values=list(consultas_predef.keys()), state="readonly", width=30)
    tabla_cb.grid(row=0, column=1, padx=5)

    tk.Label(root, text="Consulta:").grid(row=1, column=0, padx=5, pady=5)
    consulta_cb = ttk.Combobox(root, state="readonly", width=60)
    consulta_cb.grid(row=1, column=1, padx=5)

    # Frame para el treeview con scrollbars
    frame = tk.Frame(root)
    frame.grid(row=3, columnspan=2, sticky="nsew", padx=5, pady=10)

    # Scrollbar vertical
    scrollbar_y = ttk.Scrollbar(frame)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    # Scrollbar horizontal
    scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    tree = ttk.Treeview(
        frame,
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    # Configurar pesos para la grilla
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    def cargar_consultas(event):
        tabla = tabla_cb.get()
        if tabla in consultas_predef:
            consulta_cb["values"] = list(consultas_predef[tabla].keys())

    tabla_cb.bind("<<ComboboxSelected>>", cargar_consultas)

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
        
        if not filas or not columnas:
            messagebox.showinfo("Información", "La consulta no retornó datos")
            tree.delete(*tree.get_children())
            tree["columns"] = []
            return

        # Limpiar treeview anterior
        tree.delete(*tree.get_children())
        for item in tree.get_children():
            tree.delete(item)

        # Configurar dinámicamente las columnas
        tree["columns"] = columnas
        tree["show"] = "headings"

        # Calcular ancho dinámico para las columnas
        ancho_dinamico = max(120, 700 // len(columnas)) if columnas else 120

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=ancho_dinamico)

        # Insertar filas
        for fila in filas:
            tree.insert("", tk.END, values=fila)

    tk.Button(root, text="Ejecutar", command=ejecutar).grid(row=2, columnspan=2, pady=10)
    tk.Button(root, text="Volver", command=lambda: volver(root)).grid(row=4, columnspan=2, pady=5)


def volver(root):
    from menu_view import mostrar_menu
    mostrar_menu(root)
