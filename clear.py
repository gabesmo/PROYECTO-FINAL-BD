def limpiar(root):
    for widget in root.winfo_children():
        widget.destroy()
