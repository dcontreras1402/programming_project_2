# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Clase base para las salas de cine (2D), que maneja la ocupación de asientos.

class Sala:
    def __init__(self, nombre, sillas_totales, precio):
        self.nombre = nombre
        self.sillas_totales = sillas_totales
        self.precio = precio
        # Lista de booleanos: True = disponible. Indexada del 0 a N-1.
        self.sillas_disponibles = [True] * sillas_totales 

    def mostrar_disponibles(self):
        """
        Muestra el estado de la sala y el número de sillas disponibles.
        """
        disponibles = sum(self.sillas_disponibles)
        ocupadas = self.sillas_totales - disponibles
        print(f"Sala '{self.nombre}' | Total: {self.sillas_totales} | Disponibles: {disponibles} | Ocupadas: {ocupadas}")

    def vender_boleta(self, cantidad):
        """
        Reserva las primeras 'cantidad' de sillas disponibles (solo venta 2D/general).
        Devuelve el precio total (float) y los índices de las sillas reservadas (list).
        """
        disponibles = sum(self.sillas_disponibles)
        if disponibles < cantidad:
            raise ValueError(f"Solo quedan {disponibles} sillas disponibles en '{self.nombre}'.")
        
        sillas_reservadas = []
        conteo_reservas = 0
        
        # Recorremos para encontrar y reservar los asientos
        for i in range(self.sillas_totales):
            if self.sillas_disponibles[i]:
                self.sillas_disponibles[i] = False  # Ocupar la silla
                sillas_reservadas.append(i + 1)     # Guardar el ID de la silla (de 1 a N)
                conteo_reservas += 1
                if conteo_reservas == cantidad:
                    break
        
        total = float(cantidad * self.precio)
        
        # CRÍTICO: Devolver el precio y las sillas para que Cine las guarde en Entrada
        return total, sillas_reservadas

    def liberar_boleta(self, indices_a_liberar):
        """
        Libera las sillas específicas de una compra cancelada, usando los IDs guardados en Entrada.
        """
        for indice_silla in indices_a_liberar:
            # Convertimos el ID de silla (1 a N) al índice de la lista (0 a N-1)
            lista_index = indice_silla - 1 
            
            # Verificación de seguridad
            if 0 <= lista_index < self.sillas_totales and not self.sillas_disponibles[lista_index]:
                self.sillas_disponibles[lista_index] = True
            # No es necesario un 'else', ya que solo se liberan sillas que se marcaron como ocupadas.
        
        return len(indices_a_liberar) # Devolvemos la cantidad de sillas liberadas


# ---------------- PRUEBA RÁPIDA ----------------
if __name__ == "__main__":
    sala_prueba = Sala("Sala 2D Prueba", 10, 10000.00)
    sala_prueba.mostrar_disponibles()

    # Venta 1
    # Vender 3 boletas
    try:
        total1, sillas1 = sala_prueba.vender_boleta(3)
        print(f"✅ Venta: ${total1:,.2f}, Sillas Reservadas: {sillas1}") # Sillas: [1, 2, 3]
        sala_prueba.mostrar_disponibles()
    except ValueError as e:
        print(f"❌ {e}")

    # Cancelación (liberando las sillas de la Venta 1)
    liberadas = sala_prueba.liberar_boleta(sillas1)
    print(f"🔄 Cancelación: Se liberaron {liberadas} sillas.") 
    sala_prueba.mostrar_disponibles()
