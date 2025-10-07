from typing import Optional
from cine import Cine
from cliente import Cliente
from sala import Sala
from sala3d import Sala3D
from persistencia import GestorPersistencia


# FUNCIONES DE INTERFAZ

def obtener_cliente_info() -> Optional[Cliente]:
    """Solicita y valida los datos del cliente."""
    print("\n--- Ingrese los datos del Cliente ---")
    try:
        nombre = input("Nombre completo: ").strip()
        cedula = input("Cédula: ").strip()
        correo = input("Correo electrónico: ").strip()
        
        return Cliente(nombre, cedula, correo)
    except ValueError as e:
        print(f"[ERROR] Error en los datos del cliente: {e}")
        return None

def solicitar_entero(prompt: str, min_val: int = 1) -> Optional[int]:
    """Solicita un entero validando que sea mayor o igual a min_val."""
    while True:
        try:
            valor = input(prompt).strip()
            if not valor:
                # Permite al usuario salir sin error si solo presiona Enter
                return None 
            
            valor_int = int(valor)
            if valor_int < min_val:
                print(f"[ERROR] El valor debe ser mayor o igual a {min_val}.")
                continue
            return valor_int
        except ValueError:
            print("[ERROR] Entrada inválida. Por favor, ingrese un número entero.")
            return None


def manejar_venta(cine: Cine):
    """Flujo interactivo para la venta de boletas."""
    print(f"\n{'*'*50}\n*** INICIO DE PROCESO DE VENTA ***\n{'*'*50}")
    
    cliente = obtener_cliente_info()
    if cliente is None:
        return

    cine.mostrar_salas()
    nombre_sala = input("\nIngrese el nombre de la sala para la compra: ").strip()
    sala = cine.buscar_sala(nombre_sala)

    if sala is None:
        print(f"[ERROR] La sala '{nombre_sala}' no existe.")
        return

    tipo_boleta = "general"
    # Se usa isinstance para determinar si es Sala3D (clase importada)
    if isinstance(sala, Sala3D):
        print("\n--- Categorías disponibles ---")
        print("1. General")
        print("2. Preferencial")
        opcion_tipo = input("Seleccione el tipo de boleta (1 o 2): ").strip()
        
        if opcion_tipo == '2':
            tipo_boleta = "preferencial"
        elif opcion_tipo != '1':
            print("[ERROR] Opción inválida. Cancelando venta.")
            return
    
    cantidad = solicitar_entero("Ingrese la cantidad de boletas a comprar: ")
    if cantidad is None:
        return

    # La clase Cine maneja la lógica interna de venta y llama a la persistencia
    cine.vender_entrada(cliente, nombre_sala, cantidad, tipo_boleta)

def manejar_cancelacion(cine: Cine):
    """Flujo interactivo para la cancelación de boletas."""
    print(f"\n{'*'*50}\n*** INICIO DE PROCESO DE CANCELACIÓN ***\n{'*'*50}")
    
    if not cine.registro_entradas:
        print("[INFO] No hay compras registradas para cancelar.")
        return

    print("\n--- Compras Registradas (Consulte el ID en el Reporte) ---")
    id_compra = solicitar_entero("Ingrese el ID de la compra a cancelar: ")
    if id_compra is None:
        return

    # La clase Cine maneja la lógica interna de cancelación y llama a la persistencia
    cine.cancelar_compra(id_compra)


def menu_principal(cine: Cine):
    """Muestra el menú principal y maneja las opciones."""
    while True:
        print(f"\n\n{'#'*60}")
        print(f"### Bienvenido al Sistema de Gestión de {cine._Cine__nombre} ###")
        print(f"{'#'*60}")
        print("\n--- Menú Principal ---")
        print("1. Vender Entradas")
        print("2. Cancelar Compra")
        print("3. Mostrar Reporte (Disponibilidad y Ventas)")
        print("4. Salir y Guardar Datos")
        
        opcion = input("\nSeleccione una opción (1-4): ").strip()

        if opcion == '1':
            manejar_venta(cine)
        elif opcion == '2':
            manejar_cancelacion(cine)
        elif opcion == '3':
            cine.mostrar_reporte()
        elif opcion == '4':
            print(f"\nSaliendo del sistema de {cine._Cine__nombre}...")
            # Usa el GestorPersistencia importado para guardar
            GestorPersistencia.guardar_datos(cine, cine.registro_entradas)
            break
        else:
            print("[ERROR] Opción no válida. Intente de nuevo.")


# BLOQUE MAIN: El sistema de ejecución
if __name__ == '__main__':
    
    # 1. Crear el objeto Cine
    cine_principal = Cine("Western Cinema")

    # 2. Intentar cargar datos existentes
    # Usa el GestorPersistencia importado para cargar
    registro_entradas_cargado = GestorPersistencia.cargar_datos(cine_principal)
    if registro_entradas_cargado:
        cine_principal.registro_entradas = registro_entradas_cargado

    # 3. Si no se cargaron salas, se crean las iniciales por defecto (usando clases importadas)
    if not cine_principal._Cine__salas:
        print("\n[INFO] Inicializando salas por primera vez (no se encontraron datos guardados)...")
        try:
            sala2d = Sala("Sala 2D", 50, 10000.00)
            sala3d = Sala3D("Sala 3D", 30, 10, 15000.00, 20000.00)

            cine_principal.agregar_sala(sala2d)
            cine_principal.agregar_sala(sala3d)
            GestorPersistencia.guardar_datos(cine_principal, cine_principal.registro_entradas)
        except ValueError as e:
            print(f"[FATAL ERROR] No se pudieron inicializar las salas: {e}")
            exit(1)
    
    # 4. Iniciar el menú principal del sistema
    menu_principal(cine_principal)
