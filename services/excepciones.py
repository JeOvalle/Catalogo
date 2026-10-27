"""
Excepciones de la capa de servicios.

Usar excepciones propias hace que los errores del catálogo sean claros y
fáciles de capturar sin depender de mensajes de texto.
"""


class CatalogoError(Exception):
    """Clase base para todos los errores del catálogo."""


class ProductoNoEncontradoError(CatalogoError):
    """Se lanza cuando se busca o elimina un producto que no existe."""

    def __init__(self, id_producto: int) -> None:
        self.id_producto = id_producto
        super().__init__(f"No existe un producto con el id {id_producto}.")


class ProductoDuplicadoError(CatalogoError):
    """Se lanza cuando se intenta registrar un id que ya está en uso."""

    def __init__(self, id_producto: int) -> None:
        self.id_producto = id_producto
        super().__init__(f"Ya existe un producto con el id {id_producto}.")
