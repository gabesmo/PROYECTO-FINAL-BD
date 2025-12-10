import customtkinter as ctk
from tkinter import messagebox
from db import ejecutar_consulta
from clear import limpiar

def mostrar_login(root):
    limpiar(root)

    ctk.CTkLabel(root, text="Usuario:").pack(pady=5)
    usuario_entry = ctk.CTkEntry(root, width=250)
    usuario_entry.pack()

    ctk.CTkLabel(root, text="Contraseña:").pack(pady=5)
    contra_entry = ctk.CTkEntry(root, show="*", width=250)
    contra_entry.pack()

    def validar():
        usuario = usuario_entry.get()
        contra = contra_entry.get()

        if usuario == "" and contra == "":
            from menu_view import mostrar_menu
            mostrar_menu(root)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    ctk.CTkButton(root, text="Ingresar", command=validar, width=200).pack(pady=15)



