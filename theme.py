
COLOR_1 = "#FDCFD9"
COLOR_2 = "#FFEDED"
COLOR_3 = "#B2E5EF"
COLOR_4 = "#A2CEF5"
COLOR_5 = "#86BFF3"
TEXT_COLOR = "#0B2540"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUB = ("Nunito", 16)
FONT_BUTTON = ("Montserrat", 14, "bold")

def apply_root_bg(root):
    """Aplica el color de fondo al root (CTk o Tk)."""
    try:
        root.configure(fg_color=COLOR_3)
    except Exception:
        root.configure(bg=COLOR_3)

BTN_KWARGS = dict(
    width=360,
    height=60,
    corner_radius=8,
    fg_color=COLOR_5,
    hover_color=COLOR_4,
    text_color=TEXT_COLOR,
    font=FONT_BUTTON
)
