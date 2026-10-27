"""
Datos de ejemplo del catálogo.

Este módulo centraliza los productos de demostración para que la app web
y la antigua demo de consola usen exactamente la misma información.
"""

from __future__ import annotations

from domain.categoria_producto import CategoriaProducto
from services.impl.catalogo_servicio_memoria import CatalogoServicioMemoria


def crear_catalogo_ejemplo() -> CatalogoServicioMemoria:
    """
    Crea un catálogo en memoria con ocho servicios académicos.

    Las imágenes son SVG locales (web/static/img) para que la simulación
    funcione sin conexión a internet.
    """
    catalogo = CatalogoServicioMemoria()

    productos = (
        CategoriaProducto(
            id=1,
            nombre="Ensayo académico",
            descripcion=(
                "Redacción de ensayos argumentativos con normas APA: "
                "investigación de fuentes confiables, construcción de tesis, "
                "desarrollo de argumentos y revisión de estilo. Incluye una "
                "ronda de correcciones y entrega en formato Word y PDF."
            ),
            precio_promedio=120_000.0,
            url_imagen="/static/img/ensayo.svg",
            categoria="Escritura",
        ),
        CategoriaProducto(
            id=2,
            nombre="Laboratorio de química",
            descripcion=(
                "Desarrollo de prácticas de laboratorio con informe técnico "
                "completo: objetivos, materiales, procedimiento, datos "
                "experimentales, cálculos y conclusiones. Ideal para química "
                "general, orgánica y analítica."
            ),
            precio_promedio=185_000.0,
            url_imagen="/static/img/laboratorio.svg",
            categoria="Ciencias",
        ),
        CategoriaProducto(
            id=3,
            nombre="Proyecto de software",
            descripcion=(
                "Análisis, diseño e implementación de un proyecto de software "
                "con arquitectura por capas. Incluye documentación técnica, "
                "diagramas UML, código comentado y una guía de ejecución."
            ),
            precio_promedio=350_000.0,
            url_imagen="/static/img/software.svg",
            categoria="Tecnología",
        ),
        CategoriaProducto(
            id=4,
            nombre="Informe técnico",
            descripcion=(
                "Elaboración de informes técnicos y académicos con "
                "introducción, metodología, resultados, conclusiones y "
                "referencias bibliográficas. Se adapta al formato solicitado "
                "por tu institución."
            ),
            precio_promedio=95_000.0,
            url_imagen="/static/img/informe.svg",
            categoria="Escritura",
        ),
        CategoriaProducto(
            id=5,
            nombre="Tutoría especializada",
            descripcion=(
                "Acompañamiento personalizado de una hora para resolver dudas "
                "de programación, matemáticas o metodología de investigación. "
                "Incluye ejercicios prácticos y material de apoyo."
            ),
            precio_promedio=60_000.0,
            url_imagen="/static/img/tutoria.svg",
            categoria="Asesoría",
        ),
        CategoriaProducto(
            id=6,
            nombre="Presentación académica",
            descripcion=(
                "Diseño de diapositivas y guion para exposiciones académicas. "
                "Incluye organización del contenido, material visual, consejos "
                "de presentación y archivo editable."
            ),
            precio_promedio=80_000.0,
            url_imagen="/static/img/presentacion.svg",
            categoria="Diseño",
        ),
        CategoriaProducto(
            id=7,
            nombre="Traducción de textos",
            descripcion=(
                "Traducción académica entre español e inglés con revisión de "
                "terminología técnica. Se entrega el documento final y una "
                "versión con comentarios sobre las decisiones de traducción."
            ),
            precio_promedio=110_000.0,
            url_imagen="/static/img/traduccion.svg",
            categoria="Escritura",
        ),
        CategoriaProducto(
            id=8,
            nombre="Análisis de datos",
            descripcion=(
                "Procesamiento y visualización de datos para trabajos de "
                "investigación. Incluye limpieza del dataset, estadísticas "
                "descriptivas, gráficos y un informe con hallazgos."
            ),
            precio_promedio=220_000.0,
            url_imagen="/static/img/datos.svg",
            categoria="Tecnología",
        ),
    )

    for producto in productos:
        catalogo.registrar_producto(producto)

    return catalogo
