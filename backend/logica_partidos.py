# backend/logica_partidos.py

from .database import get_db_connection
from datetime import datetime

# --- Clases (Modelo de Datos) ---

class Partido:
    """
    Clase que representa un partido dentro de HaxArena.
    Refleja la estructura de la tabla `partidos`.
    """
    def __init__(self, id, fecha, goles_red, goles_blue, duracion_segundos, ganador, estadisticas=None):
        self.id = id
        self.fecha = fecha
        self.goles_red = goles_red
        self.goles_blue = goles_blue
        self.duracion_segundos = duracion_segundos
        self.ganador = ganador
        self.estadisticas = estadisticas if estadisticas is not None else []

    def __repr__(self):
        return f"<Partido id={self.id} - Red {self.goles_red} vs {self.goles_blue} Blue>"

class EstadisticasJugador:
    """
    Clase que representa las estadísticas de un jugador en un partido específico.
    Refleja la estructura de la tabla `estadisticas_jugador`.
    """
    def __init__(self, id, partido_id, jugador_id, equipo, goles, asistencias, mvps):
        self.id = id
        self.partido_id = partido_id
        self.jugador_id = jugador_id
        self.equipo = equipo
        self.goles = goles
        self.asistencias = asistencias
        self.mvps = mvps

    def __repr__(self):
        return f"<Estadisticas Jugador id={self.jugador_id} en Partido id={self.partido_id}>"

# --- Lógica de Interacción con la Base de Datos ---

def registrar_partido(goles_red, goles_blue, duracion_segundos, ganador, estadisticas_jugadores):
    """
    Registra un partido completo con las estadísticas de todos los jugadores.
    
    :param estadisticas_jugadores: Una lista de diccionarios, cada uno representando las stats de un jugador.
    Ejemplo:
    [
        {'jugador_id': 1, 'equipo': 'rojo', 'goles': 2, 'asistencias': 1, 'mvps': 0},
        {'jugador_id': 2, 'equipo': 'azul', 'goles': 1, 'asistencias': 0, 'mvps': 1}
    ]
    """
    conn = get_db_connection()
    if not conn:
        return None, "Error de conexión a la base de datos."

    cursor = conn.cursor()
    try:
        # Paso 1: Insertar el resultado en la tabla `partidos`
        query_partido = """
            INSERT INTO partidos (goles_red, goles_blue, duracion_segundos, ganador)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_partido, (goles_red, goles_blue, duracion_segundos, ganador))
        id_nuevo_partido = cursor.lastrowid

        # Paso 2: Insertar las estadísticas de cada jugador
        query_stats = """
            INSERT INTO estadisticas_jugador (partido_id, jugador_id, equipo, goles, asistencias, mvp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        datos_para_insertar = []
        for stats in estadisticas_jugadores:
            datos_para_insertar.append((
                id_nuevo_partido,
                stats['jugador_id'],
                stats['equipo'],
                stats.get('goles', 0),
                stats.get('asistencias', 0),
                stats.get('mvp')
            ))
        
        cursor.executemany(query_stats, datos_para_insertar)

        conn.commit()
        return id_nuevo_partido, "Partido registrado exitosamente."

    except Exception as e:
        conn.rollback()
        print(f"Error al registrar partido: {e}")
        return None, "Ocurrió un error inesperado al registrar el partido."
    finally:
        cursor.close()
        conn.close()

# --- Bloque de Prueba ---
if __name__ == '__main__':
    # Simulación de un partido para probar la función
    print("--- Probando el registro de un nuevo partido ---")
    
    # Datos de ejemplo. Necesitarás IDs de jugadores que existan en tu tabla `users`.
    # Cambia los IDs (1, 2, 3, 4) por IDs reales de tu base de datos.
    stats_ejemplo = [
        {'jugador_id': 1, 'equipo': 'rojo', 'goles': 3, 'asistencias': 1, 'mvp': True},
    ]
    
    id_partido, mensaje = registrar_partido(
        goles_red=5,
        goles_blue=3,
        duracion_segundos=300,
        ganador='Red',  # Usamos 'Red', 'Blue' o 'Empate' como en tu ENUM
        estadisticas_jugadores=stats_ejemplo
    )

    if id_partido:
        print(f"Resultado: ¡Éxito! {mensaje} (ID de Partido: {id_partido})")
    else:
        print(f"Resultado: Falló. {mensaje}")
