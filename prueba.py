import customtkinter
import tkinter as tk
from tkinter import ttk
import requests
import json
import datetime
from PIL import Image



class WebServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Service Client")
        root.iconbitmap('Icons/montra.ico')

        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.medicion_tab = ttk.Frame(self.notebook)
        self.configuracion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.medicion_tab, text="Enviar Datos")
        self.notebook.add(self.configuracion_tab, text="Configuración")
        self.notebook.pack(fill="both", expand=True)
        self.create_medicion_tab()
        self.create_configuracion_tab()
        
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def cerrar_aplicacion(self):
        self.root.destroy()
    
    def imagenes(self):
        self.logo_montra = tk.PhotoImage(file="Icons/Logo_Montra3.png")
        self.logo_montra = self.logo_montra.subsample(1, 1)
        
        self.logo_cubiscan = tk.PhotoImage(file="Icons/Cubiscan_logo.png")
        self.logo_cubiscan = self.logo_cubiscan.subsample(1, 1)
        
        self.logo_deprisa = tk.PhotoImage(file="Icons/Deprisa_logo.png")
        self.logo_deprisa = self.logo_deprisa.subsample(1, 1)
        
    def create_medicion_tab(self):
        self.imagenes()
        self.sku_var = tk.StringVar()
        self.length_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.response_text = tk.StringVar()

        # Insertarla en una etiqueta.
        self.colorbackground= "lightgrey"
        self.background = ttk.Label(self.medicion_tab, background=self.colorbackground)
        self.background.grid(row=0, column=0, rowspan=9,padx=(0,20), sticky="snew")
        
        label_montra = ttk.Label(self.medicion_tab, image=self.logo_montra, background=self.colorbackground)
        label_montra.grid(row=0, column=0, rowspan=3, padx=(10,20), pady=(10,0), sticky="s")
        
        label_deprisa = ttk.Label(self.medicion_tab, image=self.logo_deprisa, background=self.colorbackground)
        label_deprisa.grid(row=4, column=0, rowspan=2, padx=(15,20), pady=10, sticky="ew")
        
        label_cubiscan = ttk.Label(self.medicion_tab, image=self.logo_cubiscan,background=self.colorbackground)
        label_cubiscan.grid(row=3, column=0, rowspan=3, padx=(5,20), sticky="n")
        
        # Botón de cerrar de sesión
        logout_image = customtkinter.CTkImage(Image.open("Icons/logout.png").resize((100,100), Image.Resampling.LANCZOS))
        boton_logout = customtkinter.CTkButton(self.medicion_tab, text="Cerrar Sesión", corner_radius=1,font=("Helvetica", 14), text_color="#000000", fg_color="#FFFFFF", hover_color="#828890", width=200, height=20, compound="left", image= logout_image)
        boton_logout.grid(row=5, column=0, columnspan=1, padx=(10,30), pady=5, sticky="new")
        
        ttk.Label(self.medicion_tab, text="SKU:").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.sku_entry = ttk.Entry(self.medicion_tab, textvariable=self.sku_var, font=('Helvetica', 10), width=22)
        self.sku_entry.grid(row=0, column=2, padx=10, pady=0, ipadx=15)

        self.send_button = ttk.Button(self.medicion_tab, text="Enviar",  compound="right", command=self.send_data)
        self.send_button.grid(row=2, rowspan=1, column=1, columnspan=2 ,padx=10, pady=0, sticky="n")

        ttk.Label(self.medicion_tab, text="Largo:").grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.largo_entry = ttk.Entry(self.medicion_tab, textvariable=self.length_var)
        self.largo_entry.grid(row=0, column=4, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Ancho:").grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.ancho_entry = ttk.Entry(self.medicion_tab, textvariable=self.width_var)
        self.ancho_entry.grid(row=1, column=4, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Alto:").grid(row=2, column=3, padx=10, pady=5, sticky="w")
        self.alto_entry = ttk.Entry(self.medicion_tab, textvariable=self.height_var)
        self.alto_entry.grid(row=2, column=4, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Peso:").grid(row=3, column=3, padx=10, pady=5, sticky="w")
        self.peso_entry = ttk.Entry(self.medicion_tab, textvariable=self.weight_var)
        self.peso_entry.grid(row=3, column=4, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Respuesta:").grid(row=5, column=1, columnspan=2, padx=5, sticky="w")
        self.response_entry = tk.Text(self.medicion_tab, state="disabled", background="#FCFFD0", font=("Arial", 10))
        self.response_entry.config(width=20, height=5)
        self.response_entry.grid(row=6, column=1, columnspan=20, pady=5, sticky="nsew")

        
        # Crear la tabla para mostrar los datos
        columns = ('Sku', 'Largo', 'Ancho', 'Alto', 'Peso', 'Fecha', 'Usuario')
        self.tree = ttk.Treeview(self.medicion_tab, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column('Sku', width=200)
            self.tree.column('Largo', width=50)
            self.tree.column('Ancho', width=50)
            self.tree.column('Alto', width=50)
            self.tree.column('Peso', width=50)
            self.tree.column('Fecha', width=130)
            self.tree.column('Usuario', width=80)
            #self.tree.column(col, width=100)

        self.tree.grid(row=4, column=1, columnspan=20, pady=(10,10))
        
        # Aplicar un estilo con bordes a la tabla
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 9), rowheight=20)
        style.configure("Treeview.Heading", font=('Helvetica', 9))
        style.configure("Treeview.Treeview", borderwidth=1)  # Esto añade bordes alrededor de cada celda
        
        # Crear barras de desplazamiento
        y_scroll = ttk.Scrollbar(self.medicion_tab, orient="vertical", command=self.tree.yview)
        y_scroll.grid(row=4, column=21, sticky='ns')
        self.tree.configure(yscrollcommand=y_scroll.set)
        
        
        #Etiquetas del contador
        self.paquetes_enviados_label = tk.Label(self.medicion_tab, text="Envíos exitosos: 0", font=("verdama", 10), fg='green')
        self.paquetes_enviados_label.grid(row=7, column=1, columnspan=2)

        self.paquetes_no_enviados_label = tk.Label(self.medicion_tab, text="Envíos fallidos: 0", font=("Verdana", 10), fg='red')
        self.paquetes_no_enviados_label.grid(row=7,column=3, columnspan=2)

    def create_configuracion_tab(self):
        self.url_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.machine_name_var = tk.StringVar()

        url_label = tk.Label(self.configuracion_tab, text="URL del Web Service:")
        url_label.grid(row=0, column=0)
        url_entry = tk.Entry(self.configuracion_tab, textvariable=self.url_var)
        url_entry.grid(row=0, column=1)

        username_label = tk.Label(self.configuracion_tab, text="Usuario:")
        username_label.grid(row=1, column=0)
        username_entry = tk.Entry(self.configuracion_tab, textvariable=self.username_var)
        username_entry.grid(row=1, column=1)

        password_label = tk.Label(self.configuracion_tab, text="Contraseña:")
        password_label.grid(row=2, column=0)
        password_entry = tk.Entry(self.configuracion_tab, textvariable=self.password_var, show="*")
        password_entry.grid(row=2, column=1)

        machine_name_label = tk.Label(self.configuracion_tab, text="Nombre de la Máquina:")
        machine_name_label.grid(row=3, column=0)
        machine_name_entry = tk.Entry(self.configuracion_tab, textvariable=self.machine_name_var)
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
    root.resizable(False,False)
    app = WebServiceApp(root)
    root.mainloop()