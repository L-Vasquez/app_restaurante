import sqlite3
import os

def obtener_ruta_bd():
    """Devuelve la ruta absoluta del archivo de la base de datos."""
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directorio_actual, "restaurante.db")

def ejecutar_consulta(query, parametros=(), es_lectura=True):
    """
    Ejecuta consultas SQL de forma segura: abre, ejecuta y cierra automáticamente.
    - es_lectura=True: Devuelve todos los registros con fetchall().
    - es_lectura=False: Ejecuta un INSERT, UPDATE o DELETE y hace commit().
    """
    ruta_bd = obtener_ruta_bd()
    conexion = sqlite3.connect(ruta_bd)
    conexion.execute("PRAGMA foreign_keys = ON;")  # Activar llaves foráneas
    cursor = conexion.cursor()
    
    try:
        cursor.execute(query, parametros)
        if es_lectura:
            resultado = cursor.fetchall()
        else:
            conexion.commit()
            resultado = cursor.lastrowid  # Retorna el ID insertado si aplica
        return resultado
    except Exception as e:
        print(f"Error en la base de datos: {e}")
        return None
    finally:
        conexion.close()