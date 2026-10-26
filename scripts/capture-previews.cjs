const path = require("node:path");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const previewDir = path.join(root, "previews");
const base = "http://127.0.0.1:8736";

async function inspect(page, label) {
  await page.evaluate(async () => {
    const images = [...document.images].filter((image) => image.hasAttribute("src"));
    images.forEach((image) => image.setAttribute("loading", "eager"));
    await Promise.all(images.map((image) => {
      if (image.complete) return Promise.resolve();
      return new Promise((resolve) => {
        image.addEventListener("load", resolve, { once: true });
        image.addEventListener("error", resolve, { once: true });
      });
    }));
  });
  const result = await page.evaluate(() => ({
    title: document.title,
    background: getComputedStyle(document.body).backgroundColor,
    width: document.documentElement.scrollWidth,
    viewport: window.innerWidth,
    overflowing: [...document.querySelectorAll("body *")]
      .map((element) => ({
        tag: element.tagName.toLowerCase(),
        className: typeof element.className === "string" ? element.className : "",
        left: Math.round(element.getBoundingClientRect().left),
        right: Math.round(element.getBoundingClientRect().right),
      }))
      .filter((element) => element.left < -1 || element.right > window.innerWidth + 1)
      .slice(0, 12),
    brokenImages: [...document.images]
      .filter((image) => image.hasAttribute("src") && (!image.complete || image.naturalWidth === 0))
      .map((image) => image.getAttribute("src")),
    introGap: document.querySelector(".page-intro .eyebrow") && document.querySelector(".page-intro h1")
      ? Math.round(document.querySelector(".page-intro h1").getBoundingClientRect().top - document.querySelector(".page-intro .eyebrow").getBoundingClientRect().bottom)
      : null,
    sectionGap: document.querySelector(".section-heading .eyebrow") && document.querySelector(".section-heading h2")
      ? Math.round(document.querySelector(".section-heading h2").getBoundingClientRect().top - document.querySelector(".section-heading .eyebrow").getBoundingClientRect().bottom)
      : null,
    readingWidth: document.querySelector(".full-article > .prose")
      ? (() => {
          const prose = document.querySelector(".full-article > .prose");
          const style = getComputedStyle(prose);
          return Math.round(prose.getBoundingClientRect().width - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight));
        })()
      : null,
    endTitleSize: document.querySelector(".end-title")
      ? getComputedStyle(document.querySelector(".end-title")).fontSize
      : null,
    noteParagraphs: document.querySelectorAll(".note-verbatim > p:not(.moment-head)").length,
    mainImages: [...document.querySelectorAll("body img")].filter((image) => !image.closest(".brand") && !image.closest(".lightbox")).length,
    lightboxImages: [...document.querySelectorAll("body img")]
      .filter((image) => !image.closest(".brand") && !image.closest(".lightbox"))
      .filter((image) => image.classList.contains("zoomable-image") || image.closest("[data-lightbox]"))
      .length,
  }));

  if (result.brokenImages.length) {
    throw new Error(`${label}: broken images: ${result.brokenImages.join(", ")}`);
  }
  if (result.width > result.viewport + 1) {
    throw new Error(`${label}: horizontal overflow ${result.width}px > ${result.viewport}px; ${JSON.stringify(result.overflowing)}`);
  }
  return result;
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    args: ["--disable-gpu", "--disable-crash-reporter"],
  });
  const consoleErrors = [];

  const desktop = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  desktop.on("console", (message) => {
    if (message.type() === "error" && !message.text().includes("ERR_NETWORK_ACCESS_DENIED")) {
      consoleErrors.push(message.text());
    }
  });
  await desktop.goto(`${base}/index.html`, { waitUntil: "networkidle" });
  await desktop.evaluate(() => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
  });
  await desktop.screenshot({ path: path.join(previewDir, "06-ivory-home.png") });
  const home = await inspect(desktop, "desktop home");
  await desktop.locator(".aperture-image-link").click();
  await desktop.waitForURL(`${base}/works/florilegium/index.html`);
  const homeImageNavigated = desktop.url().endsWith("/works/florilegium/index.html");
  const firstImageTrigger = desktop.locator("[data-lightbox]").first();
  await firstImageTrigger.click();
  await desktop.locator("dialog.lightbox[open]").waitFor({ state: "visible" });
  await desktop.screenshot({ path: path.join(previewDir, "12-image-lightbox.png") });
  const lightboxOpened = await desktop.locator("dialog.lightbox").evaluate((dialog) => dialog.open);
  await desktop.keyboard.press("Escape");
  await desktop.locator("dialog.lightbox").waitFor({ state: "hidden" });
  const lightboxFocusRestored = await firstImageTrigger.evaluate((trigger) => document.activeElement === trigger);

  await desktop.goto(`${base}/works/index.html`, { waitUntil: "networkidle" });
  await desktop.evaluate(() => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
  });
  await desktop.screenshot({ path: path.join(previewDir, "10-works-refined.png") });
  const works = await inspect(desktop, "desktop works");

  await desktop.goto(`${base}/works/on-neuroscience-and-religious-experience/cn.html`, { waitUntil: "networkidle" });
  await desktop.evaluate(() => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
  });
  await desktop.screenshot({ path: path.join(previewDir, "07-full-article.png") });
  const article = await inspect(desktop, "desktop article");
  await desktop.locator("h2").nth(2).scrollIntoViewIfNeeded();
  await desktop.screenshot({ path: path.join(previewDir, "08-article-reading.png") });

  await desktop.goto(`${base}/notes/2026-08-23-thomas-bergersen/cn.html`, { waitUntil: "networkidle" });
  await desktop.evaluate(() => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, document.querySelector(".note-body").offsetTop);
  });
  await desktop.screenshot({ path: path.join(previewDir, "13-note-reading.png") });
  const note = await inspect(desktop, "desktop note");

  const mobile = await browser.newPage({
    viewport: { width: 390, height: 844 },
    reducedMotion: "reduce",
  });
  await mobile.goto(`${base}/works/on-neuroscience-and-religious-experience/cn.html`, { waitUntil: "networkidle" });
  await mobile.evaluate(() => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
  });
  await mobile.screenshot({ path: path.join(previewDir, "09-article-mobile.png") });
  const mobileArticle = await inspect(mobile, "mobile article");

  await mobile.goto(`${base}/works/index.html`, { waitUntil: "networkidle" });
  await mobile.evaluate(() => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
  });
  await mobile.screenshot({ path: path.join(previewDir, "11-works-mobile.png") });
  const mobileWorks = await inspect(mobile, "mobile works");

  const medium = await browser.newPage({ viewport: { width: 850, height: 650 } });
  await medium.goto(`${base}/index.html`, { waitUntil: "networkidle" });
  await medium.evaluate(() => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, Math.max(0, document.querySelector(".section-heading").offsetTop - 110));
  });
  await medium.waitForTimeout(900);
  await medium.screenshot({ path: path.join(previewDir, "14-home-section-850.png") });
  const mediumHome = await inspect(medium, "850px home");

  await browser.close();
  if (consoleErrors.length) {
    throw new Error(`console errors: ${consoleErrors.join(" | ")}`);
  }

  console.log(JSON.stringify({ home, works, article, note, mobileArticle, mobileWorks, mediumHome, homeImageNavigated, lightboxOpened, lightboxFocusRestored }, null, 2));
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
