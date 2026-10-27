/**
 * Funciones de formato y seguridad para el frontend.
 * Se mantienen separadas de las vistas para reutilizarlas en toda la SPA.
 */

const formatoMoneda = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency: "COP",
  maximumFractionDigits: 0,
});

/** Formatea un número como precio en pesos colombianos. */
export function formatearPrecio(valor) {
  return formatoMoneda.format(Number(valor) || 0);
}

/** Calcula y formatea una cuota sin interés. */
export function formatearCuota(precio, numeroCuotas = 3) {
  return formatearPrecio((Number(precio) || 0) / numeroCuotas);
}

/** Escapa texto para insertarlo con seguridad dentro de HTML. */
export function escaparHtml(texto) {
  return String(texto ?? "").replace(/[&<>"']/g, (caracter) => {
    const entidades = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return entidades[caracter];
  });
}

/** Recorta un texto largo y agrega puntos suspensivos. */
export function truncar(texto, maximo = 90) {
  const limpio = String(texto ?? "").trim();
  if (limpio.length <= maximo) return limpio;
  return `${limpio.slice(0, maximo - 1).trimEnd()}…`;
}

/**
 * Normaliza texto para búsquedas: minúsculas y sin tildes.
 * Ejemplo: "Química" -> "quimica".
 */
export function normalizarTexto(texto) {
  return String(texto ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}
