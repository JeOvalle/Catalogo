/**
 * Aplicación principal (controlador de la SPA).
 *
 * Orquesta las dos vistas y el estado de navegación:
 *   #/                 -> cuadrícula
 *   #/producto/<id>    -> detalle
 *
 * La app solo conoce la interfaz ICatalogoServicio y las vistas. La forma
 * de obtener los datos (API Flask) queda encapsulada en CatalogoApiServicio.
 */

import { CatalogoApiServicio } from "./services/CatalogoApiServicio.js";
import { mostrarNotificacion } from "./utils/notificaciones.js";
import { VistaCuadricula } from "./views/VistaCuadricula.js";
import { VistaDetalleProducto } from "./views/VistaDetalleProducto.js";

class Aplicacion {
  #servicio;
  #vistaCuadricula;
  #vistaDetalle;
  #filtros = { texto: "", categoria: "Todas" };
  #elementos;
  #temporizadorBusqueda = null;
  #tokenRuta = 0;

  constructor() {
    this.#servicio = new CatalogoApiServicio("/api");

    const buscar = (selector) => document.querySelector(selector);
    this.#elementos = {
      catalogo: buscar("#catalogo-view"),
      detalle: buscar("#detalle-view"),
      hero: buscar("#hero"),
      formularioBusqueda: buscar("#search-form"),
      entradaBusqueda: buscar("#search-input"),
      navCategorias: buscar("#category-nav"),
      botonExplorar: buscar("#explorar-btn"),
      anio: buscar("#anio"),
    };
  }

  async iniciar() {
    if (!this.#elementos.catalogo || !this.#elementos.detalle) {
      throw new Error("No se encontraron los contenedores principales de la SPA.");
    }

    this.#vistaCuadricula = new VistaCuadricula(
      this.#servicio,
      this.#elementos.catalogo,
    );
    this.#vistaDetalle = new VistaDetalleProducto(
      this.#servicio,
      this.#elementos.detalle,
    );

    this.#configurarEventos();
    this.#escribirAnio();

    // Primera carga del catálogo. El evento "catalogo:cargado" construye
    // los filtros de categoría de la cabecera.
    await this.#vistaCuadricula.mostrar();

    window.addEventListener("hashchange", () => {
      this.#enrutar();
    });

    await this.#enrutar();
  }

  // ------------------------------------------------------------------
  // Eventos globales
  // ------------------------------------------------------------------

  #configurarEventos() {
    // Búsqueda: filtra en vivo y, al enviar, vuelve al catálogo.
    this.#elementos.formularioBusqueda?.addEventListener("submit", (evento) => {
      evento.preventDefault();
      window.clearTimeout(this.#temporizadorBusqueda);
      this.#aplicarBusqueda(this.#elementos.entradaBusqueda?.value || "");

      if (this.#esRutaDetalle()) {
        window.location.hash = "#/";
      } else {
        this.#desplazarAlCatalogo();
      }
    });

    this.#elementos.entradaBusqueda?.addEventListener("input", (evento) => {
      window.clearTimeout(this.#temporizadorBusqueda);
      const valor = evento.target.value;

      // Pequeño debounce para no repintar en cada tecla.
      this.#temporizadorBusqueda = window.setTimeout(() => {
        this.#aplicarBusqueda(valor);
      }, 170);
    });

    // Filtros de categoría (delegación de eventos).
    this.#elementos.navCategorias?.addEventListener("click", (evento) => {
      const boton = evento.target.closest("[data-categoria]");
      if (!boton) return;

      this.#filtros.categoria = boton.dataset.categoria;
      this.#sincronizarChips();

      if (this.#esRutaDetalle()) {
        window.location.hash = "#/";
      } else {
        this.#vistaCuadricula.aplicarFiltros(this.#filtros);
        this.#desplazarAlCatalogo();
      }
    });

    // La vista avisa cuando terminó de cargar y entrega sus categorías.
    this.#elementos.catalogo?.addEventListener("catalogo:cargado", (evento) => {
      this.#actualizarCategorias(evento.detail?.categorias || []);
    });

    this.#elementos.catalogo?.addEventListener(
      "catalogo:limpiar-filtros",
      () => this.#limpiarFiltros(),
    );

    this.#elementos.botonExplorar?.addEventListener("click", () => {
      this.#desplazarAlCatalogo();
    });

    // Acciones decorativas de la cabecera (vender, ayuda, carrito).
    document.addEventListener("click", (evento) => {
      const boton = evento.target.closest("[data-simulado]");
      if (!boton) return;
      mostrarNotificacion(boton.dataset.simulado);
    });
  }

  // ------------------------------------------------------------------
  // Filtros
  // ------------------------------------------------------------------

  #aplicarBusqueda(texto) {
    this.#filtros.texto = texto;
    this.#vistaCuadricula.aplicarFiltros({ texto });
  }

  #limpiarFiltros() {
    this.#filtros = { texto: "", categoria: "Todas" };

    if (this.#elementos.entradaBusqueda) {
      this.#elementos.entradaBusqueda.value = "";
    }

    this.#sincronizarChips();
    this.#vistaCuadricula.aplicarFiltros(this.#filtros);
  }

  #actualizarCategorias(categorias) {
    if (!this.#elementos.navCategorias) return;

    const todas = ["Todas", ...categorias];
    const botones = todas.map((categoria) => {
      const boton = document.createElement("button");
      boton.type = "button";
      boton.className = "category-chip";
      boton.dataset.categoria = categoria;
      boton.textContent = categoria;

      if (categoria === this.#filtros.categoria) {
        boton.classList.add("is-active");
      }

      return boton;
    });

    this.#elementos.navCategorias.replaceChildren(...botones);
  }

  #sincronizarChips() {
    this.#elementos.navCategorias
      ?.querySelectorAll("[data-categoria]")
      .forEach((boton) => {
        const activa = boton.dataset.categoria === this.#filtros.categoria;
        boton.classList.toggle("is-active", activa);
      });
  }

  // ------------------------------------------------------------------
  // Router basado en hash
  // ------------------------------------------------------------------

  async #enrutar() {
    const token = ++this.#tokenRuta;
    const coincidencia = window.location.hash.match(/^#\/producto\/(\d+)$/);

    if (coincidencia) {
      this.#elementos.hero.hidden = true;
      this.#elementos.catalogo.hidden = true;
      this.#elementos.detalle.hidden = false;

      const id = Number(coincidencia[1]);
      const producto = await this.#vistaDetalle.mostrar(id);

      if (token !== this.#tokenRuta) return;

      document.title = producto
        ? `${producto.nombre} | AcademiaMarket`
        : "Servicio no encontrado | AcademiaMarket";

      window.scrollTo(0, 0);
      return;
    }

    // Cualquier otra ruta vuelve a la cuadrícula.
    this.#elementos.detalle.hidden = true;
    this.#elementos.hero.hidden = false;
    this.#elementos.catalogo.hidden = false;
    this.#vistaCuadricula.aplicarFiltros(this.#filtros);
    document.title = "AcademiaMarket | Servicios académicos";
    window.scrollTo(0, 0);
  }

  #esRutaDetalle() {
    return /^#\/producto\/\d+$/.test(window.location.hash);
  }

  // ------------------------------------------------------------------
  // Utilidades de interfaz
  // ------------------------------------------------------------------

  #desplazarAlCatalogo() {
    window.setTimeout(() => {
      this.#elementos.catalogo?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 40);
  }

  #escribirAnio() {
    if (this.#elementos.anio) {
      this.#elementos.anio.textContent = String(new Date().getFullYear());
    }
  }
}

// Punto de arranque de la SPA.
const aplicacion = new Aplicacion();
aplicacion.iniciar().catch((error) => {
  console.error("Error al iniciar la aplicación:", error);
  const catalogo = document.querySelector("#catalogo-view");
  if (catalogo) {
    catalogo.innerHTML = `
      <div class="error-state">
        <div class="error-state__icon" aria-hidden="true">!</div>
        <h3>No pudimos iniciar el catálogo</h3>
        <p>Revisa que el servidor Flask esté ejecutándose y recarga la página.</p>
      </div>
    `;
  }
});
