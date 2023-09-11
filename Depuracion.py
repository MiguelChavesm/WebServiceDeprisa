import os
import datetime
from pathlib import Path


# Lista de carpetas en las que deseas eliminar archivos
carpetas = ["C:/Users/montr/MONTRA Dropbox/Montra Colombia/Archivos Montevideo Indices Fuera de la Matriz/DATA07032023/Image/imagen", 
            "C:/Users/montr/MONTRA Dropbox/Montra Colombia/Archivos Montevideo Indices Fuera de la Matriz/DATA07032023/Image"]

# Número de días después de los cuales los archivos deben eliminarse
dias_para_eliminar = 5

# Obtiene la fecha actual
fecha_actual = datetime.datetime.now()

# Itera sobre cada carpeta
for carpeta in carpetas:
    # Recorre todos los archivos en la carpeta actual
    for archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, archivo)

        # Verifica si el elemento en la carpeta es un archivo
        if os.path.isfile(ruta_archivo):
            # Obtiene la fecha de creación del archivo
            fecha_creacion = datetime.datetime.fromtimestamp(os.path.getctime(ruta_archivo))

            # Calcula la diferencia en días entre la fecha actual y la fecha de creación
            diferencia_dias = (fecha_actual - fecha_creacion).days

            # Si la diferencia en días es mayor que el umbral, elimina el archivo
            if diferencia_dias > dias_para_eliminar:
                os.remove(ruta_archivo)
                print(f"Archivo {archivo} en {carpeta} eliminado porque tenía más de {dias_para_eliminar} días de antigüedad.")