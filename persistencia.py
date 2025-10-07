# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Clase estática para guardar y cargar el estado completo del sistema de cine.

import pickle
import os

# Nombre del archivo donde se guardarán los datos
ARCHIVO_DATOS = 'cine_data.pkl'

class GestorPersistencia:
    """
    Clase que maneja el guardado y la carga de los datos del cine.
    Utiliza el módulo 'pickle' para serializar los objetos de Python.
    """

    @staticmethod
    def guardar_datos(cine_obj, registro_entradas):
        """
        Guarda el objeto Cine y el registro de entradas en un archivo binario.
        """
        try:
            # Creamos un diccionario con el estado del cine y el registro
            datos = {
                'salas': cine_obj._Cine__salas, # Accedemos al atributo privado __salas
                'entradas': registro_entradas
            }
            
            with open(ARCHIVO_DATOS, 'wb') as f:
                pickle.dump(datos, f)
            print(f"\n[INFO] Datos del cine guardados exitosamente en {ARCHIVO_DATOS}.")
        except Exception as e:
            print(f"\n[ERROR] Fallo al guardar datos: {e}")

    @staticmethod
    def cargar_datos(cine_obj):
        """
        Carga los datos guardados desde el archivo binario, si existe.
        Devuelve el registro de entradas cargado o None si falla.
        """
        if not os.path.exists(ARCHIVO_DATOS):
            print(f"[INFO] Archivo de datos '{ARCHIVO_DATOS}' no encontrado. Iniciando limpio.")
            return None

        try:
            with open(ARCHIVO_DATOS, 'rb') as f:
                datos = pickle.load(f)
            
            # Asignamos las salas cargadas al objeto Cine actual
            cine_obj._Cine__salas = datos.get('salas', [])
            
            print(f"[INFO] Datos del cine cargados exitosamente desde {ARCHIVO_DATOS}.")
            
            # Devolvemos las entradas para que el main las asigne
            return datos.get('entradas', [])
            
        except Exception as e:
            print(f"[ERROR] Fallo al cargar datos (el archivo podría estar corrupto): {e}")
            # Si hay un error, lo tratamos como un inicio limpio
            return None

# Nota: El objeto Cine tiene un atributo privado (__salas), 
# accedemos a él mediante el 'name mangling': _Cine__salas.
