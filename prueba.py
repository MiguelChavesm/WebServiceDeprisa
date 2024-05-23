import tkinter as tk
from tkinter import ttk
import datetime

class MedicionApp:
    def __init__(self, root):
        self.root = root
        self.create_medicion_tab()
        self.root.mainloop()

    def create_medicion_tab(self):
        self.medicion_tab = ttk.Frame(self.root)
        self.medicion_tab.pack(fill="both", expand=True)

        self.sku_var = tk.StringVar()
        self.length_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()

        # Crear la tabla para mostrar los datos
        columns = ('Sku', 'Largo', 'Ancho', 'Alto', 'Peso', 'Fecha', 'Respuesta')
        self.tree = ttk.Treeview(self.medicion_tab, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')  # Centrar el texto en cada columna

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.medicion_tab.grid_rowconfigure(0, weight=1)
        self.medicion_tab.grid_columnconfigure(0, weight=1)

        # Crear barras de desplazamiento
        y_scroll = ttk.Scrollbar(self.medicion_tab, orient="vertical", command=self.tree.yview)
        y_scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=y_scroll.set)
        
        self.abrir_puerto_button = ttk.Button(self.medicion_tab, text="Abrir Puerto", command=self.send_data)
        self.abrir_puerto_button.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    def send_data(self):
        # Obtener los valores de los campos
        sku = self.sku_var.get()
        largo = self.length_var.get()
        ancho = self.width_var.get()
        alto = self.height_var.get()
        peso = self.weight_var.get()
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje = "Mensaje de ejemplo"  # Placeholder para el mensaje real

        # Insertar valores en la tabla
        self.tree.insert('', 'end', values=(sku, largo, ancho, alto, peso, fecha, mensaje))

root = tk.Tk()
app = MedicionApp(root)
