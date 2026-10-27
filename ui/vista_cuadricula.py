"""
VistaCuadricula: simulación de la tienda virtual en consola.

Responsabilidades:
- Pedir los productos al servicio (a través de la interfaz).
- Dibujar cada producto como una tarjeta con imagen, nombre y precio.
- Simular el "clic" en una tarjeta y abrir VistaDetalleProducto.

La vista NO crea productos ni los guarda: solo consume ICatalogoServicio.
"""

from __future__ import annotations

import textwrap

from domain.categoria_producto import CategoriaProducto
from services.icatalogo_servicio import ICatalogoServicio
from ui.formato import abreviar, ancho_consola, formatear_precio
from ui.vista_detalle_producto import VistaDetalleProducto


class VistaCuadricula:
    """
    Muestra el catálogo como una cuadrícula de tarjetas.

    La dependencia se recibe por el constructor (inyección de dependencias)
    y se declara como la interfaz ICatalogoServicio, no como la clase
    concreta. Así la vista funciona con cualquier implementación futura.
    """

    # Dimensiones de cada tarjeta (en caracteres de consola).
    ANCHO_TARJETA = 34
    ALTO_TARJETA = 9
    SEPARACION = 3
    MAX_COLUMNAS = 3

    # Ancho útil para el texto dentro de los bordes:
    # "| " + texto + " |" = 4 caracteres de decoración.
    ANCHO_TEXTO = ANCHO_TARJETA - 4

    def __init__(self, catalogo_servicios: ICatalogoServicio) -> None:
        if not isinstance(catalogo_servicios, ICatalogoServicio):
            raise TypeError(
                "VistaCuadricula espera un objeto que implemente "
                "ICatalogoServicio."
            )
        self._catalogo_servicios = catalogo_servicios

    @property
    def catalogo_servicios(self) -> ICatalogoServicio:
        """Servicio inyectado (expuesto de solo lectura)."""
        return self._catalogo_servicios

    # ------------------------------------------------------------------
    # API de la vista (la que usaría el "navegador" o el controlador)
    # ------------------------------------------------------------------

    def mostrar_catalogo(self) -> None:
        """Dibuja el catálogo completo en la consola."""
        productos = self._catalogo_servicios.obtener_todos()
        ancho = ancho_consola()

        print()
        print("=" * ancho)
        print("CATÁLOGO DE SERVICIOS ACADÉMICOS".center(ancho))
        print("=" * ancho)

        if not productos:
            print("No hay productos registrados todavía.".center(ancho))
            print("=" * ancho)
            return

        columnas = self._calcular_columnas(ancho)

        # Se procesan los productos en grupos del tamaño de una fila.
        for inicio in range(0, len(productos), columnas):
            fila = productos[inicio : inicio + columnas]
            self._imprimir_fila(fila, ancho)

        print("=" * ancho)
        print("Haz clic en una tarjeta usando su ID para ver el detalle.".center(ancho))
        print("=" * ancho)

    def seleccionar_producto(self, id: int) -> VistaDetalleProducto | None:
        """
        Simula el clic del usuario en una tarjeta.

        Busca el producto en el servicio y, si existe, crea y renderiza la
        vista de detalle. Retorna la vista abierta o None si no se encontró
        el producto.
        """
        producto = self._catalogo_servicios.buscar_por_id(id)

        if producto is None:
            print(f"\n[ERROR] No existe un producto con el ID {id}.")
            return None

        print(f"\n[CLICK] Abriendo el detalle de «{producto.nombre}»...")

        # La vista de detalle recibe el modelo ya encontrado. El símbolo
        # "..>" del diagrama UML (VistaCuadricula ..> VistaDetalleProducto)
        # se materializa en esta creación de objeto.
        vista_detalle = VistaDetalleProducto(producto)
        vista_detalle.renderizar_detalle()
        return vista_detalle

    # ------------------------------------------------------------------
    # Dibujo interno de las tarjetas
    # ------------------------------------------------------------------

    def _calcular_columnas(self, ancho: int) -> int:
        """
        Calcula cuántas tarjetas caben en una fila.

        Se suma la separación al ancho total para no dejar un espacio de más
        al final de la fila.
        """
        espacio_por_tarjeta = self.ANCHO_TARJETA + self.SEPARACION
        columnas = (ancho + self.SEPARACION) // espacio_por_tarjeta
        return max(1, min(self.MAX_COLUMNAS, columnas))

    def _imprimir_fila(
        self,
        productos: list[CategoriaProducto],
        ancho: int,
    ) -> None:
        """Imprime una fila de tarjetas alineadas y centradas."""
        tarjetas = [self._crear_tarjeta(producto) for producto in productos]

        # Todas las tarjetas tienen el mismo alto, pero se rellena por
        # seguridad en caso de que en el futuro cambie el diseño.
        for tarjeta in tarjetas:
            while len(tarjeta) < self.ALTO_TARJETA:
                tarjeta.append(" " * self.ANCHO_TARJETA)

        ancho_fila = len(tarjetas) * self.ANCHO_TARJETA
        ancho_fila += (len(tarjetas) - 1) * self.SEPARACION
        margen = " " * max(0, (ancho - ancho_fila) // 2)
        separador = " " * self.SEPARACION

        # Se recorre línea por línea para unir las tarjetas horizontalmente.
        for numero_linea in range(self.ALTO_TARJETA):
            linea = separador.join(
                tarjeta[numero_linea] for tarjeta in tarjetas
            )
            print(margen + linea)

        print()

    def _crear_tarjeta(self, producto: CategoriaProducto) -> list[str]:
        """
        Construye una tarjeta de 9 líneas:

        +--------------------------------+
        | [IMG] nombre_imagen.jpg        |
        |                                |
        | Nombre del servicio            |
        | (segunda línea si es necesario)|
        | $ 120.000,00                   |
        |                                |
        | ID 1 | Ver detalle             |
        +--------------------------------+
        """
        borde_superior = "┌" + "─" * (self.ANCHO_TARJETA - 2) + "┐"
        borde_inferior = "└" + "─" * (self.ANCHO_TARJETA - 2) + "┘"

        # La imagen no se puede mostrar en una consola de texto, así que se
        # simula con una etiqueta [IMG] y el nombre del archivo.
        nombre_imagen = producto.url_imagen.rsplit("/", 1)[-1] or "sin-imagen"
        texto_imagen = f"[IMG] {abreviar(nombre_imagen, self.ANCHO_TEXTO - 6)}"

        # El nombre se reparte en máximo dos líneas para no romper la tarjeta.
        lineas_nombre = self._envolver(producto.nombre, max_lineas=2)

        lineas = [
            borde_superior,
            self._linea(texto_imagen),
            self._linea(""),
            self._linea(lineas_nombre[0]),
            self._linea(lineas_nombre[1]),
            self._linea(formatear_precio(producto.precio_promedio)),
            self._linea(""),
            self._linea(f"ID {producto.id} | Ver detalle"),
            borde_inferior,
        ]
        return lineas

    def _linea(self, texto: str) -> str:
        """Rodea un texto con los bordes laterales de la tarjeta."""
        return f"│ {texto.ljust(self.ANCHO_TEXTO)} │"

    def _envolver(self, texto: str, max_lineas: int) -> list[str]:
        """
        Divide un texto en líneas y garantiza que haya exactamente
        `max_lineas` elementos (rellena con cadenas vacías).
        """
        lineas = textwrap.wrap(texto, width=self.ANCHO_TEXTO) or [""]

        if len(lineas) > max_lineas:
            # Si hay más líneas de las permitidas, se conserva la última
            # parte abreviada para no perder el final del nombre.
            resto = " ".join(lineas[max_lineas - 1 :])
            lineas = lineas[: max_lineas - 1] + [
                abreviar(resto, self.ANCHO_TEXTO)
            ]

        return lineas + [""] * (max_lineas - len(lineas))
