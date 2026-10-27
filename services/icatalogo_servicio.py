"""
Interfaz ICatalogoServicio.

En Python no existe la palabra reservada "interface" como en Java o C#.
El equivalente es una clase abstracta (ABC) que solo declara métodos
abstractos: define QUÉ se puede hacer, pero no CÓMO se hace.

Principio Abierto/Cerrado (OCP):
- La interfaz está abierta a nuevas implementaciones (memoria, SQL,
  archivo JSON, API REST...) sin modificar las vistas.
- Las vistas dependen de esta abstracción, no de una implementación
  concreta. Por eso se puede cambiar el almacenamiento sin tocar ui/.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.categoria_producto import CategoriaProducto


class ICatalogoServicio(ABC):
    """
    Contrato de lectura y CRUD para el catálogo de servicios académicos.

    Todos los métodos son abstractos: cualquier clase que implemente esta
    interfaz está obligada a definir los cuatro métodos.
    """

    # ------------------------------------------------------------------
    # Operaciones de lectura
    # ------------------------------------------------------------------

    @abstractmethod
    def obtener_todos(self) -> list[CategoriaProducto]:
        """
        Devuelve todos los productos del catálogo.

        La implementación debe devolver una colección segura: modificar la
        lista retornada no debe alterar el estado interno del servicio.
        """
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, id: int) -> CategoriaProducto | None:
        """
        Busca un producto por su identificador.

        Retorna:
            El producto encontrado o None si no existe.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Operaciones CRUD preparadas para futuras ampliaciones (OCP)
    # ------------------------------------------------------------------

    @abstractmethod
    def registrar_producto(self, producto: CategoriaProducto) -> None:
        """
        Agrega un producto nuevo al catálogo.

        La implementación debe rechazar identificadores duplicados.
        """
        raise NotImplementedError

    @abstractmethod
    def eliminar_producto(self, id: int) -> None:
        """
        Elimina un producto por su identificador.

        La implementación debe informar si el producto no existe.
        """
        raise NotImplementedError
