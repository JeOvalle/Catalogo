"""
Paquete "services".

Define el contrato (interfaz) de la capa de servicios y las excepciones
propias de esa capa. La implementación concreta vive en services/impl/.
"""

from services.excepciones import (
    CatalogoError,
    ProductoDuplicadoError,
    ProductoNoEncontradoError,
)
from services.icatalogo_servicio import ICatalogoServicio

__all__ = [
    "ICatalogoServicio",
    "CatalogoError",
    "ProductoDuplicadoError",
    "ProductoNoEncontradoError",
]
