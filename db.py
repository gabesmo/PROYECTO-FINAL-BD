import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Cconfeccionesuv",
            user="postgres",
            password="2006",
            client_encoding="utf8"
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
        
        # Check if the query returns results
        if cur.description is None:
            # No results to fetch (INSERT, UPDATE, DELETE, etc.)
            conn.commit()
            conn.close()
            return [], []
        
        filas = cur.fetchall()
        columnas = [desc[0] for desc in cur.description]
        conn.close()
        return filas, columnas
    except psycopg2.Error as e:
        print("Error de PostgreSQL:", e)
        if conn:
            conn.rollback()
            conn.close()
        return None, None
    except Exception as e:
        print("Error:", e)
        if conn:
            conn.close()
        return None, None
