import bcrypt
from database import get_db_connection

def hash_password(password):
    """Hashea una contraseña para almacenarla de forma segura."""
    # Salt es un valor aleatorio que se añade a la contraseña antes de hashearla
    # para hacerla más segura contra ataques de diccionario y rainbow tables.
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(password, hashed_password):
    """Verifica si una contraseña coincide con su hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(username, email, password):
    """
    Registra un nuevo usuario en la base de datos.
    Devuelve (True, "Mensaje de éxito") o (False, "Mensaje de error").
    """
    conn = get_db_connection()
    if not conn:
        return (False, "Error de conexión a la base de datos.")

    try:
        cursor = conn.cursor()
        
        # Hasheamos la contraseña antes de guardarla
        hashed_pw = hash_password(password)
        
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, hashed_pw))
        
        conn.commit()
        
        return (True, f"Usuario '{username}' registrado exitosamente.")

    except conn.IntegrityError as err:
        # Este error ocurre si el usuario o email ya existen (por la restricción UNIQUE)
        return (False, "El nombre de usuario o el email ya están en uso.")
    except Exception as err:
        return (False, f"Ocurrió un error inesperado: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def login_user(username, password):
    """
    Verifica las credenciales de un usuario.
    Devuelve (True, "Mensaje de éxito") o (False, "Mensaje de error").
    """
    conn = get_db_connection()
    if not conn:
        return (False, "Error de conexión a la base de datos.")

    try:
        cursor = conn.cursor(dictionary=True) # dictionary=True devuelve filas como diccionarios
        
        query = "SELECT password_hash FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return (False, "Usuario o contraseña incorrectos.")
            
        # Obtenemos el hash almacenado
        stored_hash = user_data['password_hash']

        # Verificamos si la contraseña proporcionada coincide con el hash
        if check_password(password, stored_hash):
            return (True, "Inicio de sesión exitoso.")
        else:
            return (False, "Usuario o contraseña incorrectos.")
            
    except Exception as err:
        return (False, f"Ocurrió un error inesperado: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
