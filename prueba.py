if dato:
    trama = dato.split("\x02")[1].split("\x03")[0]
    valores = trama.split(",")

    # Obtener los valores en las posiciones 4 y 7
    valor_posicion_4 = valores[3].strip()
    valor_posicion_7 = valores[6].strip()

    if valor_posicion_4 == "M" and valor_posicion_7 == "E":
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
                peso = float(peso)*0.4536
                self.peso_entry.delete(0, tk.END)
                self.peso_entry.insert(0, peso)
        print("Condición 1: Valor en posición 4 es 'M' y valor en posición 7 es 'E'")
    elif valor_posicion_4 == "E" and valor_posicion_7 == "M":
        for valor in valores:
            if valor.startswith("L"):
                largo = valor.split("L")[1]
                largo = round(float(largo)*2.54)
                self.largo_entry.delete(0, tk.END)
                self.largo_entry.insert(0, str(largo))# Convertir a número, redondear
            elif valor.startswith("W"):
                ancho = valor.split("W")[1]
                ancho = round(float(ancho)*2.54)  # Convertir a número, redondear
                self.ancho_entry.delete(0, tk.END)
                self.ancho_entry.insert(0, str(ancho))
            elif valor.startswith("H"):
                alto = valor.split("H")[1]
                alto = round(float(alto)*2.54)  # Convertir a número, redondear
                self.alto_entry.delete(0, tk.END)
                self.alto_entry.insert(0, str(alto))
            elif valor.startswith("K"):
                peso = valor.split("K")[1]
                peso = float(peso)
                self.peso_entry.delete(0, tk.END)
                self.peso_entry.insert(0, peso)
        print("Condición 2: Valor en posición 4 es 'E' y valor en posición 7 es 'M'")
    elif valor_posicion_4 == "E" and valor_posicion_7 == "E":
        # Realizar acciones si ninguna de las condiciones se cumple
        for valor in valores:
            if valor.startswith("L"):
                largo = valor.split("L")[1]
                largo = round(float(largo)*2.54)  # Convertir a número, redondear
                self.largo_entry.delete(0, tk.END)
                self.largo_entry.insert(0, str(largo))
            elif valor.startswith("W"):
                ancho = valor.split("W")[1]
                ancho = round(float(ancho)*2.54)  # Convertir a número, redondear
                self.ancho_entry.delete(0, tk.END)
                self.ancho_entry.insert(0, str(ancho))
            elif valor.startswith("H"):
                alto = valor.split("H")[1]
                alto = round(float(alto)*2.54)  # Convertir a número, redondear
                self.alto_entry.delete(0, tk.END)
                self.alto_entry.insert(0, str(alto))
            elif valor.startswith("K"):
                peso = valor.split("K")[1]
                peso = float(peso*0.4536)
                self.peso_entry.delete(0, tk.END)
                self.peso_entry.insert(0, peso)
        print("Condición 3: Valor en posición 4 es 'E' y valor en posición 7 es 'E'")
    else: 
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
        print("Condición 4: Valor en posición 4 es 'M' y valor en posición 7 es 'M'")