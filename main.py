"""
Punto de entrada del sistema de catálogo de servicios académicos.

Este archivo cumple el rol del "composition root": es el único lugar donde
se decide qué implementación concreta se usa y se conecta con las vistas.
Si mañana se crea CatalogoServicioSQL, solo cambia la línea de creación
del servicio; las vistas no se tocan (principio Abierto/Cerrado).

Ejecutar desde la carpeta que contiene este archivo:
    python main.py
"""

from __future__ import annotations

import sys

from domain.categoria_producto import CategoriaProducto
from services.impl.catalogo_servicio_memoria import CatalogoServicioMemoria
from services.impl.datos_ejemplo import crear_catalogo_ejemplo
from ui.vista_cuadricula import VistaCuadricula


def configurar_salida_utf8() -> None:
    """
    Fuerza UTF-8 en la salida estándar.

    Es un ajuste útil en Windows: si la salida se redirige a un archivo o a
    otra aplicación, Python puede usar cp1252 y fallar al imprimir los
    bordes Unicode de las tarjetas o algunas tildes. La consola moderna de
    Windows y VS Code trabajan sin problema con UTF-8.
    """
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def cargar_catalogo_de_ejemplo() -> CatalogoServicioMemoria:
    """
    Carga los datos de ejemplo compartidos con la aplicación web.

    La fuente de datos vive en services/impl/datos_ejemplo.py para evitar
    duplicar productos entre la demo de consola y la interfaz web.
    """
    return crear_catalogo_ejemplo()


def demostrar_crud(catalogo: CatalogoServicioMemoria) -> None:
    """
    Demuestra que los métodos CRUD de la interfaz están operativos.

    Esta sección no es necesaria para el catálogo, pero evidencia que la
    estructura quedó preparada para futuras ampliaciones (OCP).
    """
    print("\n[CRUD] La interfaz también permite registrar y eliminar productos.")

    # Se calcula un ID libre para que la demo siga funcionando aunque cambien
    # los datos de ejemplo o se agreguen más productos.
    id_libre = max(producto.id for producto in catalogo.obtener_todos()) + 1

    nuevo = CategoriaProducto(
        id=id_libre,
        nombre="Curso de refuerzo",
        descripcion=(
            "Curso corto de refuerzo con ejercicios prácticos y evaluación "
            "final para consolidar temas vistos en clase."
        ),
        precio_promedio=150_000.0,
        url_imagen="/static/img/placeholder.svg",
        categoria="Asesoría",
    )

    catalogo.registrar_producto(nuevo)
    print(f"  Producto registrado: {nuevo}")
    print(f"  Total de productos: {len(catalogo.obtener_todos())}")

    catalogo.eliminar_producto(nuevo.id)
    print(f"  Producto con ID {nuevo.id} eliminado.")
    print(f"  Total de productos: {len(catalogo.obtener_todos())}")


def main() -> None:
    """
    Ejecuta la simulación completa:

    1. Se crea el servicio en memoria (backend).
    2. Se inyecta en VistaCuadricula (UI).
    3. Se muestra la cuadrícula tipo tienda virtual.
    4. Se simula el clic en una tarjeta.
    5. Se abre la vista de detalle en "pantalla completa".
    """
    configurar_salida_utf8()
    catalogo = cargar_catalogo_de_ejemplo()

    # La vista recibe la interfaz, no la implementación concreta.
    vista_cuadricula = VistaCuadricula(catalogo)

    # 1) Pantalla principal: cuadrícula de productos.
    vista_cuadricula.mostrar_catalogo()

    # 2) Simulación de clic en la tarjeta con ID 2.
    print("\n[SIMULACIÓN] El usuario hace clic en la tarjeta con ID 2...")
    vista_cuadricula.seleccionar_producto(2)

    # 3) Demostración opcional del CRUD preparado en el contrato.
    demostrar_crud(catalogo)


# Este bloque hace que el archivo sea ejecutable directamente.
# Si se importa desde otro módulo, main() no se ejecuta automáticamente.
if __name__ == "__main__":
    main()
