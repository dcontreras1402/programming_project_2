# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Administra las salas (2D y 3D), permite vender y cancelar entradas, mostrar la información general y llevar el registro de las ventas totales.

from sala import Sala
from sala3d import Sala3D
from entrada import Entrada 
from cliente import Cliente 

# ------------------- DEFINICIÓN DE LA CLASE CINE -------------------
class Cine:
    """
    Clase que representa un cine, que contiene varias salas (2D o 3D)
    y permite agregar salas, vender entradas, cancelar compras y mostrar reportes.
    """

    # Método constructor: se ejecuta al crear un objeto Cine
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__salas = []
        self.registro_entradas = [] # Lista de objetos Entrada

    # ------------------- MÉTODOS DE GESTIÓN DE SALAS -------------------

    def agregar_sala(self, sala):
        """
        Agrega un objeto Sala o Sala3D al cine.
        """
        self.__salas.append(sala) 
        print(f"Sala '{sala.nombre}' agregada al cine {self.__nombre}.")

    def mostrar_salas(self):
        """
        Muestra todas las salas registradas en el cine.
        """
        if not self.__salas:
            print("No hay salas registradas.") 
        else:
            print(f"\nSalas del cine {self.__nombre}:")
            for i, sala in enumerate(self.__salas, start=1):
                print(f"{i}. {sala.nombre}")

    def buscar_sala(self, nombre):
        """
        Busca una sala por su nombre y la devuelve.
        """
        for sala in self.__salas:
            if sala.nombre.lower() == nombre.lower():
                return sala
        return None

    # ------------------- MÉTODOS DE VENTA Y CANCELACIÓN -------------------

    def vender_entrada(self, cliente: Cliente, nombre_sala: str, cantidad: int, tipo: str = 'general'):
        """
        Vende entradas en la sala indicada y registra la transacción.
        """
        sala = self.buscar_sala(nombre_sala)
        if not sala:
            print("❌ Sala no encontrada.")
            return

        try:
            # 1. Llamar al método de venta de la sala. 
            # El método debe manejar la diferencia entre Sala (solo general) y Sala3D (general/preferencial)
            if isinstance(sala, Sala3D):
                # Sala 3D necesita el 'tipo' para vender
                precio_total, sillas_reservadas = sala.vender_boleta(tipo, cantidad)
            else:
                # Sala 2D (solo tiene un precio/tipo), solo necesita la 'cantidad'
                precio_total, sillas_reservadas = sala.vender_boleta(cantidad)
            
            # 2. Crear y registrar el objeto Entrada con los datos críticos
            nueva_entrada = Entrada(
                cliente=cliente, 
                sala_nombre=nombre_sala, 
                categoria=tipo, 
                cantidad=cantidad, 
                precio_total=precio_total,
                sillas_reservadas=sillas_reservadas # CRÍTICO: Registramos qué sillas se compraron
            )
            self.registro_entradas.append(nueva_entrada)
            print(f"✅ Venta exitosa (ID {nueva_entrada.id}). {cantidad} boletas en '{nombre_sala}' por ${precio_total:,.2f}.")
            print(f"   Sillas reservadas: {sillas_reservadas}")
            
        except ValueError as e:
            # Captura errores de falta de disponibilidad
            print(f"❌ Venta fallida en '{nombre_sala}': {e}")

    def cancelar_compra(self, id_compra):
        """
        Cancela la compra buscando por ID, libera las sillas y elimina el registro.
        """
        entrada_a_cancelar = None
        index_a_eliminar = -1

        # 1. Buscar la entrada por ID
        for i, entrada in enumerate(self.registro_entradas):
            if entrada.id == id_compra:
                entrada_a_cancelar = entrada
                index_a_eliminar = i
                break

        if entrada_a_cancelar is None:
            print(f"❌ Error: No se encontró la compra con ID {id_compra}.")
            return

        # 2. Encontrar la sala afectada
        sala = self.buscar_sala(entrada_a_cancelar.sala_nombre)
        if not sala:
            print(f"⚠️ Advertencia: Sala '{entrada_a_cancelar.sala_nombre}' no encontrada. Solo se eliminará el registro de venta.")
            self.registro_entradas.pop(index_a_eliminar)
            return

        # 3. Liberar las sillas en la sala
        sillas = entrada_a_cancelar.sillas_reservadas
        tipo = entrada_a_cancelar.categoria
        
        try:
            if isinstance(sala, Sala3D):
                # Sala 3D necesita el tipo de silla (general/preferencial) para liberar
                liberadas = sala.liberar_boleta(tipo, sillas)
            else:
                # Sala 2D solo necesita la lista de sillas
                liberadas = sala.liberar_boleta(sillas)
            
            # 4. Eliminar el registro de entrada
            if liberadas == entrada_a_cancelar.cantidad:
                self.registro_entradas.pop(index_a_eliminar)
                print(f"✅ Cancelación exitosa (ID {id_compra}). Se liberaron {liberadas} sillas en '{sala.nombre}'.")
            else:
                # Caso de error si no se liberaron todas las sillas correctamente
                print(f"⚠️ Error parcial: Solo se liberaron {liberadas} de {entrada_a_cancelar.cantidad} sillas. Revise la sala.")

        except Exception as e:
            print(f"❌ Error al liberar sillas en '{sala.nombre}': {e}")


    # ------------------- MÉTODOS DE REPORTE -------------------

    def mostrar_reporte(self):
        """
        Muestra un resumen del cine, disponibilidad de salas y ventas totales.
        """
        print(f"\n--- REPORTE DEL CINE {self.__nombre} ---")
        
        # Reporte de Disponibilidad de Salas
        print("\n[DISPONIBILIDAD DE SALAS]")
        if not self.__salas:
            print("No hay salas registradas.")
        for sala in self.__salas:
            sala.mostrar_disponibles()

        # Reporte de Ventas
        print("\n[REGISTRO DE VENTAS]")
        if not self.registro_entradas:
            print("No hay ventas registradas.")
            return

        total_ventas = sum(e.precio_total for e in self.registro_entradas)
        print(f"Total de Compras Registradas: {len(self.registro_entradas)}")
        print(f"INGRESOS TOTALES ESTIMADOS: ${total_ventas:,.2f}")
        
        # Mostrar detalle de cada venta (opcional)
        print("\n--- Detalle de Ventas ---")
        for entrada in self.registro_entradas:
            entrada.mostrar_info()
