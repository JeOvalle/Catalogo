/**
 * Implementación del contrato ICatalogoServicio que consume la API Flask.
 *
 * Es el único archivo del frontend que conoce las URLs HTTP. Si mañana
 * cambia el backend (otra ruta, otro servidor), solo se modifica esta clase.
 */

import { ICatalogoServicio } from "./ICatalogoServicio.js";

export class CatalogoApiServicio extends ICatalogoServicio {
  #baseUrl;

  constructor(baseUrl = "/api") {
    super();
    this.#baseUrl = baseUrl.replace(/\/$/, "");
  }

  async obtenerTodos() {
    return this.#solicitar("/productos");
  }

  async buscarPorId(id) {
    try {
      return await this.#solicitar(`/productos/${encodeURIComponent(id)}`);
    } catch (error) {
      // Para la vista, un 404 significa "producto no encontrado", no un fallo.
      if (error.status === 404) return null;
      throw error;
    }
  }

  async registrarProducto(producto) {
    return this.#solicitar("/productos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(producto),
    });
  }

  async eliminarProducto(id) {
    await this.#solicitar(`/productos/${encodeURIComponent(id)}`, {
      method: "DELETE",
    });
  }

  /**
   * Realiza una petición HTTP y normaliza la respuesta.
   * @param {string} ruta
   * @param {RequestInit} opciones
   */
  async #solicitar(ruta, { headers = {}, ...opciones } = {}) {
    const respuesta = await fetch(`${this.#baseUrl}${ruta}`, {
      ...opciones,
      headers: {
        Accept: "application/json",
        ...headers,
      },
    });

    let datos = null;

    if (respuesta.status !== 204) {
      const tipoContenido = respuesta.headers.get("content-type") || "";
      datos = tipoContenido.includes("application/json")
        ? await respuesta.json()
        : await respuesta.text();
    }

    if (!respuesta.ok) {
      const mensaje =
        datos && typeof datos === "object" && datos.error
          ? datos.error
          : `No se pudo completar la solicitud (código ${respuesta.status}).`;

      const error = new Error(mensaje);
      error.status = respuesta.status;
      throw error;
    }

    return datos;
  }
}
