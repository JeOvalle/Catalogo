"""
Utilidades de formato para las vistas de consola.

Se separan de las vistas para no repetir código y para que el formato de
precios o el recorte de textos se pueda cambiar en un solo lugar.
"""

from __future__ import annotations

import shutil

# Límites para que la interfaz se vea bien en ventanas pequeñas o muy grandes.
ANCHO_MINIMO = 60
ANCHO_MAXIMO = 120


def ancho_consola() -> int:
    """
    Devuelve el ancho de la terminal, limitado a un rango legible.

    shutil.get_terminal_size() funciona en Windows, Linux y macOS. El valor
    "fallback" se usa cuando Python no puede detectar el tamaño real.
    """
    ancho = shutil.get_terminal_size(fallback=(100, 30)).columns
    return max(ANCHO_MINIMO, min(ANCHO_MAXIMO, ancho))


def formatear_precio(valor: float) -> str:
    """
    Formatea un número como precio con separador de miles y dos decimales.

    Ejemplo: 120000.0 -> "$ 120.000,00"
    """
    # Primero se usa el formato estándar de Python: 120,000.00
    texto = f"{valor:,.2f}"

    # Luego se intercambian los separadores para el formato en español:
    # 120.000,00. La "X" es un separador temporal para no pisar valores.
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"$ {texto}"


def abreviar(texto: str, ancho: int) -> str:
    """
    Recorta un texto y agrega "..." cuando supera el ancho permitido.

    Se usa para nombres de archivo, URLs y nombres largos en las tarjetas.
    """
    if ancho <= 0:
        return ""
    if len(texto) <= ancho:
        return texto
    if ancho <= 3:
        return texto[:ancho]
    return texto[: ancho - 3] + "..."
