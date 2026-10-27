/**
 * Contrato del servicio de catálogo en el frontend.
 *
 * JavaScript no tiene interfaces nativas como Java o C#. Para mantener el
 * mismo concepto de arquitectura se usa esta clase abstracta "manual":
 * - No se puede instanciar directamente.
 * - Declara los métodos que debe implementar cualquier servicio concreto.
 * - La vista depende de este contrato, no de una implementación concreta.
 */

export class ICatalogoServicio {
  constructor() {
    if (new.target === ICatalogoServicio) {
      throw new TypeError(
        "ICatalogoServicio es una interfaz: crea una implementación concreta.",
      );
    }
  }

  /** @returns {Promise<Array<object>>} */
  async obtenerTodos() {
    throw new Error("Método no implementado: obtenerTodos()");
  }

  /** @param {number} _id @returns {Promise<object|null>} */
  async buscarPorId(_id) {
    throw new Error("Método no implementado: buscarPorId()");
  }

  /** @param {object} _producto @returns {Promise<object>} */
  async registrarProducto(_producto) {
    throw new Error("Método no implementado: registrarProducto()");
  }

  /** @param {number} _id @returns {Promise<void>} */
  async eliminarProducto(_id) {
    throw new Error("Método no implementado: eliminarProducto()");
  }
}
