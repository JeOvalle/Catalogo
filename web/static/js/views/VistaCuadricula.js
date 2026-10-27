/**
 * VistaCuadricula: pantalla principal tipo marketplace.
 *
 * Responsabilidades:
 * - Consumir el contrato ICatalogoServicio.
 * - Mostrar los productos en tarjetas.
 * - Aplicar búsqueda, filtro por categoría y ordenamiento.
 *
 * La vista no conoce Flask ni las URLs de la API: solo usa el servicio.
 */

import {
  escaparHtml,
  formatearCuota,
  formatearPrecio,
  normalizarTexto,
  truncar,
} from "../utils/formato.js";

const IMAGEN_PLACEHOLDER = "/static/img/placeholder.svg";

export class VistaCuadricula {
  #servicio;
  #contenedor;
  #productos = [];
  #filtros = {
    texto: "",
    categoria: "Todas",
    orden: "relevancia",
  };

  constructor(servicio, contenedor) {
    if (
      !servicio ||
      typeof servicio.obtenerTodos !== "function" ||
      typeof servicio.buscarPorId !== "function"
    ) {
      throw new TypeError(
        "VistaCuadricula necesita un servicio que implemente ICatalogoServicio.",
      );
    }

    if (!(contenedor instanceof HTMLElement)) {
      throw new TypeError("VistaCuadricula necesita un contenedor HTML válido.");
    }

    this.#servicio = servicio;
    this.#contenedor = contenedor;
  }

  /** Categorías disponibles, sin repetir y en orden de aparición. */
  get categorias() {
    return [
      ...new Set(
        this.#productos
          .map((producto) => producto.categoria)
          .filter(Boolean),
      ),
    ];
  }

  get total() {
    return this.#productos.length;
  }

  /** Carga los datos y dibuja el catálogo. */
  async mostrar() {
    this.#contenedor.innerHTML = this.#plantillaEsqueleto();

    try {
      this.#productos = await this.#servicio.obtenerTodos();
      this.#pintar();

      // La app escucha este evento para construir los filtros del header.
      this.#contenedor.dispatchEvent(
        new CustomEvent("catalogo:cargado", {
          bubbles: true,
          detail: { categorias: this.categorias, total: this.total },
        }),
      );
    } catch (error) {
      this.#pintarError(error.message);
    }
  }

  /**
   * Actualiza los filtros y vuelve a pintar sin pedir datos de nuevo.
   * @param {{texto?: string, categoria?: string, orden?: string}} filtros
   */
  aplicarFiltros(filtros = {}) {
    this.#filtros = { ...this.#filtros, ...filtros };
    this.#pintar();
  }

  // ------------------------------------------------------------------
  // Renderizado principal
  // ------------------------------------------------------------------

  #pintar() {
    const visibles = this.#obtenerVisibles();
    const total = this.#productos.length;
    const cantidad = visibles.length;

    const textoCantidad =
      total === 0
        ? "No hay servicios disponibles"
        : cantidad === total
          ? `${total} ${total === 1 ? "servicio disponible" : "servicios disponibles"}`
          : `${cantidad} de ${total} servicios`;

    this.#contenedor.innerHTML = `
      <div class="catalog-toolbar">
        <div>
          <p class="catalog-toolbar__eyebrow">MARKETPLACE ACADÉMICO</p>
          <h2>Servicios académicos</h2>
          <p class="catalog-toolbar__count" aria-live="polite">${textoCantidad}</p>
        </div>
        <label class="sort">
          Ordenar por
          <select id="sort-select" aria-label="Ordenar los servicios">
            ${this.#opcionOrden("relevancia", "Relevancia")}
            ${this.#opcionOrden("precio-asc", "Menor precio")}
            ${this.#opcionOrden("precio-desc", "Mayor precio")}
            ${this.#opcionOrden("nombre", "Nombre A-Z")}
          </select>
        </label>
      </div>
      ${
        visibles.length > 0
          ? `<div class="product-grid">${visibles
              .map((producto) => this.#plantillaTarjeta(producto))
              .join("")}</div>`
          : this.#plantillaVacio(total === 0)
      }
    `;

    this.#conectarEventos();
    this.#conectarImagenesDeRespaldo();
  }

  #obtenerVisibles() {
    const texto = normalizarTexto(this.#filtros.texto);
    const categoria = this.#filtros.categoria;

    const filtrados = this.#productos.filter((producto) => {
      const coincideCategoria =
        !categoria || categoria === "Todas" || producto.categoria === categoria;

      if (!coincideCategoria) return false;
      if (!texto) return true;

      const contenido = normalizarTexto(
        `${producto.nombre} ${producto.descripcion} ${producto.categoria}`,
      );
      return contenido.includes(texto);
    });

    return [...filtrados].sort((a, b) => {
      switch (this.#filtros.orden) {
        case "precio-asc":
          return Number(a.precio_promedio) - Number(b.precio_promedio);
        case "precio-desc":
          return Number(b.precio_promedio) - Number(a.precio_promedio);
        case "nombre":
          return String(a.nombre).localeCompare(String(b.nombre), "es");
        default:
          return Number(a.id) - Number(b.id);
      }
    });
  }

  #conectarEventos() {
    const selectorOrden = this.#contenedor.querySelector("#sort-select");
    selectorOrden?.addEventListener("change", (evento) => {
      this.#filtros.orden = evento.target.value;
      this.#pintar();
    });

    this.#contenedor
      .querySelector("[data-accion='limpiar-filtros']")
      ?.addEventListener("click", () => {
        this.#contenedor.dispatchEvent(
          new CustomEvent("catalogo:limpiar-filtros", { bubbles: true }),
        );
      });
  }

  /**
   * Si una imagen no existe, se reemplaza por el placeholder local.
   * Se hace con addEventListener para no usar JavaScript inline en HTML.
   */
  #conectarImagenesDeRespaldo() {
    this.#contenedor.querySelectorAll("img[data-imagen]").forEach((imagen) => {
      imagen.addEventListener(
        "error",
        () => {
          imagen.src = IMAGEN_PLACEHOLDER;
        },
        { once: true },
      );
    });
  }

  // ------------------------------------------------------------------
  // Plantillas HTML
  // ------------------------------------------------------------------

  #opcionOrden(valor, texto) {
    const seleccionado = this.#filtros.orden === valor ? "selected" : "";
    return `<option value="${valor}" ${seleccionado}>${texto}</option>`;
  }

  #plantillaTarjeta(producto) {
    const id = Number(producto.id);
    const nombre = escaparHtml(producto.nombre);
    const categoria = escaparHtml(producto.categoria || "General");
    const descripcion = escaparHtml(truncar(producto.descripcion, 92));
    const precio = formatearPrecio(producto.precio_promedio);
    const cuota = formatearCuota(producto.precio_promedio);
    const imagen = escaparHtml(producto.url_imagen || IMAGEN_PLACEHOLDER);

    return `
      <a class="product-card" href="#/producto/${id}">
        <div class="product-card__media">
          <img
            src="${imagen}"
            alt="${nombre}"
            loading="lazy"
            decoding="async"
            data-imagen
          >
          <span class="product-card__badge">VERIFICADO</span>
        </div>
        <div class="product-card__body">
          <span class="product-card__category">${categoria}</span>
          <h3 class="product-card__title">${nombre}</h3>
          <p class="product-card__desc">${descripcion}</p>
          <p class="product-card__price">${precio}</p>
          <p class="product-card__installments">3 cuotas de ${cuota} sin interés</p>
          <span class="product-card__shipping">Entrega coordinada</span>
          <span class="product-card__cta">Ver detalle <span aria-hidden="true">→</span></span>
        </div>
      </a>
    `;
  }

  #plantillaVacio(catalogoVacio) {
    return `
      <div class="empty-state">
        <div class="empty-state__icon" aria-hidden="true">⌕</div>
        <h3>${catalogoVacio ? "El catálogo está vacío" : "No encontramos servicios"}</h3>
        <p>
          ${
            catalogoVacio
              ? "Todavía no hay productos registrados en el catálogo."
              : "Prueba con otra palabra clave o cambia la categoría seleccionada."
          }
        </p>
        ${
          catalogoVacio
            ? ""
            : '<button class="btn btn--primary" type="button" data-accion="limpiar-filtros">Limpiar filtros</button>'
        }
      </div>
    `;
  }

  #plantillaEsqueleto() {
    const tarjetas = Array.from(
      { length: 8 },
      () => `
        <div class="skeleton-card" aria-hidden="true">
          <div class="skeleton-card__media skeleton-shimmer"></div>
          <div class="skeleton-card__body">
            <div class="skeleton-line skeleton-line--sm skeleton-shimmer"></div>
            <div class="skeleton-line skeleton-line--lg skeleton-shimmer"></div>
            <div class="skeleton-line skeleton-line--lg skeleton-shimmer"></div>
            <div class="skeleton-line skeleton-line--price skeleton-shimmer"></div>
            <div class="skeleton-line skeleton-line--sm skeleton-shimmer"></div>
          </div>
        </div>
      `,
    ).join("");

    return `
      <div class="catalog-toolbar">
        <div>
          <p class="catalog-toolbar__eyebrow">MARKETPLACE ACADÉMICO</p>
          <h2>Servicios académicos</h2>
          <p class="catalog-toolbar__count">Cargando servicios...</p>
        </div>
      </div>
      <div class="skeleton-grid" aria-label="Cargando catálogo">${tarjetas}</div>
    `;
  }

  #pintarError(mensaje) {
    const detalle = escaparHtml(
      mensaje || "No fue posible cargar el catálogo. Intenta de nuevo.",
    );

    this.#contenedor.innerHTML = `
      <div class="error-state">
        <div class="error-state__icon" aria-hidden="true">!</div>
        <h3>No pudimos cargar el catálogo</h3>
        <p>${detalle}</p>
        <button class="btn btn--primary" type="button" data-accion="reintentar">
          Reintentar
        </button>
      </div>
    `;

    this.#contenedor
      .querySelector("[data-accion='reintentar']")
      ?.addEventListener("click", () => this.mostrar());
  }
}
