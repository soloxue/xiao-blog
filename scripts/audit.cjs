const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const htmlFiles = [];

function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const item = path.join(directory, entry.name);
    if (entry.isDirectory()) walk(item);
    else if (entry.name.endsWith(".html")) htmlFiles.push(item);
  }
}

walk(root);
const brokenLocalReferences = [];
const oldRouteReferences = [];
const linkedLogos = [];
const repeatedReadLinks = [];

for (const file of htmlFiles) {
  const html = fs.readFileSync(file, "utf8");
  const relative = path.relative(root, file);
  if (/index\.en|zh\.html/.test(html)) oldRouteReferences.push(relative);
  if (/<a[^>]*class="brand"/.test(html)) linkedLogos.push(relative);
  if (/read the complete work/i.test(html)) repeatedReadLinks.push(relative);

  for (const match of html.matchAll(/(?:href|src)="([^"#?]+)[^"]*"/g)) {
    const reference = match[1];
    if (/^(?:https?:|mailto:|data:|javascript:)/.test(reference)) continue;
    const target = path.resolve(path.dirname(file), decodeURI(reference));
    if (!fs.existsSync(target)) brokenLocalReferences.push(`${relative}: ${reference}`);
  }
}

const indexFiles = ["index.html", "index.cn.html", "works/index.html", "works/index.cn.html"];
const indexLightboxMarkers = Object.fromEntries(indexFiles.map((file) => {
  const html = fs.readFileSync(path.join(root, file), "utf8");
  return [file, (html.match(/data-lightbox/g) || []).length];
}));

const report = {
  htmlFiles: htmlFiles.length,
  brokenLocalReferences,
  oldRouteReferences,
  linkedLogos,
  repeatedReadLinks,
  indexLightboxMarkers,
};

console.log(JSON.stringify(report, null, 2));
if (brokenLocalReferences.length || oldRouteReferences.length || linkedLogos.length || repeatedReadLinks.length || Object.values(indexLightboxMarkers).some(Boolean)) {
  process.exitCode = 1;
}
