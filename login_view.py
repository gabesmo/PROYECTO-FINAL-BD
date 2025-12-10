# ...existing code...
import customtkinter as ctk
from clear import limpiar
from session import set_user

def mostrar_login(root):
    limpiar(root)

    # Paleta
    COLOR_1 = "#FDCFD9"  # suave
    COLOR_2 = "#FFEDED"  # fondo del panel (rosado)
    COLOR_3 = "#B2E5EF"  # fondo general
    COLOR_4 = "#A2CEF5"  # hover / secundario
    COLOR_5 = "#86BFF3"  # primario botones
    TEXT_COLOR = "#0B2540"  # color de texto (oscuro / negro)

    FONT_TITLE = ("Segoe UI", 22, "bold")
    FONT_SUB = ("Nunito", 16)
    FONT_BUTTON = ("Montserrat", 14, "bold")

    # Si root es un CTk, usar fg_color; si es Tk, usar bg
    try:
        root.configure(fg_color=COLOR_3)
    except Exception:
        root.configure(bg=COLOR_3)

    # Panel rosado más ancho: fijar width y evitar pack_propagate para mantener tamaño fijo
    panel = ctk.CTkFrame(root, fg_color=COLOR_2, corner_radius=12, width=520, height=320)
    panel.pack(expand=True, padx=40, pady=40)
    panel.pack_propagate(False)

    ctk.CTkLabel(panel, text="Sistema de Confecciones", font=FONT_TITLE,
                 text_color=TEXT_COLOR).pack(pady=(30, 10))
    ctk.CTkLabel(panel, text="Selecciona tu rol", font=FONT_SUB,
                 text_color=TEXT_COLOR).pack(pady=(0, 20))

    def login_admin():
        set_user(1, "admin", "ADMIN", "Administrador")
        from menu_view import mostrar_menu
        mostrar_menu(root)

    def login_vendedor():
        set_user(2, "vendedor", "VENDEDOR", "Vendedor")
        from menu_view import mostrar_menu
        mostrar_menu(root)

# ...existing code...
    # Botones más anchos y con texto en negro (TEXT_COLOR)
    btn_kwargs = dict(width=360, height=60, font=FONT_BUTTON, corner_radius=8)

    ctk.CTkButton(panel, text="👨‍💼  ADMINISTRADOR",
                  fg_color=COLOR_5, hover_color=COLOR_4, text_color=TEXT_COLOR,
                  command=login_admin, **btn_kwargs).pack(pady=(18, 8))

    ctk.CTkButton(panel, text="👤  VENDEDOR",
                  fg_color=COLOR_5, hover_color=COLOR_4, text_color=TEXT_COLOR,
                  command=login_vendedor, **btn_kwargs).pack(pady=(8, 30))
# ...existing code...