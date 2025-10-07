# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Representa una sala de cine con sillas generales, precios y métodos para vender, cancelar y mostrar disponibilidad.

class Sala:
    def __init__(self, nombre, sillas_totales, precio):
        self.nombre = nombre
        self.sillas_totales = sillas_totales
        self.precio = precio
        self.sillas_disponibles = [True] * sillas_totales  # True = disponible

    def mostrar_disponibles(self):
        disponibles = sum(self.sillas_disponibles)
        print(f"Sala '{self.nombre}' - Sillas disponibles: {disponibles}")

    def vender_boleta(self, cantidad):
        if sum(self.sillas_disponibles) >= cantidad:
            for i in range(cantidad):
                index = self.sillas_disponibles.index(True)
                self.sillas_disponibles[index] = False
            total = cantidad * self.precio
            return f"Compra realizada: {cantidad} boletas. Total a pagar: ${total}"
        else:
            return "❌ No hay suficientes sillas disponibles."

    def cancelar_compra(self, cantidad):
        liberadas = 0
        for i in range(len(self.sillas_disponibles)):
            if not self.sillas_disponibles[i]:
                self.sillas_disponibles[i] = True
                liberadas += 1
                if liberadas == cantidad:
                    break
        return f"Se cancelaron {cantidad} boletas."