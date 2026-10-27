"""
Fábrica de la aplicación Flask.

Se usa el patrón "application factory" para poder inyectar una
implementación distinta de ICatalogoServicio (por ejemplo, una de pruebas)
sin tocar las rutas ni el frontend.
"""

from __future__ import annotations

from flask import Flask, render_template

from services.icatalogo_servicio import ICatalogoServicio
from services.impl.datos_ejemplo import crear_catalogo_ejemplo
from web.routes.catalogo_api import bp as catalogo_api_bp


def crear_app(catalogo_servicio: ICatalogoServicio | None = None) -> Flask:
    """
    Crea y configura la aplicación web.

    Args:
        catalogo_servicio: implementación opcional del contrato. Si no se
            entrega, se usa el catálogo en memoria con datos de ejemplo.
    """
    app = Flask(__name__)

    # JSON legible con tildes y caracteres especiales.
    app.json.ensure_ascii = False

    # Inyección de dependencias: las rutas leen el servicio desde aquí.
    app.extensions["catalogo_servicio"] = (
        catalogo_servicio or crear_catalogo_ejemplo()
    )

    app.register_blueprint(catalogo_api_bp)

    @app.get("/")
    def inicio():
        """Entrega el documento HTML de la aplicación (SPA)."""
        return render_template("index.html")

    return app
