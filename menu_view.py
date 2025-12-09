import tkinter as tk
from queries_view import mostrar_consultas
from crud_view import mostrar_crud_cliente
from clear import limpiar

def mostrar_menu(root):
    limpiar(root)

    tk.Button(root, text="Gestión CRUD CLIENTE", width=30,
          command=lambda: mostrar_crud_cliente(root)).pack(pady=10)
    tk.Button(root, text="Consultas SQL", width=30,
              command=lambda: mostrar_consultas(root)).pack(pady=10)
    tk.Button(root, text="Salir", width=30,
              command=root.quit).pack(pady=10)
