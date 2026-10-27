"""
Paquete "domain".

Contiene las entidades del negocio. Esta capa no debe conocer la consola,
la base de datos ni ningún detalle de infraestructura: solo modela y valida
los datos del catálogo.
"""

from domain.categoria_producto import CategoriaProducto

__all__ = ["CategoriaProducto"]
