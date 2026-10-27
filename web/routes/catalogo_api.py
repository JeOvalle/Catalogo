"""
API REST del catálogo.

Esta capa traduce HTTP <-> dominio. No contiene reglas de negocio: delega
todo en el servicio inyectado, que cumple la interfaz ICatalogoServicio.

Endpoints:
    GET    /api/productos          -> lista de productos
    GET    /api/productos/<id>     -> detalle de un producto
    POST   /api/productos          -> registra un producto (CRUD futuro)
    DELETE /api/productos/<id>     -> elimina un producto (CRUD futuro)
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from domain.categoria_producto import CategoriaProducto
from services.excepciones import ProductoDuplicadoError, ProductoNoEncontradoError
from services.icatalogo_servicio import ICatalogoServicio

bp = Blueprint("catalogo_api", __name__, url_prefix="/api")


def _servicio() -> ICatalogoServicio:
    """Recupera la implementación inyectada al crear la aplicación Flask."""
    return current_app.extensions["catalogo_servicio"]


def _error(mensaje: str, estado: int):
    """Respuesta JSON uniforme para los errores de la API."""
    return jsonify({"error": mensaje}), estado


@bp.get("/productos")
def listar_productos():
    """Devuelve todos los productos serializados como JSON."""
    productos = _servicio().obtener_todos()
    return jsonify([producto.obtener_info_completa() for producto in productos])


@bp.get("/productos/<int:id_producto>")
def obtener_producto(id_producto: int):
    """Devuelve un producto concreto o un 404 si no existe."""
    producto = _servicio().buscar_por_id(id_producto)

    if producto is None:
        return _error(f"No existe un producto con el id {id_producto}.", 404)

    return jsonify(producto.obtener_info_completa())


@bp.post("/productos")
def registrar_producto():
    """
    Registra un producto nuevo.

    Este endpoint no se usa todavía en la interfaz, pero demuestra que el
    contrato ICatalogoServicio quedó preparado para ampliar el CRUD sin
    modificar las vistas actuales.
    """
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return _error("El cuerpo de la solicitud debe ser un JSON válido.", 400)

    try:
        producto = CategoriaProducto(
            id=datos.get("id"),
            nombre=datos.get("nombre"),
            descripcion=datos.get("descripcion"),
            precio_promedio=datos.get("precio_promedio"),
            url_imagen=datos.get("url_imagen", ""),
            categoria=datos.get("categoria", "General"),
        )
    except (TypeError, ValueError) as error:
        return _error(str(error), 400)

    try:
        _servicio().registrar_producto(producto)
    except ProductoDuplicadoError as error:
        return _error(str(error), 409)

    return jsonify(producto.obtener_info_completa()), 201


@bp.delete("/productos/<int:id_producto>")
def eliminar_producto(id_producto: int):
    """Elimina un producto y responde 204 sin cuerpo."""
    try:
        _servicio().eliminar_producto(id_producto)
    except ProductoNoEncontradoError as error:
        return _error(str(error), 404)

    return "", 204
