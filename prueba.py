import tkinter as tk
import sqlite3
from tkinter import Scrollbar  
from tkinter import ttk

# Crear una conexión a la base de datos o crearla si no existe
conn = sqlite3.connect('MONTRADB.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS LogIn (
                  Usuario TEXT,
                  Contraseña TEXT,
                  Acceso TEXT)''')
conn.commit()

# Función para guardar los datos en la base de datos
def guardar_datos():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    acceso = entry_acceso.get()
    cursor.execute("INSERT INTO LogIn VALUES (?, ?, ?)", (usuario, contraseña, acceso))
    conn.commit()
    actualizar_lista()

# Función para mostrar los datos en la parte inferior
def actualizar_lista():

# Definir etiquetas de estilo con colores
    tree.tag_configure('ADMINISTRADOR', background='#FF6666') #ROJO
    tree.tag_configure('OPERARIO', background='#B7FF66') #VERDE
    tree.tag_configure('SUPERUSUARIO', background='#66DCFF') #AZUL

    # Limpiar la tabla actual
    for item in tree.get_children():
        tree.delete(item)

    # Consultar la base de datos y agregar los datos al Treeview
    cursor.execute("SELECT * FROM LogIn")
    for row in cursor.fetchall():
        access_type = row[2]  # Obtener el tipo de acceso de la fila
        tree.insert("", "end", values=row, tags=(access_type.upper(),))  # Asignar la etiqueta de estilo en mayúsculas
        
# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Registro")

# Crear una lista de opciones para el campo de "Acceso"
opciones_acceso = ["ADMINISTRADOR", "OPERARIO"]

# Crear un StringVar para el campo de "Acceso"
var_acceso = tk.StringVar()


# Crear campos de entrada
label_usuario = tk.Label(root, text="Usuario:")
entry_usuario = tk.Entry(root)
label_contraseña = tk.Label(root, text="Contraseña:")
entry_contraseña = tk.Entry(root)
# Crear el campo de "Acceso" con una lista desplegable
label_acceso = tk.Label(root, text="Acceso:")
entry_acceso = ttk.Combobox(root, textvariable=var_acceso, values=opciones_acceso)

# Inicializar la lista desplegable con el primer elemento
var_acceso.set(opciones_acceso[0])

# Botón para guardar datos
button_guardar = tk.Button(root, text="Guardar", command=guardar_datos)

# Lista para mostrar los datos
#list_box = tk.Listbox(root, width=40)
tree = ttk.Treeview(root, columns=("Usuario", "Contraseña", "Acceso"), show="headings")
scrollbar = Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)

# Configurar las columnas
tree.heading("Usuario", text="Usuario")
tree.heading("Contraseña", text="Contraseña")
tree.heading("Acceso", text="Acceso")

# Vincula el Scrollbar a la lista
tree.config(yscrollcommand=scrollbar.set)

# Colocar widgets en la ventana
label_usuario.grid(row=0, column=0)
entry_usuario.grid(row=0, column=1)
label_contraseña.grid(row=1, column=0)
entry_contraseña.grid(row=1, column=1)
label_acceso.grid(row=2, column=0)
entry_acceso.grid(row=2, column=1)
button_guardar.grid(row=3, column=0, columnspan=2)
tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)  # Ajusta el padx y pady según tus preferencias
scrollbar.grid(row=4, column=3, sticky="ns")

# Actualizar la lista de datos al inicio
actualizar_lista()

# Iniciar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos cuando se cierra la aplicación
conn.close()