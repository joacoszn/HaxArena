import bcrypt
import mysql.connector
# Usamos un punto (.) para indicar que 'database' está en el mismo directorio (backend)
from .database import get_db_connection

def hashear_clave(clave):
    """Hashea una contraseña para almacenarla de forma segura."""
    salt = bcrypt.gensalt()
    clave_hasheada = bcrypt.hashpw(clave.encode('utf-8'), salt)
    return clave_hasheada

def verificar_clave(clave, clave_hasheada):
    """Verifica si una contraseña coincide con su hash."""
    return bcrypt.checkpw(clave.encode('utf-8'), clave_hasheada.encode('utf-8'))

def registrar_usuario(username, email, clave):
    """
    Registra un nuevo usuario en la base de datos.
    Devuelve (True, "Mensaje de éxito") o (False, "Mensaje de error").
    """
    conn = get_db_connection()
    if not conn:
        return (False, "Error de conexión a la base de datos.")

    try:
        cursor = conn.cursor()
        
        clave_hasheada = hashear_clave(clave)
        
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, clave_hasheada.decode('utf-8')))
        
        conn.commit()
        
        return (True, f"Usuario '{username}' registrado exitosamente.")

    except mysql.connector.IntegrityError:
        return (False, "El nombre de usuario o el email ya están en uso.")
    except Exception as err:
        return (False, f"Ocurrió un error inesperado: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def iniciar_sesion_usuario(username, clave):
    """
    Verifica las credenciales de un usuario.
    Devuelve (True, "Mensaje de éxito") o (False, "Mensaje de error").
    """
    conn = get_db_connection()
    if not conn:
        return (False, "Error de conexión a la base de datos.")

    try:
        cursor = conn.cursor()
        
        query = "SELECT password_hash FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if not result:
            return (False, "Usuario o contraseña incorrectos.")
            
        hash_almacenado = result[0]

        if verificar_clave(clave, hash_almacenado):
            return (True, "Inicio de sesión exitoso.")
        else:
            return (False, "Usuario o contraseña incorrectos.")
            
    except Exception as err:
        return (False, f"Ocurrió un error inesperado: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- BLOQUE DE PRUEBA ---
# Este bloque ahora requiere que el script se ejecute como un módulo para que
# las importaciones relativas funcionen.
# Para ejecutarlo, desde la carpeta raíz (HaxArena), usa el comando:
# python3 -m backend.auth
if __name__ == '__main__':
    # Necesitamos importar estas dependencias aquí adentro para que el test funcione
    # al ser ejecutado como módulo.
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

