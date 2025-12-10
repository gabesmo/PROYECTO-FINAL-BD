import customtkinter as ctk
from queries_view import mostrar_consultas
from crud_view import mostrar_crud_cliente
from clear import limpiar

def mostrar_menu(root):
    limpiar(root)

    ctk.CTkButton(root, text="Gestión CRUD CLIENTE", width=300,
                  command=lambda: mostrar_crud_cliente(root)).pack(pady=10)
    ctk.CTkButton(root, text="Consultas SQL", width=300,
                  command=lambda: mostrar_consultas(root)).pack(pady=10)
    ctk.CTkButton(root, text="Salir", width=300,
                  command=root.quit).pack(pady=10)
