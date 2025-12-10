# ...existing code...
import psycopg2
import psycopg2.extras

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="confeccionesuv",
            user="postgres",
            password="2006"
        )
        # asegurar encoding
        conn.set_client_encoding("UTF8")
        return conn
    except Exception as e:
        print("Error en la conexión:", e)
        return None

def ejecutar_consulta(sql, params=None):
    conn = conectar()
    if not conn:
        return (None, None)
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = None
        cols = None
        # si la consulta retorna filas (SELECT o RETURNING)
        if cur.description:
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
        else:
            rows = []
        conn.commit()
        cur.close()
        conn.close()
        return (rows, cols)
    except Exception as e:
        print("Error en ejecutar_consulta:", e)
        try:
            conn.rollback()
        except:
            pass
        try:
            conn.close()
        except:
            pass
        return (None, None)
# ...existing code...