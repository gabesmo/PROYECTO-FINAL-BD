import customtkinter as ctk
from queries_view import mostrar_consultas
from crud_view import mostrar_crud_general
from clear import limpiar
from session import is_admin, is_vendor, get_current_user, clear_session
from venta_view import mostrar_venta
from pedidos_view import mostrar_gestion_pedidos

def mostrar_menu(root):
    limpiar(root)
    
    user = get_current_user()
    ctk.CTkLabel(root, text=f"Bienvenido: {user['nombre_completo']}", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(root, text=f"Rol: {user['rol']}", font=("Arial", 12)).pack(pady=5)
    
    ctk.CTkLabel(root, text="Menú Principal", font=("Arial", 16, "bold")).pack(pady=15)
    
    # Opciones para ADMIN
    if is_admin():
        ctk.CTkButton(root, text="Gestión CRUD Tablas", width=300,
                      command=lambda: mostrar_crud_general(root)).pack(pady=5)
        ctk.CTkButton(root, text="Consultas SQL", width=300,
                      command=lambda: mostrar_consultas(root)).pack(pady=5)
    
    # Opciones para VENDEDOR
    if is_vendor():
        ctk.CTkButton(root, text="Gestión de Pedidos", width=300,
                      command=lambda: mostrar_gestion_pedidos(root)).pack(pady=5)
        ctk.CTkButton(root, text="Procesar Venta", width=300,
                      command=lambda: mostrar_venta(root)).pack(pady=5)
        ctk.CTkButton(root, text="Consultas", width=300,
                      command=lambda: mostrar_consultas(root)).pack(pady=5)
    
    ctk.CTkButton(root, text="Cerrar Sesión", width=300,
                  command=lambda: cerrar_sesion(root)).pack(pady=10)
    ctk.CTkButton(root, text="Salir", width=300,
                  command=root.quit).pack(pady=5)

def cerrar_sesion(root):
    clear_session()
    from login_view import mostrar_login
    mostrar_login(root)

def mostrar_gestion_pedidos(root):
    # Llama a la vista especializada de pedidos
    from pedidos_view import mostrar_gestion_pedidos as sg
    sg(root)

def mostrar_venta(root):
    # Llama a la vista de procesamiento de venta
    from venta_view import mostrar_venta as sv
    sv(root)
