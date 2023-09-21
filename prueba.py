import tkinter as tk

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        
        # Botón para abrir la ventana emergente de inicio de sesión
        self.btn_abrir_login = tk.Button(self, text="Abrir Login", command=self.abrir_ventana_login)
        self.btn_abrir_login.pack(pady=20)
    
    def abrir_ventana_login(self):
        # Crear la ventana emergente de inicio de sesión
        ventana_login = VentanaLogin(self)
        
        # Bloquear la ventana principal
        self.wait_window(ventana_login)

class VentanaLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inicio de Sesión")
        
        # Agregar contenido de inicio de sesión aquí
        # ...
        
        # Ejemplo de un botón para cerrar la ventana emergente
        self.btn_cerrar = tk.Button(self, text="Cerrar", command=self.cerrar_ventana)
        self.btn_cerrar.pack(pady=10)
        
        # Establecer el "grabo" en la ventana emergente
        self.grab_set()
    
    def cerrar_ventana(self):
        # Cerrar la ventana emergente
        self.destroy()

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
