import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="CONFECCIONES",
            user="postgres",
            password="1234"
        )
        return conn
    except Exception as e:
        print("Error en la conexión:", e)
        return None


def ejecutar_consulta(sql, params=None):
    conn = conectar()
    if not conn:
        return None, None

    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        filas = cur.fetchall()
        columnas = [desc[0] for desc in cur.description] if cur.description else []
        conn.close()
        return filas, columnas
    except Exception as e:
        print("Error:", e)
        conn.close()
        return None, None
