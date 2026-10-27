"""
Entidad de dominio: CategoriaProducto.

Representa un servicio académico del catálogo (ensayo, laboratorio,
proyecto, etc.). Se usa POO "estricta":

- Los datos se guardan en atributos privados (con guion bajo).
- Se exponen mediante propiedades (@property) para validar cada cambio.
- La clase no imprime nada: la presentación es responsabilidad de ui/.
"""

from __future__ import annotations

from typing import Any


class CategoriaProducto:
    """
    Modelo de un servicio académico ofrecido en el catálogo.

    Atributos del diagrama de clases:
        id              -> identificador único (entero positivo).
        nombre          -> nombre del servicio.
        descripcion     -> texto ampliado que se muestra en el detalle.
        precio_promedio -> valor promedio del servicio.
        url_imagen      -> dirección de la imagen de la tarjeta.
    """

    def __init__(
        self,
        id: int,
        nombre: str,
        descripcion: str,
        precio_promedio: float,
        url_imagen: str = "",
        categoria: str = "General",
    ) -> None:
        # Se asignan mediante las propiedades para que las validaciones
        # también se apliquen al crear el objeto.
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_promedio = precio_promedio
        self.url_imagen = url_imagen
        self.categoria = categoria

    # ------------------------------------------------------------------
    # Propiedades con validación (encapsulamiento)
    # ------------------------------------------------------------------

    @property
    def id(self) -> int:
        """Identificador único del producto."""
        return self._id

    @id.setter
    def id(self, valor: int) -> None:
        # bool es subclase de int en Python; se excluye explícitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("El id debe ser un número entero.")
        if valor <= 0:
            raise ValueError("El id debe ser mayor que cero.")
        self._id = valor

    @property
    def nombre(self) -> str:
        """Nombre corto que se muestra en la tarjeta."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def descripcion(self) -> str:
        """Descripción ampliada del servicio."""
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La descripción no puede estar vacía.")
        self._descripcion = valor.strip()

    @property
    def precio_promedio(self) -> float:
        """Precio promedio del servicio."""
        return self._precio_promedio

    @precio_promedio.setter
    def precio_promedio(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("El precio promedio debe ser numérico.")
        if valor < 0:
            raise ValueError("El precio promedio no puede ser negativo.")
        # Se normaliza a float para que el atributo siempre tenga el mismo tipo.
        self._precio_promedio = float(valor)

    @property
    def url_imagen(self) -> str:
        """Dirección de la imagen del producto (puede estar vacía)."""
        return self._url_imagen

    @url_imagen.setter
    def url_imagen(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("La URL de la imagen debe ser texto.")
        self._url_imagen = valor.strip()

    @property
    def categoria(self) -> str:
        """Categoría usada para filtros y navegación en la tienda."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = valor.strip()

    # ------------------------------------------------------------------
    # Comportamiento del dominio
    # ------------------------------------------------------------------

    def obtener_info_completa(self) -> dict[str, Any]:
        """
        Devuelve todos los datos del producto en un diccionario.

        ¿Por qué un diccionario y no texto formateado? Porque el dominio no
        debe saber si la información se mostrará en consola, en una web o en
        una app móvil. La capa ui/ decide cómo presentar estos datos.

        Retorna:
            dict con las claves: id, nombre, descripcion,
            precio_promedio y url_imagen.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio_promedio": self.precio_promedio,
            "url_imagen": self.url_imagen,
            "categoria": self.categoria,
        }

    def __str__(self) -> str:
        """Representación legible para mensajes al usuario."""
        return f"{self.nombre} (ID: {self.id})"

    def __repr__(self) -> str:
        """Representación técnica útil para depuración."""
        return (
            f"CategoriaProducto(id={self.id!r}, nombre={self.nombre!r}, "
            f"precio_promedio={self.precio_promedio!r})"
        )
