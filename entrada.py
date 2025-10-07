# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Representa una entrada vendida a un cliente para una sala específica.
# Actualizado: Incluye ID único, registro de las sillas reservadas y es funcional con la persistencia.

class Entrada:
    # ATRIBUTO ESTÁTICO
    # Contador usado para asignar un ID único a cada compra.
    # Es crucial para la persistencia.
    compra_id_counter = 0

    def __init__(self, cliente, sala_nombre, categoria, cantidad, precio_total, sillas_reservadas):
        
        # 1. Asignar ID único y actualizar el contador
        Entrada.compra_id_counter += 1
        self.id = Entrada.compra_id_counter  # ID único de la compra

        # 2. Datos de la transacción
        self.cliente = cliente              # Objeto Cliente
        self.sala_nombre = sala_nombre      # Nombre de la sala
        self.categoria = categoria          # Categoría de la entrada (general/preferencial)
        self.cantidad = cantidad            # Cantidad de boletas
        self.precio_total = precio_total    # Total a pagar
        
        # 3. CRÍTICO PARA LA CANCELACIÓN
        # Almacena los IDs de las sillas que se reservaron. Ejemplo: [1, 2, 3]
        self.sillas_reservadas = sillas_reservadas 

    def mostrar_info(self):
        """Muestra los datos de la entrada, incluyendo el ID de compra y las sillas."""
        print(f"\n--- Detalle de Compra ID: {self.id} ---")
        print(f"Cliente: {self.cliente.nombre}")
        print(f"Sala: {self.sala_nombre}")
        print(f"Categoría: {self.categoria}")
        print(f"Cantidad: {self.cantidad}")
        print(f"Sillas Reservadas: {self.sillas_reservadas}")
        print(f"Total a pagar: ${self.precio_total:,.2f}")


# PRUEBA RÁPIDA
if __name__ == "__main__":
    from cliente import Cliente
    
    cliente1 = Cliente("Juan Pérez", "123456789", "juan@mail.com")
    
    # Simulación: se reservaron las sillas 10, 11 y 12
    sillas_ejemplo = [10, 11, 12]
    
    entrada1 = Entrada(
        cliente=cliente1, 
        sala_nombre="Sala 2D", 
        categoria="general", 
        cantidad=3, 
        precio_total=30000,
        sillas_reservadas=sillas_ejemplo
    )
    
    entrada1.mostrar_info()
    
    # Comprobar que el ID aumenta para la siguiente entrada
    entrada2 = Entrada(
        cliente=cliente1, 
        sala_nombre="Sala 3D", 
        categoria="preferencial", 
        cantidad=1, 
        precio_total=20000,
        sillas_reservadas=[20]
    )
    print(f"\nID de la segunda compra (debe ser 2): {entrada2.id}")