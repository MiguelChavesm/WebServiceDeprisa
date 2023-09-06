import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import requests
import json
import datetime
import configparser
import uuid
#import winreg
#import time


class SerialInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Comunicación WebService Deprisa")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
        self.medicion_tab = ttk.Frame(self.notebook)
        self.configuracion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.medicion_tab, text="Medición")
        self.notebook.add(self.configuracion_tab, text="Configuración")
        
        self.create_medicion_tab()
        self.create_configuracion_tab()
        self.cargar_configuracion()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
                
        self.paquetes_enviados = 0
        self.paquetes_no_enviados = 0
        
        self.tiempo_espera = 2  # Tiempo en segundos para esperar la recepción de datos
        self.datos_recibidos = False  # Agrega esta línea para inicializar la variable

        self.notebook.bind("<<NotebookTabChanged>>", self.verificar_contraseña)

        self.verificar_mac()
        
        #print(self.obtener_mac())

#VERIFICACIÓN DE MAC
    def get_mac_address(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        formatted_mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)])
        return formatted_mac

        
    def verificar_mac(self):
        direcciones_mac_permitidas = ["30:05:05:b8:bb:31", "00:11:22:33:44:55", "30:05:05:b8:bb:31"]  # Lista de direcciones MAC permitidas  # Reemplaza con la MAC permitida
        mac_actual = self.get_mac_address()  # Usa el método de obtener_mac() definido
        if mac_actual not in direcciones_mac_permitidas:
            self.cerrar_puerto()
            self.mostrar_error_y_salir()  # Llama a la función para mostrar un mensaje de error y cerrar el programa

    
        # Agrega esta función para mostrar un mensaje de error y cerrar el programa.
    def mostrar_error_y_salir(self):
        mensaje = "Este software solo puede ejecutarse en una computadora autorizada."
        messagebox.showerror("Error", mensaje)
        root.destroy()  # Cierra la aplicación

#CREACIÓN DE VENTANA DE MEDICIÓN
    def create_medicion_tab(self):
        
        self.sku_var = tk.StringVar()
        self.length_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.response_text = tk.StringVar()
        root.iconbitmap('montra.ico')

        ttk.Label(self.medicion_tab, text="SKU:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.sku_entry = ttk.Entry(self.medicion_tab, textvariable=self.sku_var)
        self.sku_entry.grid(row=0, column=1, padx=10, pady=5)
        self.sku_entry.focus_set()
        self.medir_button = ttk.Button(self.medicion_tab, text="Medir", command=self.enviar_trama)
        self.medir_button.grid(row=1, columnspan=2, padx=10, pady=5)
        
        self.send_button = ttk.Button(self.medicion_tab, text="Enviar", command=self.send_data)
        self.send_button.grid(row=2, columnspan=2, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Largo:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.largo_entry = ttk.Entry(self.medicion_tab, textvariable=self.length_var)
        self.largo_entry.grid(row=0, column=3, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Ancho:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.ancho_entry = ttk.Entry(self.medicion_tab, textvariable=self.width_var)
        self.ancho_entry.grid(row=1, column=3, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Alto:").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.alto_entry = ttk.Entry(self.medicion_tab, textvariable=self.height_var)
        self.alto_entry.grid(row=2, column=3, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Peso:").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.peso_entry = ttk.Entry(self.medicion_tab, textvariable=self.weight_var)
        self.peso_entry.grid(row=3, column=3, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Respuesta:").grid(row=9, columnspan=2, padx=10, pady=5)
        self.response_entry = ttk.Entry(self.medicion_tab, textvariable=self.response_text, state="readonly")
        self.response_entry.grid(row=7, columnspan=2, padx=10, pady=5)
        
        #Etiquetas del contador
        self.paquetes_enviados_label = tk.Label(self.medicion_tab, text="Envíos exitosos: 0", font=("verdama", 10))
        self.paquetes_enviados_label.grid(row=3, column=1)

        self.paquetes_no_enviados_label = tk.Label(self.medicion_tab, text="Envíos fallidos: 0", font=("Verdana", 10))
        self.paquetes_no_enviados_label.grid(row=4,column=1)
        
        self.medir_button.bind('<Return>', self.on_enter_press)
        self.medir_button.bind('<FocusIn>', self.on_button_focus_in)
        self.medir_button.bind('<FocusOut>', self.on_button_focus_out)
        
        self.send_button.bind('<Return>', self.on_enter_press)
        self.send_button.bind('<FocusIn>', self.on_sendbutton_focus_in)
        self.send_button.bind('<FocusOut>', self.on_sendbutton_focus_out)
        
        self.sku_entry.bind("<Return>", self.cambiar_foco_a_medir)

    #CREACIÓN DE COMANDOS PARA FOCUS Y ACCIONES CON ENTER
    # Evento de ENTER en SKU
    def cambiar_foco_a_medir(self, event): 
        self.medir_button.focus_set()
    
    #Evento de enter al tener focus en "Medir" o "Enviar"
    def on_enter_press(self, event):
        if self.is_medirbutton_focused:
            self.enviar_trama()
        elif self.is_sendbutton_focused:
            self.send_data()
            
    #Confirmar cursor en boton "medir" con variable en TRUE
    def on_button_focus_in(self, event): 
        self.is_medirbutton_focused = True 
    
    #Confirmar cursor en boton "medir" con variable en FALSE
    def on_button_focus_out(self, event): 
        self.is_medirbutton_focused = False    
    
    #Confirmar cursor en boton "Enviar" con variable en TRUE
    def on_sendbutton_focus_in(self, event):
        self.is_sendbutton_focused = True
    
    #Confirmar cursor en boton "Enviar" con variable en TRUE
    def on_sendbutton_focus_out(self, event):
        self.is_sendbutton_focused = False


#CREACIÓN DE VENTANA DE CONFIGURACIÓN
    def create_configuracion_tab(self):

        self.url_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.machine_name_var = tk.StringVar()

        ttk.Label(self.configuracion_tab, text="URL del Web Service:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        url_entry = ttk.Entry(self.configuracion_tab, textvariable=self.url_var, show="*")
        url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.configuracion_tab, text="Usuario:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        username_entry = ttk.Entry(self.configuracion_tab, textvariable=self.username_var, show="*")
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

        self.actualizar_puertos_button = ttk.Button(self.configuracion_tab, text="Actualizar", command=self.listar_puertos)
        self.actualizar_puertos_button.grid(row=4, column=2, padx=10, pady=5)

        self.abrir_puerto_button = ttk.Button(self.configuracion_tab, text="Abrir Puerto", command=self.abrir_puerto)
        self.abrir_puerto_button.grid(row=5, column=1, padx=10, pady=5)

        self.cerrar_puerto_button = ttk.Button(self.configuracion_tab, text="Cerrar Puerto", command=self.cerrar_puerto)
        self.cerrar_puerto_button.grid(row=6, column=1, padx=10, pady=5)
        self.cerrar_puerto_button.configure(state="disabled")
        
        self.guardar_config_button = ttk.Button(self.configuracion_tab, text="Guardar Configuración", command=self.guardar_configuracion)
        self.guardar_config_button.grid(row=7, columnspan=2, padx=10, pady=5)
        
        # Botón para cambiar la contraseña
        cambiar_contraseña_button = ttk.Button(self.configuracion_tab, text="Cambiar Contraseña", command=self.abrir_ventana_cambio_contraseña)
        cambiar_contraseña_button.grid(row=8, columnspan=2, padx=10, pady=5)
    
#CONFIGURACIÓN DE PUERTOS
    #Listar los puertos disponibles
    def listar_puertos(self):
        puertos = [puerto.device for puerto in serial.tools.list_ports.comports()]
        self.puertos_combobox['values'] = puertos
    
    #Abrir puerto seleccionado
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
    
    #Cerrar el puerto
    def cerrar_puerto(self): 
        if hasattr(self, 'puerto_serial') and self.puerto_serial.is_open:
            self.puerto_serial.close()
            self.puerto_serial = None
            self.puertos_combobox.configure(state="readonly")  # Desbloquear el combobox
            self.abrir_puerto_button.configure(state="enabled")
            self.cerrar_puerto_button.configure(state="disabled")

#CONFIGURACIÓN DE ARCHIVO.INI PARA PRECARGAR Y GUARDAR LOS DATOS
    #Precargar configuración en archivo.ini
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
            self.contraseña_actual = config['Configuracion'].get('contraseña_adicional', 'MONTRA101') # Obtener la contraseña
            self.abrir_puerto()

    #Guardar configuración en archivo.ini
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
        config['Configuracion']['contraseña_adicional'] = self.contraseña_actual
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
#CONFIGURACIÓN DE CONTRASEÑA PARA ACCESO A VENTANA CONFIGURACIÓN
    #Verificar contraseña guardada con contraseña ingresada al cambiar de pestaña. Contraseña inicial: MONTRA101
    def verificar_contraseña(self, event):
        if self.notebook.tab(self.notebook.select(), "text") == "Configuración":
            password = simpledialog.askstring("Contraseña", "Ingrese la contraseña:", show="*")
            if password != self.contraseña_actual:  # Usar la contraseña actual almacenada
                self.notebook.select(self.medicion_tab)
                messagebox.showerror("Acceso denegado", "La contraseña ingresada es incorrecta. Acceso denegado a la pestaña de configuración.")

    #Creación de ventana para cambiar contraseña.
    def abrir_ventana_cambio_contraseña(self):
        # Ventana emergente para cambiar la contraseña
        cambio_contraseña_window = tk.Toplevel(self.root)
        cambio_contraseña_window.title("Cambiar Contraseña")

        ttk.Label(cambio_contraseña_window, text="Contraseña Actual:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        contraseña_actual_entry = ttk.Entry(cambio_contraseña_window, show="*")
        contraseña_actual_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(cambio_contraseña_window, text="Nueva Contraseña:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        nueva_contraseña_entry = ttk.Entry(cambio_contraseña_window, show="*")
        nueva_contraseña_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(cambio_contraseña_window, text="Guardar", command=lambda: self.guardar_nueva_contraseña(contraseña_actual_entry.get(), nueva_contraseña_entry.get(), cambio_contraseña_window)).grid(row=2, columnspan=2, padx=10, pady=5)

    #Acción ejecutada por el boton para guardar la nueva contraseña en el archivo.ini
    def guardar_nueva_contraseña(self, contraseña_actual, nueva_contraseña, window):
        if contraseña_actual != self.contraseña_actual:
            messagebox.showerror("Error", "La contraseña actual es incorrecta.")
        elif nueva_contraseña:
                self.contraseña_actual = nueva_contraseña
                messagebox.showinfo("Contraseña Cambiada", "La contraseña ha sido cambiada con éxito.")
                window.destroy()
                self.guardar_configuracion()  # Guardar la nueva contraseña en el archivo config.ini
    
    #Configuración para cerrar el puerto y guardar la configuración al cerrar la app.
    def cerrar_aplicacion(self):
        if hasattr(self, 'puerto_serial') and self.puerto_serial and self.puerto_serial.is_open:
            self.cerrar_puerto()  # Cerrar el puerto si está abierto
        self.guardar_configuracion()  # Guardar la configuración antes de salir
        self.root.destroy()  # Cerrar la aplicación

#CONFIGURACIÓN PARA RECEPCIÓN PEDIR Y RECIBIR DATOS DE CUBISCAN
    #Solicitar medición
    def enviar_trama(self):
        self.iniciar_espera_datos()
        if hasattr(self, 'puerto_serial') and self.puerto_serial.is_open:
            #self.iniciar_espera_datos()  # Iniciar la espera de datos
            trama = b'\x02M\x03\r\n'  # Trama: <STX>M<ETX><CR><LF>
            enviar_thread = threading.Thread(target=self.enviar_trama_thread, args=(trama,))
            enviar_thread.start()
    
    #Metodo independiente para solicitar medición
    def enviar_trama_thread(self, trama):
        try:
            self.puerto_serial.write(trama)
        except Exception as e:
            print("Error al enviar la trama:", e)  

    #Recepción de datos y estructurar en campos:
    def leer_datos(self):
        while hasattr(self, 'puerto_serial') and self.puerto_serial and self.puerto_serial.is_open:
            try:
                dato = self.puerto_serial.readline().decode('utf-8')
                if dato:
                    self.datos_recibidos = True  # Datos recibidos, detener temporizador
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
                    self.verificar_datos_cubiscan()
            except:
                pass
    
    #Confirmación que ningun dato recibido sea cero.
    def verificar_datos_cubiscan(self):
        # Verificar si alguno de los campos está en 0
        if self.sku_var.get() <= '0' or self.length_var.get() <= '0' or self.width_var.get() <= '0' or self.weight_var.get() <= '0' and self.length_var.get()!= "" or self.width_var.get() == "" or self.height_var.get() == "" or self.weight_var.get() == "":
            self.medir_button.focus_set()
            messagebox.showerror("Error", "Los campos SKU, Largo, Ancho y Alto no pueden ser 0 o estar vacíos.")
            return  # No se envía la información si algún campo es 0
        else:
            self.send_button.focus_set()

    # Metodo para iniciar espera de datos
    def iniciar_espera_datos(self):
        self.datos_recibidos = False
        self.timer = threading.Timer(self.tiempo_espera, self.mostrar_error_sin_datos)
        self.timer.start()

    # Método para mostrar un mensaje de error si no se reciben datos
    def mostrar_error_sin_datos(self):
        if not self.datos_recibidos:
            messagebox.showerror("Error", "No hay comunicación con la CubiScan, revise cables y conexiones.")

    # Agrega este método para detener el temporizador
    def detener_espera_datos(self):
        if hasattr(self, 'timer') or self.timer.is_alive():
            self.timer.cancel()
    

#CONFIGURACIÓN ENVÍO JSON
    #Configuración del envío de estructura JSON
    def send_data(self):
        # Obtener los valores de los campos
        sku = self.sku_var.get()
        largo = self.length_var.get()
        ancho = self.width_var.get()
        alto = self.height_var.get()
        peso = self.weight_var.get()

        # Construir el JSON con los datos ingresados
        data = {
            "machine_pid": self.machine_name_var.get(),
            "code": self.sku_var.get(),
            "measure_date": datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S"),
            "length": self.length_var.get(),
            "width": self.width_var.get(),
            "height": self.height_var.get(),
            "weight": self.weight_var.get(),
            "unit_type": "cm"
        }
        print(data)
        # Verificar si alguno de los campos está en 0
        if sku <= '0' or largo <= '0' or ancho <= '0' or alto <= '0' or peso <= '0':
            self.send_button.focus_set()
            messagebox.showerror("Error", "Los campos SKU, Largo, Ancho y Alto no pueden ser 0 o estar vacíos.")
            return  # No se envía la información si algún campo es 0
        elif sku == "" or largo == "" or alto == "" or ancho == "" or peso=="":
            self.send_button.focus_set()

        # Obtener los valores de los campos
        sku = self.sku_var.get()
        largo = self.length_var.get()
        ancho = self.width_var.get()
        alto = self.height_var.get()
        

    # Verificar si alguno de los campos está en 0
        if sku <= '0' or largo <= '0' or ancho <= '0' or alto <= '0' and sku == "" or largo == "" or alto == "" or ancho == "":

            messagebox.showerror("Error", "Los campos SKU, Largo, Ancho y Alto no pueden ser 0 o estar vacíos.")
            return  # No se envía la información si algún campo es 0
        else:
            self.sku_entry.focus_set()
            

        # Realizar la solicitud POST al WebService
        url = self.url_var.get()
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=(self.username_var.get(), self.password_var.get()))

        #contador
        if response.status_code == 200:
            self.paquetes_enviados += 1
            
        else:
            self.paquetes_no_enviados += 1
        # Actualizar la respuesta en la interfaz
        self.response_text.set(response.text)
        #actualizar contadores
        self.update_contadores()
        self.sku_var.set("")     # Borra el contenido del campo SKU
        self.length_var.set("")  # Borra el contenido del campo Largo
        self.width_var.set("")   # Borra el contenido del campo Ancho
        self.height_var.set("")  # Borra el contenido del campo Alto
        self.weight_var.set("")  # Borra el contenido del campo Peso

    #Conteos exitoso y fallidos de envío
    def update_contadores(self):
        self.paquetes_enviados_label.config(text=f"Envíos exitosos: {self.paquetes_enviados}")
        self.paquetes_no_enviados_label.config(text=f"Envíos fallidos: {self.paquetes_no_enviados}")


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False,False)
    app = SerialInterface(root)
    root.mainloop()

#Comentario adicional