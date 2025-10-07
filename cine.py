# Integrantes: Daniel Contreras, Isabella Estupiñan, Antonio Cortes y Roxsana Zuluaga
# Descripción: Administra las salas (2D y 3D), permite vender y cancelar entradas, mostrar la información general y llevar el registro de las ventas totales.

from sala import Sala
from sala3d import Sala3D

# ------------------- DEFINICIÓN DE LA CLASE CINE -------------------
class Cine:
    """
    Clase que representa un cine, que contiene varias salas (2D o 3D)
    y permite agregar salas, vender entradas, cancelar compras y mostrar reportes.
    """

    # Método constructor: se ejecuta al crear un objeto Cine
    def __init__(self, nombre):
        # Nombre del cine (privado, no se debería modificar desde fuera)
        self.__nombre = nombre
        # Lista de salas que contiene el cine (inicialmente vacía)
        self.__salas = []

    # ------------------- MÉTODOS -------------------

    def agregar_sala(self, sala):
        """
        Agrega un objeto Sala o Sala3D al cine.
        """
        self.__salas.append(sala)  # Añadimos la sala a la lista
        print(f"Sala '{sala.nombre}' agregada al cine {self.__nombre}.")

    def mostrar_salas(self):
        """
        Muestra todas las salas registradas en el cine.
        """
        if not self.__salas:
            print("No hay salas registradas.")  # Mensaje si no hay salas
        else:
            print(f"\nSalas del cine {self.__nombre}:")
            # Recorremos la lista y mostramos el número y nombre de cada sala
            for i, sala in enumerate(self.__salas, start=1):
                print(f"{i}. {sala.nombre}")

    def buscar_sala(self, nombre):
        """
        Busca una sala por su nombre y la devuelve.
        """
        for sala in self.__salas:  # Recorremos todas las salas
            if sala.nombre.lower() == nombre.lower():  # Compara ignorando mayúsculas
                return sala  # Retorna la sala encontrada
        return None  # Retorna None si no se encontró

    def vender_entrada(self, nombre_sala, tipo=None, cantidad=1):
        """
        Vende entradas en la sala indicada.
        """
        sala = self.buscar_sala(nombre_sala)  # Buscamos la sala
        if sala:  # Si la sala existe
            # Polimorfismo: llamamos al método adecuado según el tipo de sala
            if isinstance(sala, Sala3D):
                print(sala.vender_boleta(tipo, cantidad))
            else:
                print(sala.vender_boleta(cantidad))
        else:
            print("❌ Sala no encontrada.")  # Mensaje si la sala no existe

    def cancelar_compra(self, nombre_sala, tipo=None, cantidad=1):
        """
        Cancela la compra de entradas en la sala indicada.
        """
        sala = self.buscar_sala(nombre_sala)
        if sala:
            # Polimorfismo: usamos el método correcto según sea 2D o 3D
            if isinstance(sala, Sala3D):
                print(sala.cancelar_compra(tipo, cantidad))
            else:
                print(sala.cancelar_compra(cantidad))
        else:
            print("❌ Sala no encontrada.")

    def mostrar_reporte(self):
        """
        Muestra un resumen del cine, mostrando la disponibilidad
        de sillas en cada sala.
        """
        print(f"\n--- REPORTE DEL CINE {self.__nombre} ---")
        for sala in self.__salas:
            sala.mostrar_disponibles()  # Cada sala muestra su disponibilidad


# ------------------- PRUEBA -------------------

if __name__ == "__main__":
    # Crear salas: una 2D y otra 3D
    sala2d = Sala("Sala 2D", 50, 10000)  # 50 sillas, precio 10000
    sala3d = Sala3D("Sala 3D", 30, 10, 15000, 20000)  # 30 generales, 10 preferenciales

    # Crear el cine
    cine = Cine("Cine UAO")

    # Agregar las salas al cine
    cine.agregar_sala(sala2d)
    cine.agregar_sala(sala3d)

    # Mostrar todas las salas del cine
    cine.mostrar_salas()

    # Vender entradas
    cine.vender_entrada("Sala 2D", cantidad=2)  # 2 entradas 2D
    cine.vender_entrada("Sala 3D", tipo="preferencial", cantidad=3)  # 3 entradas preferenciales 3D

    # Mostrar reporte final con disponibilidad de todas las salas
    cine.mostrar_reporte()