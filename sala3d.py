# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Representa una sala de cine 3D con categoría general y preferencial.

from sala import Sala

class Sala3D(Sala):
    def __init__(self, nombre, total_general, total_preferencial, precio_general, precio_preferencial):
        super().__init__(nombre, total_general, precio_general)
        self.total_preferencial = total_preferencial
        self.precio_preferencial = precio_preferencial
        self.sillas_preferenciales = [True] * total_preferencial

    def mostrar_disponibles(self):
        disponibles_general = sum(self.sillas_disponibles)
        disponibles_preferencial = sum(self.sillas_preferenciales)
        print(f"Sala 3D '{self.nombre}':")
        print(f"  Generales disponibles: {disponibles_general}")
        print(f"  Preferenciales disponibles: {disponibles_preferencial}")

    def vender_boleta(self, tipo, cantidad):
        if tipo == "general":
            return super().vender_boleta(cantidad)
        elif tipo == "preferencial":
            if sum(self.sillas_preferenciales) >= cantidad:
                for i in range(cantidad):
                    index = self.sillas_preferenciales.index(True)
                    self.sillas_preferenciales[index] = False
                total = cantidad * self.precio_preferencial
                return f"Compra realizada: {cantidad} boletas preferenciales. Total a pagar: ${total}"
            else:
                return "❌ No hay suficientes sillas preferenciales disponibles."
        else:
            return "Tipo inválido. Use 'general' o 'preferencial'."

    def cancelar_compra(self, tipo, cantidad):
        if tipo == "general":
            return super().cancelar_compra(cantidad)
        elif tipo == "preferencial":
            liberadas = 0
            for i in range(len(self.sillas_preferenciales)):
                if not self.sillas_preferenciales[i]:
                    self.sillas_preferenciales[i] = True
                    liberadas += 1
                    if liberadas == cantidad:
                        break
            return f"Se cancelaron {cantidad} boletas preferenciales."
        else:
            return "Tipo inválido. Use 'general' o 'preferencial'."