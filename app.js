const menuToggle = document.querySelector("[data-menu-toggle]");
const siteNav = document.querySelector("[data-site-nav]");

if (menuToggle && siteNav) {
  siteNav.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      menuToggle.checked = false;
    }
  });
}

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealItems = [...document.querySelectorAll("[data-reveal]")];

if (!reduceMotion && "IntersectionObserver" in window) {
  document.documentElement.classList.add("has-reveal");
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.dataset.revealed = "true";
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -8%", threshold: 0.08 });

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => { item.dataset.revealed = "true"; });
}

// Notes backdrops stay decorative; each Works cover keeps the first gallery slot.
const contentImages = [...document.querySelectorAll(".full-article .article-backdrop, .full-article .plate img, .note-page .note-body img")];

if (contentImages.length && typeof HTMLDialogElement !== "undefined" && "showModal" in HTMLDialogElement.prototype) {
  const isChinese = document.documentElement.lang.toLowerCase().startsWith("zh");
  const labels = isChinese ? {
    title: "图片查看器", close: "关闭图片预览", previous: "上一张图片", next: "下一张图片",
    zoom: "查看原图大小", fit: "让图片适应屏幕", fitText: "适应", loading: "图片加载中…",
    error: "这张图片暂时无法显示。", original: "打开原图", enlarge: "放大图片",
    hint: "方向键切图 · 点击图片放大 · Esc 关闭", zoomHint: "滚动查看原图 · 方向键切图 · Esc 关闭"
  } : {
    title: "Image viewer", close: "Close image preview", previous: "Previous image", next: "Next image",
    zoom: "View image at original size", fit: "Fit image to screen", fitText: "Fit", loading: "Loading image…",
    error: "This image could not be displayed.", original: "Open original image", enlarge: "Enlarge image",
    hint: "Arrow keys to browse · Click image to zoom · Esc to close", zoomHint: "Scroll to inspect · Arrow keys to browse · Esc to close"
  };
  const makeButton = (className, label, text) => {
    const button = document.createElement("button");
    button.className = className;
    button.type = "button";
    button.setAttribute("aria-label", label);
    button.textContent = text;
    return button;
  };
  const lightbox = document.createElement("dialog");
  lightbox.className = "lightbox";
  lightbox.setAttribute("aria-label", labels.title);
  const toolbar = document.createElement("div");
  toolbar.className = "lightbox-toolbar";
  const count = document.createElement("span");
  count.className = "lightbox-count";
  count.setAttribute("aria-live", "polite");
  count.setAttribute("aria-atomic", "true");
  const zoomButton = makeButton("lightbox-zoom", labels.zoom, "1:1");
  const closeButton = makeButton("lightbox-close", labels.close, "×");
  toolbar.append(count, zoomButton, closeButton);
  const stage = document.createElement("div");
  stage.className = "lightbox-stage";
  const lightboxImage = document.createElement("img");
  lightboxImage.alt = "";
  const message = document.createElement("p");
  message.className = "lightbox-message";
  message.setAttribute("role", "status");
  message.hidden = true;
  stage.append(lightboxImage, message);
  const previousButton = makeButton("lightbox-nav lightbox-prev", labels.previous, "←");
  const nextButton = makeButton("lightbox-nav lightbox-next", labels.next, "→");
  previousButton.hidden = nextButton.hidden = contentImages.length < 2;
  const caption = document.createElement("p");
  caption.className = "lightbox-caption";
  caption.id = "lightbox-caption";
  const hint = document.createElement("p");
  hint.className = "lightbox-hint";
  hint.id = "lightbox-hint";
  const originalLink = document.createElement("a");
  originalLink.className = "lightbox-original";
  originalLink.textContent = labels.original;
  originalLink.hidden = true;
  message.append(originalLink);
  lightbox.setAttribute("aria-describedby", "lightbox-caption lightbox-hint");
  lightbox.append(toolbar, stage, caption, hint, previousButton, nextButton);
  document.body.append(lightbox);
  let current = 0;
  let zoomed = false;
  let lastTrigger = null;
  let previousPaddingRight = "";

  const setZoom = (value) => {
    zoomed = value;
    stage.classList.toggle("lightbox-stage--zoomed", value);
    zoomButton.textContent = value ? labels.fitText : "1:1";
    zoomButton.setAttribute("aria-label", value ? labels.fit : labels.zoom);
    zoomButton.setAttribute("aria-pressed", String(value));
    hint.textContent = value ? labels.zoomHint : labels.hint;
    stage.scrollTo(0, 0);
  };
  const imageTrigger = (image) => image.classList.contains("article-backdrop")
    ? document.querySelector("[data-hero-lightbox]") : image.closest("[data-lightbox]");
  const showImage = (index) => {
    current = (index + contentImages.length) % contentImages.length;
    const source = contentImages[current];
    const trigger = imageTrigger(source);
    const figureCaption = source.closest("figure")?.querySelector("figcaption");
    const sourceUrl = trigger?.getAttribute("href") || source.currentSrc || source.src;
    originalLink.href = sourceUrl;
    originalLink.hidden = true;
    message.replaceChildren(document.createTextNode(labels.loading), originalLink);
    message.hidden = false;
    lightboxImage.hidden = true;
    lightboxImage.alt = trigger?.dataset.imageAlt || source.alt || "";
    lightboxImage.src = sourceUrl;
    caption.textContent = figureCaption?.textContent.trim() || trigger?.dataset.caption || source.alt || "";
    caption.hidden = !caption.textContent;
    count.textContent = `${current + 1} / ${contentImages.length}`;
    setZoom(false);
  };
  lightboxImage.addEventListener("load", () => {
    message.hidden = true;
    lightboxImage.hidden = false;
  });
  lightboxImage.addEventListener("error", () => {
    if (!lightbox.open) return;
    message.replaceChildren(document.createTextNode(`${labels.error} `), originalLink);
    originalLink.hidden = false;
    lightboxImage.hidden = true;
    message.hidden = false;
  });
  const openLightbox = (trigger, index) => {
    lastTrigger = trigger;
    showImage(index);
    const scrollbarGap = window.innerWidth - document.documentElement.clientWidth;
    previousPaddingRight = document.body.style.paddingRight;
    if (scrollbarGap > 0) {
      document.body.style.paddingRight = `${parseFloat(getComputedStyle(document.body).paddingRight) + scrollbarGap}px`;
    }
    document.documentElement.classList.add("lightbox-open");
    if (!lightbox.open) lightbox.showModal();
    closeButton.focus({ preventScroll: true });
  };
  const closeLightbox = () => { if (lightbox.open) lightbox.close(); };
  const wiredTriggers = new Set();
  contentImages.forEach((image, index) => {
    let trigger = imageTrigger(image);
    if (!trigger) {
      // A real link preserves the original-image fallback when dialog support is absent.
      trigger = document.createElement("a");
      trigger.href = image.currentSrc || image.src;
      trigger.className = "image-button zoomable-image";
      trigger.setAttribute("aria-label", `${labels.enlarge}: ${image.alt || ""}`);
      image.before(trigger);
      trigger.append(image);
    }
    if (!wiredTriggers.has(trigger)) {
      trigger.addEventListener("click", (event) => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        openLightbox(trigger, index);
      });
      wiredTriggers.add(trigger);
    }
  });
  previousButton.addEventListener("click", () => showImage(current - 1));
  nextButton.addEventListener("click", () => showImage(current + 1));
  zoomButton.addEventListener("click", () => setZoom(!zoomed));
  lightboxImage.addEventListener("click", () => setZoom(!zoomed));
  closeButton.addEventListener("click", closeLightbox);
  stage.addEventListener("click", (event) => { if (event.target === stage) closeLightbox(); });
  lightbox.addEventListener("click", (event) => { if (event.target === lightbox) closeLightbox(); });
  lightbox.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      const controls = [...lightbox.querySelectorAll('button:not([disabled]), a[href]')]
        .filter((element) => element.getClientRects().length > 0);
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      showImage(current + (event.key === "ArrowRight" ? 1 : -1));
    }
  });
  lightbox.addEventListener("close", () => {
    document.documentElement.classList.remove("lightbox-open");
    document.body.style.paddingRight = previousPaddingRight;
    lightboxImage.removeAttribute("src");
    if (lastTrigger?.isConnected) lastTrigger.focus({ preventScroll: true });
  });
}
