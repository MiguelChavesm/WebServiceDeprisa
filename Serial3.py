import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import json
import datetime

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
        
        self.listar_puertos()
        puertos_disponibles = [p for p in self.puertos_combobox['values'] if p]
        if len(puertos_disponibles) == 1:
            self.puertos_combobox.set(puertos_disponibles[0])
            self.abrir_puerto()

    def create_medicion_tab(self):
        ttk.Label(self.medicion_tab, text="SKU:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.sku_entry = ttk.Entry(self.medicion_tab)
        self.sku_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Largo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.largo_entry = ttk.Entry(self.medicion_tab)
        self.largo_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Ancho:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ancho_entry = ttk.Entry(self.medicion_tab)
        self.ancho_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Alto:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.alto_entry = ttk.Entry(self.medicion_tab)
        self.alto_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.medicion_tab, text="Peso:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.peso_entry = ttk.Entry(self.medicion_tab)
        self.peso_entry.grid(row=4, column=1, padx=10, pady=5)

        self.medir_button = ttk.Button(self.medicion_tab, text="Medir", command=self.enviar_trama)
        self.medir_button.grid(row=5, columnspan=2, padx=10, pady=5)

        
    def create_configuracion_tab(self):
        self.label = ttk.Label(self.configuracion_tab, text="Puertos COM disponibles:")
        self.label.pack(padx=10, pady=10)

        self.puertos_combobox = ttk.Combobox(self.configuracion_tab)
        self.puertos_combobox.pack(padx=10, pady=5)

        self.actualizar_puertos_button = ttk.Button(self.configuracion_tab, text="Actualizar puertos", command=self.listar_puertos)
        self.actualizar_puertos_button.pack(padx=10, pady=5)

        self.abrir_puerto_button = ttk.Button(self.configuracion_tab, text="Abrir Puerto", command=self.abrir_puerto)
        self.abrir_puerto_button.pack(padx=10, pady=5)

        self.cerrar_puerto_button = ttk.Button(self.configuracion_tab, text="Cerrar Puerto", command=self.cerrar_puerto)
        self.cerrar_puerto_button.pack(padx=10, pady=5)
        self.cerrar_puerto_button.configure(state="disabled")



        
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
            self.puertos_combobox.configure(state="disabled")  # Bloquear el combobox
            self.abrir_puerto_button.configure(state="disabled")
            self.cerrar_puerto_button.configure(state="enabled")
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

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialInterface(root)
    root.mainloop()