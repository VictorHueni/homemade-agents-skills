/*
 * com-artefact-viz runtime — vanilla JS, no dependencies.
 * Inlined into every rendered view. All behaviour is progressive: a view with
 * none of these hooks present still renders correctly as static HTML.
 */
(function () {
  "use strict";

  /* ---- Collapsible tree nodes (FBS, capability map) ---------------------- */
  // A node toggle is any element with [data-toggle]; it flips .is-collapsed on
  // the closest [data-node] ancestor, hiding that node's [data-children].
  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-toggle]");
    if (toggle) {
      var node = toggle.closest("[data-node]");
      if (node) {
        node.classList.toggle("is-collapsed");
        toggle.setAttribute(
          "aria-expanded",
          node.classList.contains("is-collapsed") ? "false" : "true"
        );
      }
      return;
    }

    /* ---- Generic detail disclosure (epic cards, capability cards) -------- */
    var disc = e.target.closest("[data-disclose]");
    if (disc) {
      var card = disc.closest("[data-card]");
      if (card) card.classList.toggle("is-open");
    }
  });

  /* ---- Toolbar actions --------------------------------------------------- */
  function setAll(collapsed) {
    document.querySelectorAll("[data-node]").forEach(function (n) {
      n.classList.toggle("is-collapsed", collapsed);
      var t = n.querySelector(":scope > * [data-toggle], :scope > [data-toggle]");
      if (t) t.setAttribute("aria-expanded", collapsed ? "false" : "true");
    });
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-action]");
    if (!btn) return;
    var action = btn.getAttribute("data-action");

    if (action === "expand-all") setAll(false);
    if (action === "collapse-all") setAll(true);

    if (action === "orient") {
      // Toggle horizontal <-> vertical on every [data-tree] root.
      var pressed = btn.getAttribute("aria-pressed") === "true";
      var horizontal = !pressed;
      btn.setAttribute("aria-pressed", String(horizontal));
      btn.textContent = horizontal ? "Orientation: horizontal" : "Orientation: vertical";
      document.querySelectorAll("[data-tree]").forEach(function (tree) {
        tree.classList.toggle("tree--horizontal", horizontal);
        tree.classList.toggle("tree--vertical", !horizontal);
      });
    }
  });
})();
