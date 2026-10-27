"""
VistaDetalleProducto: simulación de la pantalla de detalle.

Recibe un CategoriaProducto y muestra toda su información en un panel de
ancho completo. No modifica el producto ni accede al servicio: es una vista
de solo lectura.
"""

from __future__ import annotations

import textwrap

from domain.categoria_producto import CategoriaProducto
from ui.formato import abreviar, ancho_consola, formatear_precio


class VistaDetalleProducto:
    """
    Muestra la ficha ampliada de un producto.

    El atributo _producto es privado y se expone con una propiedad de solo
    lectura para respetar el encapsulamiento.
    """

    def __init__(self, producto: CategoriaProducto) -> None:
        if not isinstance(producto, CategoriaProducto):
            raise TypeError("VistaDetalleProducto espera un CategoriaProducto.")
        self._producto = producto

    @property
    def producto(self) -> CategoriaProducto:
        """Producto que se está mostrando."""
        return self._producto

    def renderizar_detalle(self) -> None:
        """
        Dibuja el detalle en la consola.

        Se usa todo el ancho disponible para simular la "pantalla completa"
        que en una aplicación web sería la página de detalle del producto.
        """
        # obtener_info_completa() devuelve un diccionario con todos los datos.
        info = self._producto.obtener_info_completa()

        ancho = ancho_consola()
        margen = "  "
        ancho_util = ancho - (len(margen) * 2)

        print()
        print("=" * ancho)
        print("DETALLE DEL SERVICIO ACADÉMICO".center(ancho))
        print("=" * ancho)
        print()

        # En una interfaz gráfica aquí se mostraría la imagen. En consola se
        # simula con la etiqueta [IMAGEN] y la URL del archivo.
        url = str(info["url_imagen"]) or "sin imagen"
        print(f"{margen}[IMAGEN] {abreviar(url, ancho_util - 9)}")
        print(f"{margen}{'-' * ancho_util}")
        print()

        # Ficha con etiquetas alineadas.
        etiqueta = 18
        print(f"{margen}{'Nombre':<{etiqueta}}: {info['nombre']}")
        print(
            f"{margen}{'Precio promedio':<{etiqueta}}: "
            f"{formatear_precio(float(info['precio_promedio']))}"
        )
        print(f"{margen}{'ID':<{etiqueta}}: {info['id']}")
        print()
        print(f"{margen}{'Descripción':<{etiqueta}}:")

        # La descripción puede ser larga: se ajusta al ancho de la ventana.
        ancho_descripcion = max(20, ancho - len(margen) - etiqueta - 2)
        lineas = textwrap.wrap(
            str(info["descripcion"]),
            width=ancho_descripcion,
        ) or [""]

        for linea in lineas:
            print(f"{margen}{'':<{etiqueta}}  {linea}")

        print()
        print("=" * ancho)
        print(
            "Fin del detalle. Usa el ID de otra tarjeta para abrir otro producto."
            .center(ancho)
        )
        print("=" * ancho)
