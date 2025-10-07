# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Representa una sala de cine 3D con categoría general y preferencial.

from sala import Sala

class Sala3D(Sala):
    def __init__(self, nombre, total_general, total_preferencial, precio_general, precio_preferencial):
        
        # Inicializa la parte de asientos Generales (hereda nombre, precio y sillas_disponibles)
        # El total de sillas de la Sala base será el total_general.
        super().__init__(nombre, total_general, precio_general)
        
        # Atributos específicos de la Sala 3D (sillas preferenciales y su precio)
        self.total_preferencial = total_preferencial
        self.precio_preferencial = precio_preferencial
        
        # La lista de sillas preferenciales empieza su indexación después de las generales
        # Asignamos IDs de silla consecutivos después de las generales.
        self.sillas_preferenciales = [True] * total_preferencial

    def mostrar_disponibles(self):
        """
        Sobreescribe el método base para mostrar la disponibilidad por categoría.
        """
        disponibles_general = sum(self.sillas_disponibles)
        disponibles_preferencial = sum(self.sillas_preferenciales)
        
        print(f"\n--- Sala 3D '{self.nombre}' ---")
        print(f"  Generales: {disponibles_general}/{self.sillas_totales} disponibles (Precio: ${self.precio:,.2f})")
        print(f"  Preferenciales: {disponibles_preferencial}/{self.total_preferencial} disponibles (Precio: ${self.precio_preferencial:,.2f})")

    def vender_boleta(self, tipo, cantidad):
        """
        Vende boletas por tipo ('general' o 'preferencial').
        Devuelve (precio_total, sillas_reservadas).
        """
        if tipo == "general":
            # Reutilizamos el método del padre (Sala), que ya devuelve (total, sillas)
            # El ID de las sillas es de 1 hasta self.sillas_totales (total_general)
            return super().vender_boleta(cantidad)
            
        elif tipo == "preferencial":
            disponibles = sum(self.sillas_preferenciales)
            if disponibles < cantidad:
                raise ValueError(f"Solo quedan {disponibles} sillas preferenciales disponibles en '{self.nombre}'.")
            
            sillas_reservadas = []
            conteo_reservas = 0
            
            # Cálculo del ID de inicio de las sillas preferenciales
            # Las sillas generales van de 1 a N, las preferenciales de N+1 a N+M.
            id_inicio = self.sillas_totales + 1
            
            # Recorremos para encontrar y reservar los asientos preferenciales
            for i in range(self.total_preferencial):
                if self.sillas_preferenciales[i]:
                    self.sillas_preferenciales[i] = False  # Ocupar la silla
                    # El ID de la silla es el ID base + el índice de la lista preferencial
                    silla_id = id_inicio + i 
                    sillas_reservadas.append(silla_id)
                    conteo_reservas += 1
                    if conteo_reservas == cantidad:
                        break
            
            total = float(cantidad * self.precio_preferencial)
            
            # Devolver el precio y las sillas para que Cine las guarde en Entrada
            return total, sillas_reservadas
            
        else:
            raise ValueError("Tipo de boleta inválido. Use 'general' o 'preferencial'.")

    def liberar_boleta(self, tipo, indices_a_liberar):
        """
        Libera las sillas específicas por tipo de categoría, usando los IDs guardados en Entrada.
        """
        liberadas = 0
        
        if tipo == "general":
            # Delegamos a la clase padre la liberación de sillas generales
            liberadas = super().liberar_boleta(indices_a_liberar)
            return liberadas
            
        elif tipo == "preferencial":
            # Rango de IDs de las sillas preferenciales
            id_inicio_preferencial = self.sillas_totales + 1
            id_fin_preferencial = self.sillas_totales + self.total_preferencial
            
            for indice_silla in indices_a_liberar:
                # 1. Verificar que el ID de silla esté en el rango preferencial
                if id_inicio_preferencial <= indice_silla <= id_fin_preferencial:
                    
                    # 2. Convertir el ID global (N+X) al índice local de la lista preferencial (X)
                    lista_index = indice_silla - id_inicio_preferencial 
                    
                    # 3. Liberar la silla si estaba ocupada
                    if not self.sillas_preferenciales[lista_index]:
                        self.sillas_preferenciales[lista_index] = True
                        liberadas += 1
                        
            return liberadas
            
        else:
            # Aunque Cine debe manejar esto, devuelve 0 en caso de tipo inválido
            return 0


# PRUEBA RÁPIDA
if __name__ == "__main__":
    # 10 sillas generales (ID 1-10) a 10000
    # 5 sillas preferenciales (ID 11-15) a 15000
    sala3d_prueba = Sala3D("Sala Fantasía", 10, 5, 10000.00, 15000.00)
    sala3d_prueba.mostrar_disponibles()

    # Venta Preferencial
    try:
        total_p, sillas_p = sala3d_prueba.vender_boleta("preferencial", 2)
        print(f"✅ Venta Pref: ${total_p:,.2f}, Sillas: {sillas_p}") # Sillas: [11, 12]
        sala3d_prueba.mostrar_disponibles()
    except ValueError as e:
        print(f"❌ {e}")

    # Venta General
    try:
        total_g, sillas_g = sala3d_prueba.vender_boleta("general", 3)
        print(f"✅ Venta General: ${total_g:,.2f}, Sillas: {sillas_g}") # Sillas: [1, 2, 3]
        sala3d_prueba.mostrar_disponibles()
    except ValueError as e:
        print(f"❌ {e}")
        
    # Cancelación Preferencial
    liberadas_p = sala3d_prueba.liberar_boleta("preferencial", sillas_p)
    print(f"🔄 Cancelación Pref: Se liberaron {liberadas_p} sillas.") 
    sala3d_prueba.mostrar_disponibles()
