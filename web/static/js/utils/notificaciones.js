/**
 * Notificaciones tipo toast.
 *
 * Se usan para dar retroalimentación en acciones simuladas (contratar,
 * guardar, carrito, etc.) sin recargar la página.
 */

import { escaparHtml } from "./formato.js";

export function mostrarNotificacion(mensaje, tipo = "info") {
  const raiz = document.querySelector("#toast-root");
  if (!raiz) return;

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.dataset.tipo = tipo;

  const icono = tipo === "exito" ? "✓" : "i";
  toast.innerHTML = `
    <span class="toast__icon" aria-hidden="true">${icono}</span>
    <span>${escaparHtml(mensaje)}</span>
  `;

  raiz.append(toast);

  // Se espera un frame para que el navegador aplique la transición.
  requestAnimationFrame(() => toast.classList.add("is-visible"));

  window.setTimeout(() => {
    toast.classList.remove("is-visible");
    window.setTimeout(() => toast.remove(), 260);
  }, 3400);
}
