// Renders the social images and icons with Playwright (dev only; the site itself needs no Node).
// Usage, from the repository root: node _build/render.mjs
// If Playwright is installed globally, run with: NODE_PATH="$(npm root -g)" node _build/render.mjs
import { createRequire } from "module";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const require = createRequire(import.meta.url);
let pw;
try { pw = require("playwright"); } catch { pw = require(path.join(process.env.NODE_PATH || "", "playwright")); }
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
for (const name of ["og", "og-study"]) {
  await page.goto("file://" + path.join(root, "_build/og", name + ".html"));
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(root, name + ".png") });
}
const svgRounded = fs.readFileSync(path.join(root, "favicon.svg"), "utf8");
const svgSquare = fs.readFileSync(path.join(root, "_build/data/mark-square.svg"), "utf8");
async function icon(svg, size, out) {
  await page.setViewportSize({ width: size, height: size });
  await page.setContent(`<html><body style="margin:0;background:transparent">${svg.replace("<svg ", `<svg width="${size}" height="${size}" `)}</body></html>`);
  await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: size, height: size } });
}
fs.mkdirSync(path.join(root, "_build/tmp"), { recursive: true });
for (const s of [16, 32, 48]) await icon(svgRounded, s, path.join(root, `_build/tmp/fav-${s}.png`));
await icon(svgSquare, 180, path.join(root, "apple-touch-icon.png"));
await browser.close();
console.log("rendered og.png, og-study.png, apple-touch-icon.png and favicon PNGs in _build/tmp (pack them with _build/make_ico.py)");
