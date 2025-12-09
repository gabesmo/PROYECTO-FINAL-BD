import tkinter as tk
from tkinter import ttk, messagebox
from clear import limpiar
from db import ejecutar_consulta

def mostrar_crud_cliente(root):
    limpiar(root)

    tk.Label(root, text="CRUD CLIENTE", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tree = ttk.Treeview(frame, columns=("No_Id", "Nombre"), show="headings")
    tree.heading("No_Id", text="No_Id")
    tree.heading("Nombre", text="Nombre")
    tree.pack()

    # ---------- Cargar datos ----------
    def cargar_clientes():
        tree.delete(*tree.get_children())
        sql = "SELECT * FROM cliente ORDER BY No_Id;"
        resultado = ejecutar_consulta(sql)
        if resultado and resultado != (None, None):
            filas, _ = resultado
            if filas:
                for fila in filas:
                    tree.insert("", tk.END, values=fila)

    cargar_clientes()

    # Campos de entrada
    tk.Label(root, text="No_Id").pack()
    id_entry = tk.Entry(root)
    id_entry.pack()

    tk.Label(root, text="Nombre").pack()
    nombre_entry = tk.Entry(root, width=40)
    nombre_entry.pack()

    # Manejo de selección
    def seleccionar(event):
        item = tree.selection()
        if not item: return
        valores = tree.item(item)["values"]
        id_entry.delete(0, tk.END)
        nombre_entry.delete(0, tk.END)
        id_entry.insert(0, valores[0])
        nombre_entry.insert(0, valores[1])

    tree.bind("<<TreeviewSelect>>", seleccionar)

    # Botón Insertar
    def insertar():
        idv = id_entry.get()
        nom = nombre_entry.get()
        if not idv or not nom:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios")
            return
        sql = "INSERT INTO cliente (No_Id, Nombre) VALUES (%s, %s)"
        ejecutar_consulta(sql, (idv, nom))
        cargar_clientes()
        messagebox.showinfo("Éxito", "Cliente agregado")

    # Botón Actualizar
    def actualizar():
        idv = id_entry.get()
        nom = nombre_entry.get()
        sql = "UPDATE cliente SET Nombre=%s WHERE No_Id=%s"
        ejecutar_consulta(sql, (nom, idv))
        cargar_clientes()
        messagebox.showinfo("Éxito", "Cliente actualizado")

    # Botón Eliminar
    def eliminar():
        idv = id_entry.get()
        if not idv:
            return
        respuesta = messagebox.askyesno("Confirmar", "¿Desea eliminar este cliente?")
        if respuesta:
            sql = "DELETE FROM cliente WHERE No_Id=%s"
            ejecutar_consulta(sql, (idv,))
            cargar_clientes()
            messagebox.showinfo("Éxito", "Cliente eliminado")

    # Botones
    tk.Button(root, text="Insertar", width=20, command=insertar).pack(pady=3)
    tk.Button(root, text="Actualizar", width=20, command=actualizar).pack(pady=3)
    tk.Button(root, text="Eliminar", width=20, command=eliminar).pack(pady=3)

    tk.Button(root, text="Volver", width=20,
              command=lambda: volver(root)).pack(pady=10)


def volver(root):
    from menu_view import mostrar_menu
    mostrar_menu(root)
