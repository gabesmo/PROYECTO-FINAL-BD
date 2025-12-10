import customtkinter as ctk
from login_view import mostrar_login

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Tienda Confecciones")
root.geometry("700x600")

mostrar_login(root)

root.mainloop()

