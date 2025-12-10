# Módulo de sesión global para almacenar datos del usuario logueado
session_data = {
    "user_id": None,
    "username": None,
    "rol": None,
    "nombre_completo": None,
    "logged_in": False,
}

def set_user(user_id, username, rol, nombre_completo):
    session_data["user_id"] = user_id
    session_data["username"] = username
    session_data["rol"] = rol
    session_data["nombre_completo"] = nombre_completo
    session_data["logged_in"] = True

def clear_session():
    session_data["user_id"] = None
    session_data["username"] = None
    session_data["rol"] = None
    session_data["nombre_completo"] = None
    session_data["logged_in"] = False

def is_admin():
    return session_data.get("rol") == "ADMIN"

def is_vendor():
    return session_data.get("rol") == "VENDEDOR"

def is_logged_in():
    return session_data.get("logged_in", False)

def get_current_user():
    return session_data
