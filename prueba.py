import configparser
from cryptography.fernet import Fernet
import tempfile

# Genera una clave de cifrado
clave_cifrado = b'dG-OU1aAt4zYSR5hQuld09TNoZca3jHKGQsR-EJRLVY='

# Crea un objeto Fernet con la clave de cifrado
fernet = Fernet(clave_cifrado)

# Nombre del archivo cifrado
archivo_cifrado = 'configuracion.ini'

# Lee el contenido cifrado del archivo
with open(archivo_cifrado, 'rb') as archivo_ini:
    contenido_cifrado = archivo_ini.read()

# Descifra el contenido
contenido_desencriptado = fernet.decrypt(contenido_cifrado)

# Convierte el contenido desencriptado en una cadena
contenido_str = contenido_desencriptado.decode()

# Parsea el contenido como un archivo .ini
config = configparser.ConfigParser()
config.read_string(contenido_str)

# Ahora puedes acceder a los valores del archivo .ini
url = config['Configuracion'].get('url', '')
username = config['Configuracion'].get('username', '')
password = config['Configuracion'].get('password', '')
machine_name = config['Configuracion'].get('machine_name', '')
ruta_exportacion = config['Configuracion'].get('ruta_exportacion', '')
ultimo_puerto = config['Configuracion'].get('ultimo_puerto', '')

# Utiliza los valores según sea necesario
print(f"URL: {url}")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Machine Name: {machine_name}")
print(f"Ruta Exportación: {ruta_exportacion}")
print(f"Último Puerto: {ultimo_puerto}")
