import customtkinter as ctk
from queries_view import mostrar_consultas
from crud_view import mostrar_crud_general
from clear import limpiar
from session import is_admin, is_vendedor, get_current_user, clear_session
from venta_view import mostrar_venta
from pedidos_view import mostrar_gestion_pedidos
import theme

def mostrar_menu(root):
    limpiar(root)
    theme.apply_root_bg(root)

    panel = ctk.CTkFrame(root, fg_color=theme.COLOR_2, corner_radius=12, width=520)
    panel.pack(expand=True, padx=40, pady=30, fill="both")

    user = get_current_user()
    nombre = user.get('nombre_completo', 'Usuario')
    rol = user.get('rol', '').upper()


    ctk.CTkLabel(panel, text=f"Bienvenido: {nombre}", font=theme.FONT_TITLE,
                 text_color=theme.TEXT_COLOR).pack(pady=(8, 2))
    ctk.CTkLabel(panel, text=f"Rol: {rol}", font=theme.FONT_TITLE,
                 text_color=theme.TEXT_COLOR).pack(pady=(0, 6))
    ctk.CTkLabel(panel, text="Menú Principal", font=theme.FONT_TITLE,
                 text_color=theme.TEXT_COLOR).pack(pady=(4, 12))

    btn_frame = ctk.CTkFrame(panel, fg_color=theme.COLOR_2, corner_radius=0)
    btn_frame.pack(expand=True)         

    bottom_frame = ctk.CTkFrame(panel, fg_color=theme.COLOR_2, corner_radius=0)
    bottom_frame.pack(side="bottom", fill="x", pady=(8,12))

    def make_button(parent, text, cmd, height=None, pady=(6,0)):
        kwargs = dict(theme.BTN_KWARGS) 
        if height:
            kwargs["height"] = height
        kwargs.update({"text": text, "command": cmd})
        btn = ctk.CTkButton(parent, **kwargs)
        btn.pack(pady=pady, anchor="center")
        return btn

    if is_admin():
        make_button(btn_frame, "Gestión CRUD Tablas", lambda: mostrar_crud_general(root), pady=(6,6))
        make_button(btn_frame, "Consultas SQL", lambda: mostrar_consultas(root), pady=(6,6))


    if is_vendedor():
        make_button(btn_frame, "Gestión de Pedidos", lambda: mostrar_gestion_pedidos(root), pady=(6,6))
        make_button(btn_frame, "Procesar Venta", lambda: mostrar_venta(root), pady=(6,6))
        make_button(btn_frame, "Consultas", lambda: mostrar_consultas(root), pady=(6,6))

    def cerrar_sesion(root):
        clear_session()
        from login_view import mostrar_login
        mostrar_login(root)

    make_button(bottom_frame, "Cerrar Sesión", lambda: cerrar_sesion(root), height=48, pady=0)
    make_button(bottom_frame, "Salir", root.quit, height=48, pady=(6,0))
