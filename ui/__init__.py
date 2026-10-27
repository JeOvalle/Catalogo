"""
Paquete "ui".

Contiene las vistas de consola que simulan la interfaz web:
- VistaCuadricula: catálogo en forma de tarjetas.
- VistaDetalleProducto: ficha ampliada de un producto.
"""

from ui.vista_cuadricula import VistaCuadricula
from ui.vista_detalle_producto import VistaDetalleProducto

__all__ = ["VistaCuadricula", "VistaDetalleProducto"]
