/**
 * VistaDetalleProducto: pantalla ampliada de un servicio.
 *
 * Se encarga de pedir un producto por id y construir la ficha de detalle
 * con imagen, título, precio, descripción y acciones simuladas.
 */

import {
  escaparHtml,
  formatearCuota,
  formatearPrecio,
} from "../utils/formato.js";
import { mostrarNotificacion } from "../utils/notificaciones.js";

const IMAGEN_PLACEHOLDER = "/static/img/placeholder.svg";

const BENEFICIOS_POR_CATEGORIA = {
  Escritura: [
    "Revisión de redacción, ortografía y citas",
    "Entrega en Word y PDF",
  ],
  Ciencias: [
    "Datos y cálculos explicados paso a paso",
    "Informe técnico estructurado",
  ],
  Tecnología: [
    "Código comentado y documentación",
    "Guía de instalación y uso",
  ],
  Asesoría: [
    "Sesión personalizada de 60 minutos",
    "Material de apoyo incluido",
  ],
  Diseño: [
    "Archivo editable incluido",
    "Diseño adaptado a tu exposición",
  ],
};

export class VistaDetalleProducto {
  #servicio;
  #contenedor;
  #ultimoId = null;

  constructor(servicio, contenedor) {
    if (
      !servicio ||
      typeof servicio.buscarPorId !== "function"
    ) {
      throw new TypeError(
        "VistaDetalleProducto necesita un servicio que implemente ICatalogoServicio.",
      );
    }

    if (!(contenedor instanceof HTMLElement)) {
      throw new TypeError(
        "VistaDetalleProducto necesita un contenedor HTML válido.",
      );
    }

    this.#servicio = servicio;
    this.#contenedor = contenedor;
  }

  /**
   * Carga y renderiza un producto.
   * @param {number} id
   * @returns {Promise<object|null>} producto encontrado o null.
   */
  async mostrar(id) {
    this.#ultimoId = id;
    this.#contenedor.hidden = false;
    this.#contenedor.innerHTML = this.#plantillaEsqueleto();

    try {
      const producto = await this.#servicio.buscarPorId(id);

      if (!producto) {
        this.#pintarNoEncontrado(id);
        return null;
      }

      this.#pintarProducto(producto);
      return producto;
    } catch (error) {
      this.#pintarError(error.message);
      return null;
    }
  }

  // ------------------------------------------------------------------
  // Renderizado
  // ------------------------------------------------------------------

  #pintarProducto(producto) {
    const id = Number(producto.id);
    const nombre = escaparHtml(producto.nombre);
    const categoria = escaparHtml(producto.categoria || "General");
    const descripcion = escaparHtml(producto.descripcion);
    const imagen = escaparHtml(producto.url_imagen || IMAGEN_PLACEHOLDER);
    const precio = formatearPrecio(producto.precio_promedio);
    const cuota = formatearCuota(producto.precio_promedio);
    const beneficios = this.#obtenerBeneficios(producto.categoria);

    this.#contenedor.innerHTML = `
      <nav class="breadcrumb" aria-label="Ruta de navegación">
        <a href="#/">Inicio</a>
        <span class="breadcrumb__sep" aria-hidden="true">›</span>
        <span>${categoria}</span>
        <span class="breadcrumb__sep" aria-hidden="true">›</span>
        <strong>${nombre}</strong>
      </nav>

      <article class="detail-card">
        <div class="detail-gallery">
          <img
            src="${imagen}"
            alt="${nombre}"
            decoding="async"
            data-imagen
          >
        </div>

        <div class="detail-info">
          <p class="detail-info__eyebrow">
            <span>${categoria}</span> · Servicio verificado
          </p>
          <h1>${nombre}</h1>

          <div class="detail-rating">
            <span class="stars" aria-hidden="true">★★★★★</span>
            <strong>4.9</strong>
            <span class="sr-only">de 5 estrellas</span>
            <span aria-hidden="true">·</span>
            <span>Valoración promedio</span>
          </div>

          <p class="detail-price">${precio}</p>
          <p class="detail-installments">en 3 cuotas de ${cuota} sin interés</p>
          <p class="detail-stock">
            <span class="detail-stock__dot" aria-hidden="true"></span>
            Disponible · Entrega coordinada con el especialista
          </p>

          <hr class="detail-divider">

          <section class="detail-description">
            <h2>Descripción</h2>
            <p>${descripcion}</p>
          </section>

          <section class="detail-features">
            <h2>Este servicio incluye</h2>
            <ul>
              ${beneficios.map((beneficio) => `<li>${escaparHtml(beneficio)}</li>`).join("")}
            </ul>
          </section>

          <div class="detail-actions">
            <button class="btn btn--primary" type="button" data-accion="contratar">
              Contratar servicio
            </button>
            <button class="btn btn--secondary" type="button" data-accion="guardar">
              Guardar
            </button>
          </div>

          <div class="seller-card">
            <div class="seller-avatar" aria-hidden="true">AM</div>
            <div class="seller-info">
              <strong>AcademiaMarket</strong>
              <span>Vendedor verificado · Respuesta en menos de 24 h</span>
            </div>
            <span class="seller-badge">Excelente</span>
          </div>
        </div>
      </article>

      <div class="detail-back">
        <a class="link-back" href="#/">← Volver al catálogo</a>
      </div>
    `;

    this.#conectarAcciones(producto, id);
    this.#conectarImagenDeRespaldo();
  }

  #obtenerBeneficios(categoria) {
    const especificos = BENEFICIOS_POR_CATEGORIA[categoria] || [];
    const generales = [
      "Acompañamiento de un especialista",
      "Una ronda de revisiones incluida",
    ];

    return [...new Set([...especificos, ...generales])].slice(0, 4);
  }

  #conectarAcciones(producto, id) {
    const botonContratar = this.#contenedor.querySelector(
      "[data-accion='contratar']",
    );
    const botonGuardar = this.#contenedor.querySelector(
      "[data-accion='guardar']",
    );

    botonContratar?.addEventListener("click", () => {
      botonContratar.disabled = true;
      botonContratar.textContent = "Solicitud enviada ✓";
      mostrarNotificacion(
        `Solicitud simulada para «${producto.nombre}». Un asesor te contactaría.`,
        "exito",
      );
    });

    botonGuardar?.addEventListener("click", () => {
      const guardado = botonGuardar.dataset.guardado === "true";
      botonGuardar.dataset.guardado = String(!guardado);
      botonGuardar.textContent = guardado ? "Guardar" : "Guardado ✓";
      mostrarNotificacion(
        guardado
          ? `Se quitó «${producto.nombre}» de tus guardados.`
          : `«${producto.nombre}» se guardó en tu lista simulada.`,
      );
    });

    // El id se deja disponible para futuras acciones (carrito, historial).
    this.#contenedor.dataset.productoId = String(id);
  }

  #conectarImagenDeRespaldo() {
    const imagen = this.#contenedor.querySelector("img[data-imagen]");
    imagen?.addEventListener(
      "error",
      () => {
        imagen.src = IMAGEN_PLACEHOLDER;
      },
      { once: true },
    );
  }

  #pintarNoEncontrado(id) {
    this.#contenedor.innerHTML = `
      <div class="error-state">
        <div class="error-state__icon" aria-hidden="true">?</div>
        <h3>Servicio no encontrado</h3>
        <p>No existe un producto con el ID ${escaparHtml(id)} en el catálogo.</p>
        <a class="btn btn--primary" href="#/">Volver al catálogo</a>
      </div>
    `;
  }

  #pintarError(mensaje) {
    this.#contenedor.innerHTML = `
      <div class="error-state">
        <div class="error-state__icon" aria-hidden="true">!</div>
        <h3>No pudimos cargar el detalle</h3>
        <p>${escaparHtml(mensaje || "Ocurrió un error inesperado.")}</p>
        <button class="btn btn--primary" type="button" data-accion="reintentar">
          Reintentar
        </button>
      </div>
    `;

    this.#contenedor
      .querySelector("[data-accion='reintentar']")
      ?.addEventListener("click", () => this.mostrar(this.#ultimoId));
  }

  #plantillaEsqueleto() {
    return `
      <div class="skeleton-detail" aria-label="Cargando detalle del servicio">
        <div class="skeleton-detail__media skeleton-shimmer"></div>
        <div class="skeleton-detail__info">
          <div class="skeleton-line skeleton-line--sm skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-line--lg skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-line--lg skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-line--price skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-line--lg skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-line--lg skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-line--sm skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-line--price skeleton-shimmer"></div>
        </div>
      </div>
    `;
  }
}
