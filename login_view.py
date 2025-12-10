import customtkinter as ctk
from tkinter import messagebox
from clear import limpiar
from session import set_user
from theme import COLOR_2, COLOR_3, COLOR_4, COLOR_5, FONT_TITLE, FONT_SUB, FONT_BUTTON, TEXT_COLOR

def mostrar_login(root):
    limpiar(root)

    try:
        root.configure(fg_color=COLOR_3)
    except Exception:
        root.configure(bg=COLOR_3)

    panel = ctk.CTkFrame(root, fg_color=COLOR_2, corner_radius=12, width=520, height=320)
    panel.pack(expand=True, padx=40, pady=40)
    panel.pack_propagate(False)

    ctk.CTkLabel(panel, text="Sistema de Confecciones", font=FONT_TITLE,
                 text_color=TEXT_COLOR).pack(pady=(30, 10))
    ctk.CTkLabel(panel, text="Selecciona tu rol", font=FONT_SUB,
                 text_color=TEXT_COLOR).pack(pady=(0, 20))

    def login_vendedor():
        set_user(2, "vendedor", "VENDEDOR", "Vendedor")
        from menu_view import mostrar_menu
        mostrar_menu(root)

    def mostrar_login_admin():
        limpiar(root)
        try:
            root.configure(fg_color=COLOR_3)
        except Exception:
            root.configure(bg=COLOR_3)

        admin_panel = ctk.CTkFrame(root, fg_color=COLOR_2, corner_radius=12, width=520, height=360)
        admin_panel.pack(expand=True, padx=40, pady=40)
        admin_panel.pack_propagate(False)

        ctk.CTkLabel(admin_panel, text="Login Administrador", font=FONT_TITLE,
                     text_color=TEXT_COLOR).pack(pady=(30, 20))

        ctk.CTkLabel(admin_panel, text="Usuario:", font=FONT_SUB,
                     text_color=TEXT_COLOR).pack(pady=(10, 2))
        usuario_entry = ctk.CTkEntry(admin_panel, width=360, placeholder_text="adminbd")
        usuario_entry.pack(pady=(2, 10))

        ctk.CTkLabel(admin_panel, text="Contraseña:", font=FONT_SUB,
                     text_color=TEXT_COLOR).pack(pady=(0, 2))
        contra_entry = ctk.CTkEntry(admin_panel, width=360, show="*", placeholder_text="••••••••")
        contra_entry.pack(pady=(2, 20))

        def validar_admin():
            usuario = usuario_entry.get()
            contra = contra_entry.get()

            if usuario == "adminbd" and contra == "12345678":
                set_user(1, "admin", "ADMIN", "Administrador")
                from menu_view import mostrar_menu
                mostrar_menu(root)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")

        def volver_login():
            mostrar_login(root)

        btn_frame = ctk.CTkFrame(admin_panel, fg_color=COLOR_2)
        btn_frame.pack(pady=(10, 20))

        btn_kwargs = dict(width=360, height=50, font=FONT_BUTTON, corner_radius=8)
        ctk.CTkButton(btn_frame, text="Ingresar",
                      fg_color=COLOR_5, hover_color=COLOR_4, text_color=TEXT_COLOR,
                      command=validar_admin, **btn_kwargs).pack(pady=(0, 10))
        ctk.CTkButton(btn_frame, text="Volver",
                      fg_color=COLOR_5, hover_color=COLOR_4, text_color=TEXT_COLOR,
                      command=volver_login, **btn_kwargs).pack()

    btn_kwargs = dict(width=360, height=60, font=FONT_BUTTON, corner_radius=8)

    ctk.CTkButton(panel, text="👨‍💼  ADMINISTRADOR",
                  fg_color=COLOR_5, hover_color=COLOR_4, text_color=TEXT_COLOR,
                  command=mostrar_login_admin, **btn_kwargs).pack(pady=(18, 8))

    ctk.CTkButton(panel, text="👤  VENDEDOR",
                  fg_color=COLOR_5, hover_color=COLOR_4, text_color=TEXT_COLOR,
                  command=login_vendedor, **btn_kwargs).pack(pady=(8, 30))
