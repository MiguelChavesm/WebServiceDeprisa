import tkinter as tk
from tkinter import ttk
import requests
import json
import datetime

class WebServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Service Client")

        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Enviar Datos")
        self.notebook.add(self.tab2, text="Configuración")
        self.notebook.pack()

        # Configuración de la pestaña 1
        self.sku_var = tk.StringVar()
        self.length_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.response_text = tk.StringVar()

        sku_label = tk.Label(self.tab1, text="SKU:")
        sku_label.grid(row=0, column=0)
        sku_entry = tk.Entry(self.tab1, textvariable=self.sku_var)
        sku_entry.grid(row=0, column=1)

        length_label = tk.Label(self.tab1, text="Largo:")
        length_label.grid(row=1, column=0)
        length_entry = tk.Entry(self.tab1, textvariable=self.length_var)
        length_entry.grid(row=1, column=1)

        width_label = tk.Label(self.tab1, text="Ancho:")
        width_label.grid(row=2, column=0)
        width_entry = tk.Entry(self.tab1, textvariable=self.width_var)
        width_entry.grid(row=2, column=1)

        height_label = tk.Label(self.tab1, text="Alto:")
        height_label.grid(row=3, column=0)
        height_entry = tk.Entry(self.tab1, textvariable=self.height_var)
        height_entry.grid(row=3, column=1)

        weight_label = tk.Label(self.tab1, text="Peso:")
        weight_label.grid(row=4, column=0)
        weight_entry = tk.Entry(self.tab1, textvariable=self.weight_var)
        weight_entry.grid(row=4, column=1)

        send_button = tk.Button(self.tab1, text="Enviar", command=self.send_data)
        send_button.grid(row=5, columnspan=2)

        response_label = tk.Label(self.tab1, text="Respuesta:")
        response_label.grid(row=6, column=0)
        response_entry = tk.Entry(self.tab1, textvariable=self.response_text, state="readonly")
        response_entry.grid(row=6, column=1)

        # Configuración de la pestaña 2
        self.url_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.machine_name_var = tk.StringVar()

        url_label = tk.Label(self.tab2, text="URL del Web Service:")
        url_label.grid(row=0, column=0)
        url_entry = tk.Entry(self.tab2, textvariable=self.url_var)
        url_entry.grid(row=0, column=1)

        username_label = tk.Label(self.tab2, text="Usuario:")
        username_label.grid(row=1, column=0)
        username_entry = tk.Entry(self.tab2, textvariable=self.username_var)
        username_entry.grid(row=1, column=1)

        password_label = tk.Label(self.tab2, text="Contraseña:")
        password_label.grid(row=2, column=0)
        password_entry = tk.Entry(self.tab2, textvariable=self.password_var, show="*")
        password_entry.grid(row=2, column=1)

        machine_name_label = tk.Label(self.tab2, text="Nombre de la Máquina:")
        machine_name_label.grid(row=3, column=0)
        machine_name_entry = tk.Entry(self.tab2, textvariable=self.machine_name_var)
        machine_name_entry.grid(row=3, column=1)

    def send_data(self):
        # Construir el JSON con los datos ingresados
        data = {
            "machine_pid": self.machine_name_var.get(),
            "code": self.sku_var.get(),
            "measure_date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "length": self.length_var.get(),
            "width": self.width_var.get(),
            "height": self.height_var.get(),
            "weight": self.weight_var.get(),
            "unit_type": "cm"
        }

        # Realizar la solicitud POST al WebService
        url = self.url_var.get()
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=(self.username_var.get(), self.password_var.get()))

        # Actualizar la respuesta en la interfaz
        self.response_text.set(response.text)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebServiceApp(root)
    root.mainloop()

#Comentario prueba GIT 
#Otro comentario