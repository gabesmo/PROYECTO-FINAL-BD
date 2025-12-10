import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="CONFECCIONES",
            user="postgres",
            password="08220920"
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

        # Si la consulta retorna filas (SELECT), cur.description trae metadatos
        if cur.description:
            filas = cur.fetchall()
            columnas = [desc[0] for desc in cur.description]
            conn.close()
            return filas, columnas

        # Para INSERT/UPDATE/DELETE se hace commit y se retorna filas afectadas
        conn.commit()
        afectadas = cur.rowcount
        conn.close()
        return afectadas, []
    except Exception as e:
        print("Error:", e)
        conn.rollback()
        conn.close()
        return None, None
