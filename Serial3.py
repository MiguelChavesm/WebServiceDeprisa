import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class SerialInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Comunicación Serial")
        
        self.label = ttk.Label(root, text="Puertos COM disponibles:")
        self.label.pack(padx=10, pady=10)

        self.puertos_combobox = ttk.Combobox(root)
        self.puertos_combobox.pack(padx=10, pady=5)

        self.actualizar_puertos_button = ttk.Button(root, text="Actualizar puertos", command=self.listar_puertos)
        self.actualizar_puertos_button.pack(padx=10, pady=5)

        self.abrir_puerto_button = ttk.Button(root, text="Abrir Puerto", command=self.abrir_puerto)
        self.abrir_puerto_button.pack(padx=10, pady=5)

        self.cerrar_puerto_button = ttk.Button(root, text="Cerrar Puerto", command=self.cerrar_puerto)
        self.cerrar_puerto_button.pack(padx=10, pady=5)
        self.cerrar_puerto_button.configure(state="disabled")
        
        self.medir_button = ttk.Button(root, text="Medir", command=self.enviar_trama)
        self.medir_button.pack(padx=10, pady=5)

        self.medir_button.bind('<Return>', self.on_enter_press)
        self.medir_button.bind('<FocusIn>', self.on_button_focus_in)
        self.medir_button.bind('<FocusOut>', self.on_button_focus_out)

        self.is_button_focused = False
        
        self.datos_received_text = tk.Text(root)
        self.datos_received_text.pack(padx=10, pady=10)
        
        self.listar_puertos()
        puertos_disponibles = [p for p in self.puertos_combobox['values'] if p]  # Filtrar puertos no vacíos
        if len(puertos_disponibles) == 1:  # Si solo hay un puerto no vacío
            self.puertos_combobox.set(puertos_disponibles[0])  # Establecer el único puerto automáticamente
            self.abrir_puerto()  # Abrir automáticamente el puerto

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
            self.abrir_puerto_button.configure(state="disabled")
            self.cerrar_puerto_button.configure(state="enabled")
            self.data_thread = threading.Thread(target=self.leer_datos)
            self.data_thread.start()
        except Exception as e:
            #mensaje = "Error al abrir el puerto, no se encuentra o ya está abierto en otro programa"
            mensaje = f"Error al abrir el puerto: {e}"
            messagebox.showerror("Error", mensaje)

            messagebox.showerror("Error", mensaje)


    def cerrar_puerto(self):
        if hasattr(self, 'puerto_serial') and self.puerto_serial.is_open:
            self.puerto_serial.close()
            self.puerto_serial = None
            self.abrir_puerto_button.configure(state="enabled")
            self.cerrar_puerto_button.configure(state="disabled")
    
    
    def leer_datos(self):
        while hasattr(self, 'puerto_serial') and self.puerto_serial and self.puerto_serial.is_open:
            try:
                dato = self.puerto_serial.readline().decode('utf-8')
                self.datos_received_text.insert(tk.END, dato)
                self.datos_received_text.see(tk.END)  # Hacer scroll para mostrar los nuevos datos
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