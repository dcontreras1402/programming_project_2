# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Representa un cliente que compra entradas en el cine.

class Cliente:
    def __init__(self, nombre, cedula, correo):
        self.nombre = nombre      # Nombre del cliente
        self.cedula = cedula      # Cédula o documento de identidad
        self.correo = correo      # Correo electrónico

    def mostrar_info(self):
        """Muestra la información del cliente"""
        print(f"Nombre: {self.nombre}")
        print(f"Cédula: {self.cedula}")
        print(f"Correo: {self.correo}")


# ---------------- PRUEBA RÁPIDA ----------------
if __name__ == "__main__":
    cliente1 = Cliente("Juan Pérez", "123456789", "juan@mail.com")
    cliente1.mostrar_info()
