/* Lightbox: click a plate to view it enlarged.
   Fit-to-screen first, click again for 1:1 pixels, Esc / backdrop / × to close. */
(function () {
  "use strict";

  var figs = Array.prototype.slice.call(document.querySelectorAll("figure.plate"));
  if (!figs.length) return;

  var overlay, stage, img, caption, hint, zoomed = false, lastFocus = null;
  var zh = document.documentElement.lang.indexOf("zh") === 0;

  function build() {
    overlay = document.createElement("div");
    overlay.className = "lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", zh ? "查看放大的图片" : "Enlarged image");

    var closeBtn = document.createElement("button");
    closeBtn.className = "lightbox-close";
    closeBtn.type = "button";
    closeBtn.setAttribute("aria-label", zh ? "关闭" : "Close");
    closeBtn.textContent = "×";

    stage = document.createElement("div");
    stage.className = "lightbox-stage";

    img = document.createElement("img");
    img.alt = "";

    caption = document.createElement("p");
    caption.className = "lightbox-caption";

    hint = document.createElement("p");
    hint.className = "lightbox-hint";
    hint.textContent = zh ? "点击图片查看原图 · Esc 关闭" : "Click the image for full size · Esc to close";

    stage.appendChild(img);
    overlay.appendChild(closeBtn);
    overlay.appendChild(stage);
    overlay.appendChild(caption);
    overlay.appendChild(hint);
    document.body.appendChild(overlay);

    closeBtn.addEventListener("click", close);
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay || e.target === stage) close();
    });
    img.addEventListener("click", function () { setZoom(!zoomed); });
    document.addEventListener("keydown", function (e) {
      if (!overlay.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setZoom(!zoomed); }
      /* Focus trap: the close button is the dialog's only focusable element,
         so keep Tab inside the overlay. */
      if (e.key === "Tab") {
        e.preventDefault();
        overlay.querySelector(".lightbox-close").focus();
      }
    });
  }

  function setZoom(z) {
    zoomed = z;
    stage.classList.toggle("lightbox-stage--zoomed", zoomed);
    hint.textContent = zoomed
      ? (zh ? "点击适应屏幕 · Esc 关闭" : "Click to fit · Esc to close")
      : (zh ? "点击图片查看原图 · Esc 关闭" : "Click the image for full size · Esc to close");
  }

  function open(fig) {
    if (!overlay) build();
    var src = fig.querySelector("img");
    if (!src) return;
    lastFocus = document.activeElement;
    img.src = src.currentSrc || src.src;
    img.alt = src.alt || "";
    var cap = fig.querySelector("figcaption");
    caption.textContent = cap ? cap.textContent : "";
    caption.style.display = cap ? "" : "none";
    setZoom(false);
    stage.scrollTop = 0;
    stage.scrollLeft = 0;
    overlay.classList.add("is-open");
    document.documentElement.style.overflow = "hidden";
    overlay.querySelector(".lightbox-close").focus();
  }

  function close() {
    overlay.classList.remove("is-open");
    document.documentElement.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }

  figs.forEach(function (fig) {
    var target = fig.querySelector("img");
    if (!target) return;
    fig.classList.add("plate--zoomable");
    fig.setAttribute("tabindex", "0");
    fig.setAttribute("role", "button");
    fig.setAttribute("aria-label", zh ? "放大查看图片" : "View image enlarged");
    fig.addEventListener("click", function () { open(fig); });
    fig.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(fig); }
    });
  });
})();
