import customtkinter as ctk
from tkinter import ttk, messagebox
from clear import limpiar
from db import ejecutar_consulta

def mostrar_crud_cliente(root):
    limpiar(root)

    ctk.CTkLabel(root, text="CRUD CLIENTE", font=("Arial", 16)).pack(pady=10)

    frame = ctk.CTkFrame(root)
    frame.pack(pady=10, fill="both", expand=False)

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
                    tree.insert("", "end", values=fila)

    cargar_clientes()

    # Campos
    ctk.CTkLabel(root, text="No_Id").pack()
    id_entry = ctk.CTkEntry(root)
    id_entry.pack()

    ctk.CTkLabel(root, text="Nombre").pack()
    nombre_entry = ctk.CTkEntry(root, width=300)
    nombre_entry.pack()

    # Selección del Treeview
    def seleccionar(event):
        item = tree.selection()
        if not item:
            return
        valores = tree.item(item)["values"]
        id_entry.delete(0, "end")
        nombre_entry.delete(0, "end")
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
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este cliente?"):
            sql = "DELETE FROM cliente WHERE No_Id=%s"
            ejecutar_consulta(sql, (idv,))
            cargar_clientes()
            messagebox.showinfo("Éxito", "Cliente eliminado")

    ctk.CTkButton(root, text="Insertar", width=200, command=insertar).pack(pady=3)
    ctk.CTkButton(root, text="Actualizar", width=200, command=actualizar).pack(pady=3)
    ctk.CTkButton(root, text="Eliminar", width=200, command=eliminar).pack(pady=3)
    ctk.CTkButton(root, text="Volver", width=200,
                  command=lambda: volver(root)).pack(pady=10)


def volver(root):
    from menu_view import mostrar_menu
    mostrar_menu(root)
