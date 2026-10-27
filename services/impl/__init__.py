"""
Paquete "services.impl".

Aquí viven las implementaciones concretas de la interfaz
ICatalogoServicio. Actualmente se incluye una implementación en memoria.
"""

from services.impl.catalogo_servicio_memoria import CatalogoServicioMemoria

__all__ = ["CatalogoServicioMemoria"]
