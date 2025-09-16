import mysql.connector
from mysql.connector import errorcode

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# Modifica estos valores para que coincidan con tu configuración de MySQL.
DB_CONFIG = {
    'user': 'root',
    'password': 'joaquin1233', 
    'host': '127.0.0.1', # O 'localhost'
    'database': 'haxarena_db',
    'raise_on_warnings': True
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Algo está mal con tu usuario o contraseña de MySQL.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Error: La base de datos '{DB_CONFIG['database']}' no existe.")
        else:
            print(f"Error al conectar a la base de datos: {err}")
        return None

if __name__ == '__main__':
    print("Intentando conectar a la base de datos...")
    connection = get_db_connection()
    if connection:
        print("¡Conexión a la base de datos exitosa!")
        connection.close()
    else:
        print("No se pudo establecer la conexión.")
