import tkinter as tk
from login_view import mostrar_login

root = tk.Tk()
root.title("Tienda Confecciones") 
root.geometry("700x500")

mostrar_login(root)

root.mainloop()

