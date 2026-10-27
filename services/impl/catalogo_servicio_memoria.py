"""
Implementación en memoria de ICatalogoServicio.

Guarda los productos en una lista de Python. Es útil para practicar la
arquitectura y para ejecutar el ejemplo sin base de datos.

Gracias al OCP, mañana se podría crear otra clase
(ej. CatalogoServicioSQL) que implemente la misma interfaz y las vistas
seguirían funcionando sin cambios.
"""

from __future__ import annotations

from collections.abc import Iterable

from domain.categoria_producto import CategoriaProducto
from services.excepciones import ProductoDuplicadoError, ProductoNoEncontradoError
from services.icatalogo_servicio import ICatalogoServicio


class CatalogoServicioMemoria(ICatalogoServicio):
    """
    Catálogo almacenado en una lista en memoria.

    El atributo _productos es privado (guion bajo): solo esta clase debe
    modificarlo. Las vistas acceden a los datos mediante los métodos del
    contrato ICatalogoServicio.
    """

    def __init__(
        self,
        productos_iniciales: Iterable[CategoriaProducto] | None = None,
    ) -> None:
        # Lista interna. Se inicializa vacía y se llena usando el método
        # registrar_producto para no duplicar las validaciones.
        self._productos: list[CategoriaProducto] = []

        for producto in productos_iniciales or []:
            self.registrar_producto(producto)

    # ------------------------------------------------------------------
    # Operaciones de lectura
    # ------------------------------------------------------------------

    def obtener_todos(self) -> list[CategoriaProducto]:
        """
        Devuelve una copia de la lista interna.

        La copia evita que quien recibe la lista pueda agregar, borrar o
        reemplazar elementos del catálogo sin pasar por los métodos CRUD.
        """
        return list(self._productos)

    def buscar_por_id(self, id: int) -> CategoriaProducto | None:
        """Recorre la lista y retorna el primer producto con ese id."""
        for producto in self._productos:
            if producto.id == id:
                return producto
        return None

    # ------------------------------------------------------------------
    # Operaciones CRUD
    # ------------------------------------------------------------------

    def registrar_producto(self, producto: CategoriaProducto) -> None:
        """
        Agrega un producto al final de la lista.

        Lanza:
            TypeError: si no se recibe un CategoriaProducto.
            ProductoDuplicadoError: si el id ya está registrado.
        """
        if not isinstance(producto, CategoriaProducto):
            raise TypeError("Solo se pueden registrar objetos CategoriaProducto.")

        if self.buscar_por_id(producto.id) is not None:
            raise ProductoDuplicadoError(producto.id)

        self._productos.append(producto)

    def eliminar_producto(self, id: int) -> None:
        """
        Elimina el producto cuyo id coincide.

        Lanza:
            ProductoNoEncontradoError: si no existe un producto con ese id.
        """
        for indice, producto in enumerate(self._productos):
            if producto.id == id:
                self._productos.pop(indice)
                return

        raise ProductoNoEncontradoError(id)
