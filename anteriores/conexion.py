import sqlite3
import os

def obtener_ruta_bd():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directorio_actual, "restaurante.db")

def ejecutar_consulta(query, parametros=(), es_lectura=True):
    """
    Función genérica para manejar la conexión de forma segura.
    Abre la conexión, ejecuta la consulta y la cierra automáticamente.
    """
    ruta_bd = obtener_ruta_bd()
    conexion = sqlite3.connect(ruta_bd)
    conexion.execute("PRAGMA foreign_keys = ON;") # Habilitar relaciones
    cursor = conexion.cursor()
    
    try:
        cursor.execute(query, parametros)
        if es_lectura:
            resultado = cursor.fetchall()
        else:
            conexion.commit()
            resultado = cursor.lastrowid # Devuelve el ID insertado si es un INSERT
        return resultado
    except Exception as e:
        print(f"Error en la base de datos: {e}")
        return None
    finally:
        conexion.close() # Se cierra siempre para liberar el archivo