# backend/perfil.py

from .database import get_db_connection
from datetime import datetime

class PerfilUsuario:
    """
    Clase que representa el perfil de un usuario.
    Este es nuestro primer paso hacia una arquitectura Orientada a Objetos.
    """
    # CORRECCIÓN: El parámetro ahora se llama 'creation_date' para coincidir con la base de datos.
    def __init__(self, id, username, email, creation_date):
        self.id = id
        self.username = username
        self.email = email
        self.creation_date = creation_date # CORRECCIÓN

    def __repr__(self):
        """Representación del objeto para debugging."""
        return f"<PerfilUsuario {self.username}>"
    
    @property
    def fecha_creacion_formateada(self):
        """Devuelve la fecha de creación en un formato legible en español."""
        # CORRECCIÓN: Usamos self.creation_date
        if isinstance(self.creation_date, datetime):
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            mes = meses[self.creation_date.month - 1]
            return self.creation_date.strftime(f"%d de {mes} de %Y")
        return "Fecha no disponible"

def obtener_perfil_usuario(username):
    """
    Obtiene los datos de un usuario de la base de datos y devuelve un objeto PerfilUsuario.
    """
    conn = get_db_connection()
    if conn is None:
        return None, "No se pudo conectar a la base de datos."

    try:
        cursor = conn.cursor() 
        # CORRECCIÓN: La columna se llama 'creation_date', no 'created_at'.
        query = "SELECT id, username, email, creation_date FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        datos_usuario = cursor.fetchone() 

        if datos_usuario:
            # Accedemos a los datos por su índice/posición en la tupla
            perfil = PerfilUsuario(
                id=datos_usuario[0],
                username=datos_usuario[1],
                email=datos_usuario[2],
                creation_date=datos_usuario[3] # CORRECCIÓN
            )
            return perfil, "Perfil encontrado exitosamente."
        else:
            return None, "Usuario no encontrado."

    except Exception as e:
        print(f"Error al obtener el perfil: {e}")
        return None, "Error al consultar la base de datos."
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

