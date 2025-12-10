import customtkinter as ctk
from clear import limpiar
from session import set_user

def mostrar_login(root):
    limpiar(root)

    ctk.CTkLabel(root, text="Sistema de Confecciones", font=("Arial", 20, "bold")).pack(pady=30)
    ctk.CTkLabel(root, text="Selecciona tu rol", font=("Arial", 16)).pack(pady=10)

    def login_admin():
        set_user(1, "admin", "ADMIN", "Administrador")
        from menu_view import mostrar_menu
        mostrar_menu(root)

    def login_vendedor():
        set_user(2, "vendedor", "VENDEDOR", "Vendedor")
        from menu_view import mostrar_menu
        mostrar_menu(root)

    ctk.CTkButton(root, text="👨‍💼 ADMINISTRADOR", width=250, height=60, font=("Arial", 14), command=login_admin).pack(pady=10)
    ctk.CTkButton(root, text="👤 VENDEDOR", width=250, height=60, font=("Arial", 14), command=login_vendedor).pack(pady=10)



