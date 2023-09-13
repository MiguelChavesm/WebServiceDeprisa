import tkinter as tk

# Función para crear la ventana
def create_window():
    window = tk.Tk()
    window.geometry("400x300")  # Ajusta el tamaño de la ventana según tus necesidades

    # Contenido principal de la ventana
    main_content = tk.Label(window, text="Contenido principal de la ventana")
    main_content.grid(row=0, column=0, sticky="nsew")
    
    # Configurar el fondo del texto informativo
    info_text = tk.Label(window, text="Derechos reservados por XXX", fg="white", bg="blue")
    info_text.grid(row=1, column=0, sticky="ew")

    # Configurar las filas y columnas para que se expandan al cambiar el tamaño de la ventana
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    return window

if __name__ == "__main__":
    root = create_window()
    root.mainloop()
