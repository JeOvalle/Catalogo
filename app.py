"""
Punto de entrada de la versión web.

Ejecutar desde la carpeta Catalogo:
    python app.py

Luego abrir en el navegador:
    http://127.0.0.1:5000
"""

from web.app import crear_app

app = crear_app()


if __name__ == "__main__":
    # debug=True recarga el servidor al guardar cambios durante el desarrollo.
    app.run(host="127.0.0.1", port=5000, debug=True)
