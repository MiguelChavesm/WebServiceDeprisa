import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import requests
import json
import datetime
import configparser

paquetes_enviados = 0
paquetes_no_enviados = 0

class SerialInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Comunicación Serial")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
        self.medicion_tab = ttk.Frame(self.notebook)
        self.configuracion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.medicion_tab, text="Medición")
        self.notebook.add(self.configuracion_tab, text="Configuración")
        
        self.create_medicion_tab()
        self.create_configuracion_tab()
        
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        self.cargar_configuracion()
        
        self.listar_puertos()
        puertos_disponibles = [p for p in self.puertos_combobox['values'] if p]
        if len(puertos_disponibles) == 1:
            self.puertos_combobox.set(puertos_disponibles[0])
            self.abrir_puerto()
            
        # Añadir la protección por contraseña a la pestaña de configuración
        self.notebook.bind("<<NotebookTabChanged>>", self.verificar_contraseña)

    def verificar_contraseña(self, event):
        if self.notebook.tab(self.notebook.select(), "text") == "Configuración":
            password = simpledialog.askstring("Contraseña", "Ingrese la contraseña:")
            if password != "MONTRA101":  # Reemplaza "tu_contraseña_aqui" con la contraseña real
                self.notebook.select(self.medicion_tab)
                self.show_configuracion_message()
    
    def show_configuracion_message(self):
        messagebox.showerror("Acceso denegado", "La contraseña ingresada es incorrecta. Acceso denegado a la pestaña de configuración.")
    
    def cerrar_aplicacion(self):
        if hasattr(self, 'puerto_serial') and self.puerto_serial.is_open:
            self.cerrar_puerto()  # Cerrar el puerto si está abierto
        self.guardar_configuracion()  # Guardar la configuración antes de salir
        self.root.destroy()  # Cerrar la aplicación

    def cargar_configuracion(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'Configuracion' in config:
            self.url_var.set(config['Configuracion'].get('url', ''))
            self.username_var.set(config['Configuracion'].get('username', ''))
            self.password_var.set(config['Configuracion'].get('password', ''))
            self.machine_name_var.set(config['Configuracion'].get('machine_name', ''))
            # Cargar y establecer el último puerto en el combobox
            ultimo_puerto = config['Configuracion'].get('ultimo_puerto', '')
            self.puertos_combobox.set(ultimo_puerto)
            self.abrir_puerto()
            
            
    def guardar_configuracion(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Guardar los valores de configuración
        config['Configuracion']['url'] = self.url_var.get()
        config['Configuracion']['username'] = self.username_var.get()
        config['Configuracion']['password'] = self.password_var.get()
        config['Configuracion']['machine_name'] = self.machine_name_var.get()
        # Obtener el último puerto seleccionado del combobox
        ultimo_puerto = self.puertos_combobox.get()
        config['Configuracion']['ultimo_puerto'] = ultimo_puerto
        
            
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


    def create_medicion_tab(self):
        
        self.sku_var = tk.StringVar()
        self.length_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.response_text = tk.StringVar()

        #Etiquetas del contador
        self.paquetes_enviados_label = tk.Label(
            self.medicion_tab, text="paquetes enviados: 0", font=("verdama", 10)
        )
        self.paquetes_enviados_label.grid(row=0, column=2)

        self.paquetes_no_enviados_label = tk.Label(
            self.medicion_tab, text="paquetes con mala respuesta: 0", font=("Verdana", 10)
        )
        self.paquetes_no_enviados_label.grid(row=1,column=2)

        self.paquetes_no_enviados_label.grid(row=1, column=2)        
        ttk.Label(self.medicion_tab, text="SKU:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.sku_entry = ttk.Entry(self.medicion_tab, textvariable=self.sku_var)
        self.sku_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Largo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.largo_entry = ttk.Entry(self.medicion_tab, textvariable=self.length_var)
        self.largo_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Ancho:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ancho_entry = ttk.Entry(self.medicion_tab, textvariable=self.width_var)
        self.ancho_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Alto:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.alto_entry = ttk.Entry(self.medicion_tab, textvariable=self.height_var)
        self.alto_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Peso:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.peso_entry = ttk.Entry(self.medicion_tab, textvariable=self.weight_var)
        self.peso_entry.grid(row=4, column=1, padx=10, pady=5)

        self.medir_button = ttk.Button(self.medicion_tab, text="Medir", command=self.enviar_trama)
        self.medir_button.grid(row=5, columnspan=2, padx=10, pady=5)
        
        self.send_button = ttk.Button(self.medicion_tab, text="Enviar", command=self.send_data)
        self.send_button.grid(row=6, columnspan=2, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Respuesta:").grid(row=7, columnspan=2, padx=10, pady=5)
        self.response_entry = ttk.Entry(self.medicion_tab, textvariable=self.response_text, state="readonly")
        self.response_entry.grid(row=7, columnspan=2, padx=10, pady=5)
        
        
    def update_contadores(self):
        self.paquetes_enviados_label.config(text=f"paquetes enviados: {paquetes_enviados}")
        self.paquetes_no_enviados_label.config(text=f"paquetes con mala respuesta: {paquetes_no_enviados}")


    def create_configuracion_tab(self):
        self.url_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.machine_name_var = tk.StringVar()

        ttk.Label(self.configuracion_tab, text="URL del Web Service:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        url_entry = ttk.Entry(self.configuracion_tab, textvariable=self.url_var)
        url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.configuracion_tab, text="Usuario:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        username_entry = ttk.Entry(self.configuracion_tab, textvariable=self.username_var)
        username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.configuracion_tab, text="Contraseña:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        password_entry = ttk.Entry(self.configuracion_tab, textvariable=self.password_var, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.configuracion_tab, text="Nombre de la Máquina:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        machine_name_entry = ttk.Entry(self.configuracion_tab, textvariable=self.machine_name_var)
        machine_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(self.configuracion_tab, text="Puertos COM disponibles:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.puertos_combobox = ttk.Combobox(self.configuracion_tab)
        self.puertos_combobox.grid(row=4, column=1, padx=10, pady=5)

        self.actualizar_puertos_button = ttk.Button(self.configuracion_tab, text="Actualizar puertos", command=self.listar_puertos)
        self.actualizar_puertos_button.grid(row=4, column=2, padx=10, pady=5)

        self.abrir_puerto_button = ttk.Button(self.configuracion_tab, text="Abrir Puerto", command=self.abrir_puerto)
        self.abrir_puerto_button.grid(row=5, column=1, padx=10, pady=5)

        self.cerrar_puerto_button = ttk.Button(self.configuracion_tab, text="Cerrar Puerto", command=self.cerrar_puerto)
        self.cerrar_puerto_button.grid(row=6, column=1, padx=10, pady=5)
        self.cerrar_puerto_button.configure(state="disabled")
        
        self.guardar_config_button = ttk.Button(self.configuracion_tab, text="Guardar Configuración", command=self.guardar_configuracion)
        self.guardar_config_button.grid(row=7, columnspan=2, padx=10, pady=5)
    
    def send_data():
        global paquetes_enviados
        global paquetes_no_enviados
        
    def on_enter_press(self, event):
        if self.is_button_focused:
            self.enviar_trama()

    def on_button_focus_in(self, event):
        self.is_button_focused = True

    def on_button_focus_out(self, event):
        self.is_button_focused = False

    def listar_puertos(self):
        puertos = [puerto.device for puerto in serial.tools.list_ports.comports()]
        self.puertos_combobox['values'] = puertos

    def abrir_puerto(self):
        puerto_seleccionado = self.puertos_combobox.get()
        try:
            self.puerto_serial = serial.Serial(puerto_seleccionado, baudrate=9600)
            self.puertos_combobox.configure(state="disabled")
            self.abrir_puerto_button.configure(state="disabled")
            self.cerrar_puerto_button.configure(state="enabled")

            # Guardar el último puerto en el archivo config.ini
            self.guardar_configuracion()
            
            self.data_thread = threading.Thread(target=self.leer_datos)
            self.data_thread.start()
        except Exception as e:
            mensaje = f"Error al abrir el puerto: {e}"
            messagebox.showerror("Error", mensaje)

    def cerrar_puerto(self):
        if hasattr(self, 'puerto_serial') and self.puerto_serial.is_open:
            self.puerto_serial.close()
            self.puerto_serial = None
            self.puertos_combobox.configure(state="readonly")  # Desbloquear el combobox
            self.abrir_puerto_button.configure(state="enabled")
            self.cerrar_puerto_button.configure(state="disabled")



    def leer_datos(self):
        while hasattr(self, 'puerto_serial') and self.puerto_serial and self.puerto_serial.is_open:
            try:
                dato = self.puerto_serial.readline().decode('utf-8')
                #self.datos_received_text.insert(tk.END, dato)
                #self.datos_received_text.see(tk.END)  # Hacer scroll para mostrar los nuevos datos
                
                # Procesar la trama recibida para obtener los valores de Largo, Ancho, Alto y Peso
                if "\x02" in dato and "\x03" in dato:
                    trama = dato.split("\x02")[1].split("\x03")[0]
                    valores = trama.split(",")
                    
                    for valor in valores:
                        if valor.startswith("L"):
                            largo = valor.split("L")[1]
                            largo = round(float(largo))  # Convertir a número, redondear
                            self.largo_entry.delete(0, tk.END)
                            self.largo_entry.insert(0, str(largo))
                        elif valor.startswith("W"):
                            ancho = valor.split("W")[1]
                            ancho = round(float(ancho))  # Convertir a número, redondear
                            self.ancho_entry.delete(0, tk.END)
                            self.ancho_entry.insert(0, str(ancho))
                        elif valor.startswith("H"):
                            alto = valor.split("H")[1]
                            alto = round(float(alto))  # Convertir a número, redondear
                            self.alto_entry.delete(0, tk.END)
                            self.alto_entry.insert(0, str(alto))
                        elif valor.startswith("K"):
                            peso = valor.split("K")[1]
                            peso = float(peso)
                            self.peso_entry.delete(0, tk.END)
                            self.peso_entry.insert(0, peso)
            except:
                pass

    def enviar_trama(self):
        if hasattr(self, 'puerto_serial') and self.puerto_serial.is_open:
            trama = b'\x02M\x03\r\n'  # Trama: <STX>M<ETX><CR><LF>
            enviar_thread = threading.Thread(target=self.enviar_trama_thread, args=(trama,))
            enviar_thread.start()

    def enviar_trama_thread(self, trama):
        try:
            self.puerto_serial.write(trama)
        except Exception as e:
            print("Error al enviar la trama:", e)  

        
    
    def send_data(self):
        global paquetes_enviados
        global paquetes_no_enviados

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

#contador
        if response.status_code == 200:
            paquetes_enviados += 1
        else:
            paquetes_no_enviados += 1

        # Actualizar la respuesta en la interfaz
        self.response_text.set(response.text)
        #actualizar contadores
        self.update_contadores()
            

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialInterface(root)
    root.mainloop()