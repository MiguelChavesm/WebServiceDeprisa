import os
import datetime

# Carpeta donde se encuentran los archivos que deseas eliminar
carpeta = "C:/Users/montr/MONTRA Dropbox/Montra Colombia/Archivos Montevideo Indices Fuera de la Matriz/DATA07032023/Image/imagen"

# Número de días después de los cuales los archivos deben eliminarse
dias_para_eliminar = 1

# Obtiene la fecha actual
fecha_actual = datetime.datetime.now()

# Recorre todos los archivos en la carpeta
for archivo in os.listdir(carpeta):
    ruta_archivo = os.path.join(carpeta, archivo)

    # Verifica si el elemento en la carpeta es un archivo
    if os.path.isfile(ruta_archivo):
        # Obtiene la fecha de modificación del archivo
        fecha_modificacion = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_archivo))

        # Calcula la diferencia en días entre la fecha actual y la fecha de modificación
        diferencia_dias = (fecha_actual - fecha_modificacion).days

        # Si la diferencia en días es mayor que el umbral, elimina el archivo
        if diferencia_dias > dias_para_eliminar:
            os.remove(ruta_archivo)
            print(f"Archivo {archivo} eliminado porque tenía más de {dias_para_eliminar} días de antigüedad.")
