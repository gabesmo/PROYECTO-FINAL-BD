import tkinter as tk
from tkinter import messagebox
from db import ejecutar_consulta
from clear import limpiar

def mostrar_login(root):
    limpiar(root)

    tk.Label(root, text="Usuario:").pack()
    usuario_entry = tk.Entry(root)
    usuario_entry.pack()

    tk.Label(root, text="Contraseña:").pack()
    contra_entry = tk.Entry(root, show="*")
    contra_entry.pack()

    def validar():
        usuario = usuario_entry.get()
        contra = contra_entry.get()

        if usuario == "" and contra == "":
            from menu_view import mostrar_menu 
            mostrar_menu(root)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    tk.Button(root, text="Ingresar", command=validar).pack(pady=10)


