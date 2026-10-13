// UZHPL catalog — 3D product renders (three.js, studio lighting, CC0 Poly Haven assets + modeled parts)
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js';

const Q = new URLSearchParams(location.search);
const NAME = Q.get('name') || 'drill';
const W = +Q.get('w') || 800, H = +Q.get('h') || 600;
const VIEW = Q.get('view') || 'product';

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(28, W / H, 0.01, 5000);

// ------------------------------------------------------------------ textures (procedural, deterministic)
function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
function canvasTex(w, h, draw, repeat = [1, 1], srgb = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}
const TEX = {};
TEX.hpl = (base = '#2a2c30', seed = 3) => canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h);
  const r = rng(seed);
  for (let i = 0; i < 9000; i++) { const v = r(); g.fillStyle = `rgba(${v > .5 ? 255 : 0},${v > .5 ? 255 : 0},${v > .5 ? 255 : 0},${0.025 * r()})`; g.fillRect(r() * w, r() * h, 1 + r() * 3, 1 + r() * 3); }
  for (let i = 0; i < 40; i++) { g.strokeStyle = `rgba(255,255,255,${0.02 + 0.02 * r()})`; g.beginPath(); const x = r() * w, y = r() * h; g.moveTo(x, y); g.lineTo(x + (r() - .5) * 120, y + (r() - .5) * 40); g.stroke(); }
});
TEX.wool = () => canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = '#d4b25e'; g.fillRect(0, 0, w, h);
  const r = rng(11);
  for (let i = 0; i < 2600; i++) {
    g.strokeStyle = r() > .5 ? 'rgba(150,110,40,.35)' : 'rgba(245,220,150,.45)'; g.lineWidth = .6 + r();
    g.beginPath(); const x = r() * w, y = r() * h; g.moveTo(x, y);
    g.bezierCurveTo(x + 10, y - 6 + r() * 12, x + 20, y - 6 + r() * 12, x + 30 + r() * 20, y - 4 + r() * 8); g.stroke();
  }
});
TEX.concrete = () => canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = '#b5b4ae'; g.fillRect(0, 0, w, h);
  const r = rng(5);
  for (let i = 0; i < 14000; i++) { const v = 120 + r() * 90 | 0; g.fillStyle = `rgba(${v},${v},${v - 4},.25)`; g.fillRect(r() * w, r() * h, 1 + r() * 2, 1 + r() * 2); }
  for (let i = 0; i < 160; i++) { g.fillStyle = 'rgba(70,70,68,.5)'; g.beginPath(); g.arc(r() * w, r() * h, .8 + r() * 2.4, 0, 7); g.fill(); }
});
TEX.spangle = () => canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = '#c9cdd1'; g.fillRect(0, 0, w, h);
  const r = rng(9);
  for (let i = 0; i < 220; i++) { const v = 170 + r() * 70 | 0; g.fillStyle = `rgb(${v},${v + 3},${v + 6})`; g.beginPath();
    const x = r() * w, y = r() * h, s = 10 + r() * 30; g.moveTo(x, y); for (let k = 0; k < 6; k++) g.lineTo(x + Math.cos(k + r()) * s, y + Math.sin(k + r()) * s); g.fill(); }
});
TEX.fabric = () => canvasTex(256, 256, (g, w, h) => {
  g.fillStyle = '#3d4249'; g.fillRect(0, 0, w, h);
  for (let y = 0; y < h; y += 3) { g.fillStyle = 'rgba(255,255,255,.04)'; g.fillRect(0, y, w, 1); }
  for (let x = 0; x < w; x += 3) { g.fillStyle = 'rgba(0,0,0,.08)'; g.fillRect(x, 0, 1, h); }
}, [6, 6]);

// ------------------------------------------------------------------ materials
const M = {
  galv: () => new THREE.MeshStandardMaterial({ color: 0xe0e3e6, map: TEX.spangle(), metalness: 0.6, roughness: 0.38 }),
  alu: () => new THREE.MeshStandardMaterial({ color: 0xe1e4e8, metalness: 0.75, roughness: 0.3 }),
  steel: () => new THREE.MeshStandardMaterial({ color: 0xc8cdd2, metalness: 0.7, roughness: 0.28 }),
  darkSteel: () => new THREE.MeshStandardMaterial({ color: 0x55595f, metalness: 0.9, roughness: 0.35 }),
  hpl: (c = '#2a2c30', seed = 3) => new THREE.MeshPhysicalMaterial({ map: TEX.hpl(c, seed), roughness: 0.55, clearcoat: 0.25, clearcoatRoughness: 0.45 }),
  hplCore: () => new THREE.MeshStandardMaterial({ color: 0x3b2a20, roughness: 0.8 }),
  wool: () => new THREE.MeshStandardMaterial({ map: TEX.wool(), roughness: 1 }),
  concrete: () => new THREE.MeshStandardMaterial({ map: TEX.concrete(), roughness: 0.95 }),
  rubber: () => new THREE.MeshStandardMaterial({ color: 0x1b1c1e, roughness: 0.85 }),
  plastic: (c) => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.42, clearcoat: 0.3, clearcoatRoughness: 0.4 }),
  orange: () => new THREE.MeshPhysicalMaterial({ color: 0xf26a1b, roughness: 0.38, clearcoat: 0.4 }),
  graphite: () => new THREE.MeshPhysicalMaterial({ color: 0x2b2d31, roughness: 0.45, clearcoat: 0.3 }),
  membrane: () => new THREE.MeshStandardMaterial({ map: TEX.fabric(), roughness: 0.9, side: THREE.DoubleSide }),
  glass: () => new THREE.MeshPhysicalMaterial({ color: 0x9fb4c4, metalness: 0, roughness: 0.04, transmission: 0.0, reflectivity: 1, clearcoat: 1, envMapIntensity: 1.6 }),
  laser: () => new THREE.MeshBasicMaterial({ color: 0x35e06a }),
  white: () => new THREE.MeshPhysicalMaterial({ color: 0xf2f2f0, roughness: 0.5 }),
};

// ------------------------------------------------------------------ helpers
const ext = (shape, depth, mat, bevel = 0) => {
  const g = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: bevel > 0, bevelSize: bevel, bevelThickness: bevel, bevelSegments: 2, curveSegments: 24 });
  return mesh(g, mat);
};
function mesh(g, m) { const o = new THREE.Mesh(g, m); o.castShadow = true; o.receiveShadow = true; return o; }
function box(w, h, d, m, r = 0) { return mesh(r ? new RoundedBoxGeometry(w, h, d, 4, r) : new THREE.BoxGeometry(w, h, d), m); }
function cyl(rt, rb, h, m, seg = 48) { return mesh(new THREE.CylinderGeometry(rt, rb, h, seg), m); }
function lathe(pts, m, seg = 64) { return mesh(new THREE.LatheGeometry(pts.map(([x, y]) => new THREE.Vector2(x, y)), seg), m); }
function slotPath(cx, cy, len, r) {
  const p = new THREE.Path();
  p.absarc(cx - len / 2, cy, r, Math.PI / 2, Math.PI * 1.5, false);
  p.absarc(cx + len / 2, cy, r, Math.PI * 1.5, Math.PI / 2, false);
  return p;
}
function rectShape(w, h) { const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(w, 0); s.lineTo(w, h); s.lineTo(0, h); s.lineTo(0, 0); return s; }
function group(...ch) { const g = new THREE.Group(); ch.forEach(c => g.add(c)); return g; }
function at(o, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) { o.position.set(x, y, z); o.rotation.set(rx, ry, rz); return o; }
const gltfLoader = new GLTFLoader();
const loadPH = (name) => new Promise((res) => gltfLoader.load(`assets/${name}/${name}.gltf`, g => { g.scene.traverse(o => { if (o.isMesh) { o.castShadow = o.receiveShadow = true; } }); res(g.scene); }));

// ------------------------------------------------------------------ profiles (units: mm)
function Lprofile(len = 300, a = 40, b = 40, t = 1.5) {
  const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(a, 0); s.lineTo(a, t); s.lineTo(t, t); s.lineTo(t, b); s.lineTo(0, b); s.lineTo(0, 0);
  return at(ext(s, len, M.galv(), .3), 0, 0, -len / 2);
}
function Tprofile(len = 300, a = 80, b = 50, t = 1.5) {
  const s = new THREE.Shape(); s.moveTo(-a / 2, 0); s.lineTo(a / 2, 0); s.lineTo(a / 2, t); s.lineTo(t / 2, t); s.lineTo(t / 2, b); s.lineTo(-t / 2, b); s.lineTo(-t / 2, t); s.lineTo(-a / 2, t); s.lineTo(-a / 2, 0);
  return at(ext(s, len, M.galv(), .3), 0, 0, -len / 2);
}
function bracket(sliding = false) {
  // base plate (on wall) with anchor hole + arm with slots
  const t = 2;
  const base = rectShape(50, 80); base.holes.push(slotPath(25, 40, 6, 5.5));
  const arm = rectShape(sliding ? 110 : 100, 80);
  if (sliding) { arm.holes.push(slotPath(70, 25, 40, 3)); arm.holes.push(slotPath(70, 55, 40, 3)); }
  else { arm.holes.push(slotPath(65, 25, 22, 3)); arm.holes.push(slotPath(65, 55, 22, 3)); }
  const g = new THREE.Group();
  g.add(at(ext(base, t, M.galv(), .2), -25, -40, 0));
  g.add(at(ext(arm, t, M.galv(), .2), 25 - t, -40, 0, 0, -Math.PI / 2, 0));
  return g;
}
function gasket() {
  const s = rectShape(50, 80); s.holes.push(slotPath(25, 40, 6, 5.5));
  return at(ext(s, 4, M.rubber(), .4), -25, -40, 0);
}
function anchor(len = 100) {
  const g = new THREE.Group();
  const sleeve = cyl(5, 5, len * .75, M.steel()); at(sleeve, 0, -len * .375 - 4, 0); g.add(sleeve);
  for (let i = 0; i < 14; i++) { const r = mesh(new THREE.TorusGeometry(4.9, .55, 8, 40), M.steel()); at(r, 0, -len * .45 - i * 3, 0, Math.PI / 2); g.add(r); }
  const cone = cyl(3.5, 5.5, 14, M.steel()); at(cone, 0, -len + 4, 0); g.add(cone);
  const washer = cyl(10, 10, 2, M.steel()); at(washer, 0, 1, 0); g.add(washer);
  const hex = cyl(8, 8, 7, M.steel(), 6); at(hex, 0, 6, 0); g.add(hex);
  return g;
}
function rivet(head = '#2b2d31', big = true) {
  const g = new THREE.Group();
  const R = big ? 7.5 : 5;
  g.add(lathe([[0, 0], [R, 0], [R, .6], [R * .8, 1.6], [R * .4, 2.3], [0, 2.5]], M.plastic(head)));
  g.add(at(cyl(2.5, 2.5, 15, M.alu()), 0, -7.5, 0));
  g.add(at(cyl(1.3, 1.3, 26, M.steel()), 0, -20, 0));
  g.add(at(mesh(new THREE.SphereGeometry(1.9, 24, 16), M.steel()), 0, -15.5, 0));
  return g;
}
function screwPart() {
  const g = new THREE.Group();
  g.add(lathe([[0, 0], [7.5, 0], [7.5, .5], [6, 2.2], [0, 2.8]], M.plastic('#2b2d31')));
  g.add(at(cyl(7.4, 7.4, 1.2, M.rubber()), 0, -.7, 0));
  const shaft = cyl(2.4, 2.4, 22, M.steel()); at(shaft, 0, -12, 0); g.add(shaft);
  for (let i = 0; i < 12; i++) { const r = mesh(new THREE.TorusGeometry(2.6, .5, 6, 24), M.steel()); at(r, 0, -3 - i * 1.6, 0, Math.PI / 2 + .12); g.add(r); }
  g.add(at(cyl(.2, 2.4, 5, M.steel()), 0, -25.5, 0, Math.PI));
  return g;
}
function washer() {
  const g = new THREE.Group();
  g.add(lathe([[3, 0], [9, 0], [9, 1.2], [3, 1.2]], M.steel()));
  g.add(at(lathe([[3, 0], [8.5, 0], [8.5, 1.5], [3, 1.5]], M.rubber()), 0, -1.5, 0));
  return g;
}
function panel(w = 300, h = 400, t = 8, color = '#2a2c30', holes = false) {
  const g = new THREE.Group();
  const p = box(w, h, t, [M.hplCore(), M.hplCore(), M.hplCore(), M.hplCore(), M.hpl(color), M.hpl(color)]);
  g.add(p);
  if (holes) for (const [x, y] of [[-w / 2 + 30, h / 2 - 30], [w / 2 - 30, h / 2 - 30], [-w / 2 + 30, -h / 2 + 30], [w / 2 - 30, -h / 2 + 30]]) {
    const r = rivet(); at(r, x, y, t / 2, Math.PI / 2); g.add(r);
  }
  return g;
}
function grooved() {
  const g = panel(300, 400, 10);
  const groove = box(300, 6, 4, M.hplCore()); at(groove, 0, 120, -5.1); g.add(groove);
  const groove2 = box(300, 6, 4, M.hplCore()); at(groove2, 0, -120, -5.1); g.add(groove2);
  return g;
}
function insulation() {
  const m = M.wool();
  return group(at(box(240, 160, 100, m, 3), 0, 0, 0), at(box(240, 160, 100, m, 3), 30, 0, -110));
}
function membraneRoll() {
  const g = new THREE.Group();
  const roll = cyl(55, 55, 300, M.membrane()); roll.rotation.z = Math.PI / 2; g.add(roll);
  const core = cyl(20, 20, 302, M.white()); core.rotation.z = Math.PI / 2; g.add(core);
  const sheet = mesh(new THREE.PlaneGeometry(300, 260), M.membrane()); at(sheet, 0, -55, 130, -Math.PI / 2); g.add(sheet);
  return g;
}
function tapeRoll(red = true) {
  const g = new THREE.Group();
  g.add(lathe([[38, 0], [70, 0], [70, 24], [38, 24]], M.rubber()));
  g.add(lathe([[30, -.5], [38, -.5], [38, 24.5], [30, 24.5]], M.plastic('#d8d4cc')));
  if (red) { const lb = mesh(new THREE.CylinderGeometry(70.3, 70.3, 24, 64, 1, true, 0, 1.2), M.plastic('#c62d1f')); at(lb, 0, 12, 0); g.add(lb); }
  return g;
}
function cartridge() {
  const g = new THREE.Group();
  g.add(lathe([[0, 0], [24, 0], [24, 200], [0, 200]], M.alu()));
  const label = mesh(new THREE.CylinderGeometry(24.3, 24.3, 120, 64, 1, true), M.white()); at(label, 0, 100, 0); g.add(label);
  const band = mesh(new THREE.CylinderGeometry(24.4, 24.4, 14, 64, 1, true), M.orange()); at(band, 0, 150, 0); g.add(band);
  g.add(at(lathe([[0, 0], [10, 0], [3, 70], [0, 70]], M.plastic('#e8e6e1')), 0, 200, 0));
  return g;
}
function bottle(dark = false) {
  const g = new THREE.Group();
  g.add(lathe([[0, 0], [30, 0], [32, 4], [32, 120], [28, 132], [12, 140], [12, 150], [0, 150]], dark ? M.plastic('#2b2d31') : M.plastic('#e9e7e2')));
  const lab = mesh(new THREE.CylinderGeometry(32.3, 32.3, 70, 64, 1, true), dark ? M.white() : M.graphite()); at(lab, 0, 60, 0); g.add(lab);
  g.add(at(cyl(14, 14, 24, M.orange()), 0, 160, 0));
  return g;
}
function clip() {
  const s = new THREE.Shape(); const t = 2.5;
  s.moveTo(0, 0); s.lineTo(40, 0); s.lineTo(40, t); s.lineTo(t, t); s.lineTo(t, 30); s.lineTo(-14, 42); s.lineTo(-16, 40); s.lineTo(0, 28); s.lineTo(0, 0);
  const g = new THREE.Group(); g.add(ext(s, 60, M.alu(), .3));
  const sc = screwPart(); at(sc, 25, t, 30, Math.PI); sc.scale.setScalar(.6); g.add(sc);
  return g;
}
function vprofile() {
  const g = Tprofile(300, 60, 50, 1.8);
  const rail = Lprofile(160, 30, 20, 1.8); at(rail, 0, 52, 60, 0, Math.PI / 2, 0);
  return group(g, rail);
}

// ------------------------------------------------------------------ tools (modeled)
function riveter() {
  const g = new THREE.Group();
  g.add(at(box(200, 60, 56, M.graphite(), 16), 0, 0, 0));
  g.add(at(box(60, 120, 46, M.graphite(), 14), -30, -80, 0, 0, 0, .2));
  g.add(at(box(100, 44, 80, M.orange(), 8), -50, -150, 0));
  g.add(at(box(80, 18, 72, M.graphite(), 6), -50, -124, 0));
  g.add(at(cyl(14, 18, 50, M.steel()), 120, 0, 0, 0, 0, Math.PI / 2));
  g.add(at(cyl(8, 12, 22, M.orange()), 155, 0, 0, 0, 0, Math.PI / 2));
  g.add(at(cyl(16, 16, 50, M.plastic('#d9dde2')), -120, 0, 0, 0, 0, Math.PI / 2));
  g.add(at(box(30, 14, 20, M.orange(), 4), 10, -45, 0));
  return g;
}
function laserLevel() {
  const g = new THREE.Group();
  g.add(at(box(110, 130, 110, M.graphite(), 14), 0, 0, 0));
  g.add(at(box(116, 30, 116, M.orange(), 8), 0, 70, 0));
  g.add(at(box(116, 20, 116, M.orange(), 6), 0, -70, 0));
  for (const r of [0, Math.PI / 2]) { const w = at(box(70, 70, 4, M.glass()), Math.sin(r) * 56, 10, Math.cos(r) * 56, 0, r, 0); g.add(w); }
  g.add(at(box(600, 1.2, 1.2, M.laser()), 0, 10, 58));
  g.add(at(box(1.2, 400, 1.2, M.laser()), 0, 10, 58));
  g.add(at(cyl(30, 34, 22, M.graphite()), 0, -90, 0));
  return g;
}
function circSaw() {
  const g = new THREE.Group();
  const blade = at(cyl(92, 92, 2, M.steel(), 64), 0, 0, 0, Math.PI / 2); g.add(blade);
  for (let i = 0; i < 24; i++) { const a = i / 24 * Math.PI * 2; g.add(at(box(6, 6, 2.6, M.darkSteel()), Math.cos(a) * 92, Math.sin(a) * 92, 0, 0, 0, a + .6)); }
  g.add(at(cyl(98, 98, 30, M.graphite(), 64), 0, 30, 22, Math.PI / 2, 0, 0)).scale.set(1, 1, 1);
  g.children[g.children.length - 1].geometry = new THREE.CylinderGeometry(98, 98, 30, 64, 1, false, -0.3, Math.PI + .6);
  g.add(at(box(240, 8, 140, M.alu(), 2), 0, -60, 0));
  g.add(at(box(110, 90, 80, M.orange(), 18), -40, 70, 60));
  g.add(at(mesh(new THREE.TorusGeometry(50, 12, 16, 40, Math.PI), M.graphite()), 30, 120, 60, 0, 0, 0));
  return g;
}
function trackSaw() { const g = circSaw(); g.add(at(box(600, 10, 180, M.alu(), 2), 0, -70, 0)); return g; }
function cnc() {
  const g = new THREE.Group();
  g.add(at(box(900, 60, 520, M.plastic('#d8dbe0'), 6), 0, 0, 0));
  g.add(at(box(860, 10, 480, M.graphite()), 0, 35, 0));
  g.add(at(box(700, 8, 380, M.hpl('#3a3c40', 7)), 0, 44, 0));
  for (const z of [-250, 250]) g.add(at(box(40, 300, 40, M.graphite(), 6), 200, 190, z));
  g.add(at(box(60, 60, 560, M.graphite(), 8), 200, 340, 0));
  g.add(at(box(110, 160, 110, M.orange(), 12), 200, 290, 60));
  g.add(at(cyl(20, 20, 80, M.steel()), 200, 180, 60));
  g.add(at(cyl(4, 4, 30, M.steel()), 200, 125, 60));
  g.add(at(box(900, 300, 30, M.plastic('#c9ccd1')), 0, -180, 260)); g.add(at(box(900, 300, 30, M.plastic('#c9ccd1')), 0, -180, -260));
  return g;
}
function router() {
  const g = new THREE.Group();
  g.add(at(cyl(55, 55, 140, M.graphite()), 0, 70, 0));
  g.add(at(cyl(60, 60, 24, M.orange()), 0, 150, 0));
  g.add(at(cyl(85, 85, 12, M.alu()), 0, 0, 0));
  for (const s of [-1, 1]) g.add(at(box(30, 80, 30, M.rubber(), 12), s * 95, 50, 0));
  g.add(at(cyl(5, 5, 40, M.steel()), 0, -20, 0));
  return g;
}
function levelTool() {
  const g = new THREE.Group();
  g.add(at(box(600, 56, 26, M.alu(), 3), 0, 0, 0));
  g.add(at(box(70, 60, 28, M.orange(), 4), -265, 0, 0)); g.add(at(box(70, 60, 28, M.orange(), 4), 265, 0, 0));
  g.add(at(box(70, 26, 30, M.graphite(), 3), 0, 0, 0));
  g.add(at(cyl(7, 7, 50, new THREE.MeshPhysicalMaterial({ color: 0xb8f07a, transmission: .2, roughness: .1, clearcoat: 1 })), 0, 0, 10, 0, 0, Math.PI / 2));
  return g;
}
function clamp() {
  const g = new THREE.Group();
  g.add(at(box(14, 300, 8, M.steel(), 2), 0, 0, 0));
  g.add(at(box(110, 20, 16, M.darkSteel(), 3), 50, 140, 0));
  g.add(at(box(110, 24, 18, M.darkSteel(), 3), 50, -30, 0));
  g.add(at(cyl(5, 5, 120, M.steel()), 95, -90, 0));
  g.add(at(box(36, 90, 30, M.orange(), 12), 95, -175, 0));
  g.add(at(cyl(14, 14, 8, M.rubber()), 95, -24, 0));
  return g;
}
function suction() {
  const g = new THREE.Group();
  g.add(at(box(240, 36, 40, M.graphite(), 14), 0, 60, 0));
  for (const x of [-80, 80]) { g.add(at(cyl(56, 64, 14, M.orange()), x, 0, 0)); g.add(at(cyl(66, 66, 6, M.rubber()), x, -8, 0)); g.add(at(cyl(12, 12, 40, M.graphite()), x, 30, 0)); }
  return g;
}
function caulkGun() {
  const g = new THREE.Group();
  g.add(at(cyl(26, 26, 230, M.alu()), 40, 0, 0, 0, 0, Math.PI / 2));
  g.add(at(cyl(10, 2, 60, M.plastic('#e8e6e1')), 185, 0, 0, 0, 0, -Math.PI / 2));
  g.add(at(box(40, 130, 34, M.graphite(), 10), -90, -70, 0, 0, 0, .15));
  g.add(at(box(30, 110, 22, M.orange(), 8), -55, -60, 0, 0, 0, .3));
  g.add(at(cyl(3.5, 3.5, 200, M.steel()), -150, 0, 0, 0, 0, Math.PI / 2));
  g.add(at(box(14, 40, 30, M.graphite(), 4), -250, 0, 0));
  return g;
}
function brush() {
  const g = new THREE.Group();
  g.add(at(box(160, 26, 16, new THREE.MeshStandardMaterial({ color: 0xa8743f, roughness: .6 }), 8), -90, 0, 0));
  g.add(at(box(36, 52, 22, M.steel(), 3), 6, 0, 0));
  g.add(at(box(60, 50, 20, M.plastic('#2a2724'), 4), 54, 0, 0));
  return g;
}
function wipes() { const g = new THREE.Group(); for (let i = 0; i < 4; i++) g.add(at(box(200, 3, 160, M.white(), 1), i * 6, i * 4, i * 5, 0, i * .05)); g.add(at(box(200, 60, 160, M.plastic('#e7e9ec'), 10), 30, -34, 20)); return g; }
function knife() {
  const g = new THREE.Group();
  g.add(at(box(160, 30, 20, M.orange(), 9), 0, 0, 0));
  g.add(at(box(110, 22, 22, M.graphite(), 6), -10, 0, 0));
  const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(55, 4); s.lineTo(70, 18); s.lineTo(0, 18); s.lineTo(0, 0);
  g.add(at(ext(s, 1, M.steel()), 78, -9, 0));
  return g;
}
function glasses() {
  const g = new THREE.Group();
  const lensM = new THREE.MeshPhysicalMaterial({ color: 0xbcd6ec, roughness: .05, clearcoat: 1, metalness: .1, transparent: true, opacity: .75 });
  g.add(at(box(230, 70, 6, lensM, 3), 0, 0, 0));
  g.add(at(box(236, 12, 12, M.graphite(), 5), 0, 38, 0));
  for (const s of [-1, 1]) g.add(at(box(8, 12, 170, M.orange(), 4), s * 116, 34, -85));
  g.add(at(box(30, 20, 10, M.graphite(), 5), 0, -18, 4));
  return g;
}
function earmuffs() {
  const g = new THREE.Group();
  g.add(at(mesh(new THREE.TorusGeometry(90, 9, 12, 48, Math.PI), M.graphite()), 0, 20, 0));
  for (const s of [-1, 1]) { g.add(at(box(60, 90, 40, M.orange(), 22), s * 92, -20, 0)); g.add(at(box(64, 80, 14, M.rubber(), 6), s * 92 - s * 22, -20, 0)); }
  return g;
}
function gloves() { return loadPH('garden_gloves_01'); }
function mask() {
  const g = new THREE.Group();
  g.add(at(box(150, 110, 90, M.white(), 40), 0, 0, 0));
  for (const s of [-1, 1]) { g.add(at(cyl(34, 34, 28, M.orange()), s * 70, -20, 40, Math.PI / 2, 0, 0)); }
  g.add(at(box(60, 30, 30, M.graphite(), 10), 0, -40, 50));
  return g;
}
function boots() { const g = new THREE.Group(); g.add(at(box(110, 150, 90, M.graphite(), 20), 0, 40, 0)); g.add(at(box(240, 60, 100, M.graphite(), 24), 50, -30, 0)); g.add(at(box(250, 14, 104, M.orange(), 5), 50, -62, 0)); return g; }
function hammerDrill() {
  const g = riveter();
  g.children[4].scale.set(1, 1, 1); g.children[5].material = M.steel();
  g.add(at(cyl(4, 4, 140, M.steel()), 230, 0, 0, 0, 0, Math.PI / 2));
  return g;
}
function calipers() {
  const g = new THREE.Group();
  g.add(at(box(300, 18, 4, M.steel(), 1), 0, 0, 0));
  g.add(at(box(14, 70, 4, M.steel(), 1), -143, -40, 0));
  g.add(at(box(70, 40, 12, M.orange(), 5), -40, 4, 3)); g.add(at(box(40, 20, 2, new THREE.MeshBasicMaterial({ color: 0x1d2a20 })), -40, 6, 10));
  g.add(at(box(14, 70, 4, M.steel(), 1), -75, -40, 0));
  return g;
}
function square() { const g = new THREE.Group(); g.add(at(box(300, 30, 4, M.steel(), 1), 0, 0, 0)); g.add(at(box(30, 200, 16, M.orange(), 3), -135, 85, 0)); return g; }
function hygro() { const g = new THREE.Group(); g.add(at(box(70, 140, 30, M.graphite(), 12), 0, 0, 0)); g.add(at(box(54, 50, 2, new THREE.MeshBasicMaterial({ color: 0x1f3a28 })), 0, 30, 15.5)); g.add(at(cyl(12, 12, 6, M.orange()), 0, -35, 15, Math.PI / 2)); return g; }
function deburr() { const g = new THREE.Group(); g.add(at(cyl(14, 14, 130, M.graphite()), 0, 0, 0, 0, 0, Math.PI / 2)); g.add(at(cyl(15, 15, 30, M.orange()), -40, 0, 0, 0, 0, Math.PI / 2)); g.add(at(cyl(3, 3, 60, M.steel()), 90, 0, 0, 0, 0, Math.PI / 2)); g.add(at(mesh(new THREE.TorusGeometry(10, 3, 8, 20, Math.PI), M.steel()), 125, 8, 0)); return g; }
function vacuum() { const g = new THREE.Group(); g.add(at(cyl(120, 110, 260, M.graphite()), 0, 0, 0)); g.add(at(cyl(126, 126, 60, M.orange()), 0, 150, 0)); g.add(at(mesh(new THREE.TorusGeometry(120, 18, 12, 40, Math.PI), M.graphite()), 120, 100, 0, Math.PI / 2)); return g; }
function drillbit() {
  const g = new THREE.Group();
  g.add(at(cyl(4, 4, 50, M.steel()), -60, 0, 0, 0, 0, Math.PI / 2));
  const tw = new THREE.Group();
  for (let i = 0; i < 40; i++) { const b = box(3, 8, 2, M.darkSteel()); at(b, -30 + i * 2.6, 0, 0, i * .35, 0, 0); tw.add(b); }
  g.add(tw); g.add(at(cyl(.1, 4, 10, M.darkSteel()), 79, 0, 0, 0, 0, -Math.PI / 2));
  return g;
}
function jig() { const g = new THREE.Group(); g.add(at(box(160, 16, 80, M.alu(), 3), 0, 0, 0)); g.add(at(cyl(14, 14, 80, M.steel()), 0, 48, 0)); g.add(at(cyl(30, 30, 20, M.orange()), 0, 90, 0)); for (const s of [-1, 1]) g.add(at(cyl(6, 6, 100, M.steel()), s * 60, 50, 0)); return g; }

// ------------------------------------------------------------------ registry
const R = {
  panel: () => panel(300, 400, 8), panel_groove: grooved, membrane: membraneRoll, insulation,
  lprofile: () => Lprofile(320, 40, 40), tprofile: () => Tprofile(320, 80, 50), vprofile,
  bracket_fixed: () => bracket(false), bracket_sliding: () => bracket(true), anchor: () => anchor(100),
  rivet: () => rivet(), screw: screwPart, washer, gasket, tape: tapeRoll, epdm: () => tapeRoll(false), cartridge,
  primer: () => bottle(true), activator: () => bottle(false), clip, dowel: () => anchor(110),
  drill: () => loadPH('Drill_01'), tape_measure: () => loadPH('measuring_tape_01'), wrench: () => loadPH('combination_wrench'),
  vice: () => loadPH('bench_vice_01'), gloves,
  riveter, hand_riveter: riveter, laser: laserLevel, saw: circSaw, tracksaw: trackSaw, cnc, router, level: levelTool, clamp, suction,
  gun: caulkGun, brush, wipes, knife, glasses, ear: earmuffs, mask, boots, hammerdrill: hammerDrill, calipers, square, hygro,
  deburr, vacuum, drillbit, jig,
};

// ------------------------------------------------------------------ studio
async function studio() {
  const hdr = await new RGBELoader().loadAsync('assets/hdri/studio_small_09.hdr');
  hdr.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = hdr; scene.environmentIntensity = 1.5;
  scene.backgroundBlurriness = 0;
  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(3, 6, 4); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 8; key.shadow.bias = -0.0004;
  scene.add(key); scene.add(new THREE.HemisphereLight(0xffffff, 0xdedad4, 0.4));
  return key;
}

async function main() {
  const key = await studio();
  let obj = await R[NAME]();
  const grp = new THREE.Group(); grp.add(obj); scene.add(grp);
  // normalize: fit to unit size, rest on ground
  let bb = new THREE.Box3().setFromObject(grp); const size = bb.getSize(new THREE.Vector3());
  const k = 1 / Math.max(size.x, size.y, size.z); grp.scale.setScalar(k);
  bb = new THREE.Box3().setFromObject(grp); const c = bb.getCenter(new THREE.Vector3());
  grp.position.sub(new THREE.Vector3(c.x, bb.min.y, c.z));
  // pose: slight product rotation
  const yaw = +(Q.get('yaw') ?? -0.55), pitch = +(Q.get('pitch') ?? 0.42);
  grp.rotation.y = yaw;
  bb = new THREE.Box3().setFromObject(grp); const s2 = bb.getSize(new THREE.Vector3()); const c2 = bb.getCenter(new THREE.Vector3());
  // ground shadow catcher
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(20, 20), new THREE.ShadowMaterial({ opacity: 0.22 }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = bb.min.y; ground.receiveShadow = true; scene.add(ground);
  key.shadow.camera.left = key.shadow.camera.bottom = -2; key.shadow.camera.right = key.shadow.camera.top = 2; key.target.position.copy(c2);
  scene.add(key.target);
  const r = s2.length() * 0.5;
  const dist = r / Math.sin(THREE.MathUtils.degToRad(camera.fov / 2)) * (W / H < 1 ? 1.05 * (H / W) ** 0 : 1.0) * 1.22;
  camera.position.set(c2.x, c2.y + Math.sin(pitch) * dist, c2.z + Math.cos(pitch) * dist);
  camera.lookAt(c2);
  renderer.render(scene, camera);
  document.title = 'done';
}
(NAME.startsWith('building') ? buildingMain() : NAME.startsWith('node_') ? nodeMain() : main()).catch(e => { document.title = 'error ' + e; console.error(e); });


// ================================================================== ARCHITECTURE
async function buildingMain() {
  const dark = Q.get('dark') === '1', variant = +(Q.get('v') || 0);
  const hdr = await new RGBELoader().loadAsync(`assets/hdri/${dark ? 'evening_road_01_puresky' : 'kloofendal_48d_partly_cloudy_puresky'}.hdr`);
  hdr.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = hdr; scene.background = hdr;
  if (dark) scene.background = canvasTex(16, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, '#0e1420'); gr.addColorStop(.38, '#263247'); gr.addColorStop(.5, '#b0785a'); gr.addColorStop(.52, '#2a2a2c'); gr.addColorStop(1, '#151515');
    g.fillStyle = gr; g.fillRect(0, 0, w, h); }, [1, 1]), scene.background.mapping = THREE.EquirectangularReflectionMapping; scene.environmentIntensity = dark ? .7 : 1.0; scene.backgroundIntensity = dark ? .28 : 1.0;
  renderer.toneMappingExposure = dark ? .9 : .95;
  const sun = new THREE.DirectionalLight(dark ? 0xffc89a : 0xfff3e2, dark ? .9 : 2.6);
  sun.position.set(-70, 38, 45); sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096);
  Object.assign(sun.shadow.camera, { left: -80, right: 80, top: 80, bottom: -80, near: 1, far: 300 }); sun.shadow.bias = -0.0005;
  scene.add(sun);
  // ground
  const gmat = new THREE.MeshStandardMaterial({ color: dark ? 0x26272a : 0x7e7a73, roughness: .92 });
  const ground = mesh(new THREE.PlaneGeometry(800, 800), gmat); ground.rotation.x = -Math.PI / 2; scene.add(ground);
  const pave = mesh(new THREE.PlaneGeometry(90, 14), new THREE.MeshStandardMaterial({ color: dark ? 0x3a3a3a : 0xc8c3ba, roughness: .8 }));
  pave.rotation.x = -Math.PI / 2; pave.position.set(0, .02, 13); scene.add(pave);
  const cols = variant === 0 ? [0x2d2f33, 0x8c4a2a] : [0x2f3134, 0x55585d];
  const B = new THREE.Group(); scene.add(B);
  const r = rng(13 + variant);
  // facade generator: wall along local x, panels on +z face
  function facade(len, hgt, color, winRule, x0, z0, rotY) {
    const F = new THREE.Group(); F.position.set(x0, 0, z0); F.rotation.y = rotY; B.add(F);
    const pw = 1.5, ph = 1.0, gap = .012;
    const nx = Math.round(len / pw), ny = Math.round(hgt / ph);
    const core = box(len, hgt, .4, new THREE.MeshStandardMaterial({ color: 0x222222 })); at(core, len / 2, hgt / 2, -.2); F.add(core);
    const pMat = new THREE.MeshPhysicalMaterial({ map: TEX.hpl('#ffffff', 21), roughness: .5, clearcoat: .3, clearcoatRoughness: .4 });
    const inst = new THREE.InstancedMesh(new THREE.BoxGeometry(pw - gap * 2, ph - gap * 2, .012), pMat, nx * ny);
    inst.castShadow = inst.receiveShadow = true;
    const glass = new THREE.MeshPhysicalMaterial({ color: dark ? 0x18222c : 0x6f8798, roughness: .03, metalness: .2, clearcoat: 1, envMapIntensity: 1.3 });
    const warm = new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0xffb469, emissiveIntensity: 1.6 });
    const frame = new THREE.MeshStandardMaterial({ color: 0x1c1d1f, roughness: .5, metalness: .6 });
    const m4 = new THREE.Matrix4(), c = new THREE.Color(color);
    let k = 0;
    for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) {
      const x = (i + .5) * pw, y = (j + .5) * ph;
      if (winRule(i, j, nx, ny)) {
        const gl = box(pw, ph, .05, (dark && r() < .55) ? warm : glass); at(gl, x, y, .03); F.add(gl);
        const fr = box(.05, ph, .14, frame); at(fr, i * pw, y, .07); F.add(fr);
        const fh = box(pw, .05, .14, frame); at(fh, x, j * ph, .07); F.add(fh);
        m4.makeScale(0, 0, 0);
      } else m4.makeTranslation(x, y, .06);
      inst.setMatrixAt(k, m4);
      const t = .9 + r() * .2; inst.setColorAt(k, c.clone().multiplyScalar(t)); k++;
    }
    F.add(inst);
    // parapet coping
    const cap = box(len + .1, .12, .5, new THREE.MeshStandardMaterial({ color: 0xbfc2c5, metalness: .6, roughness: .35 })); at(cap, len / 2, hgt + .06, .05); F.add(cap);
    return F;
  }
  const H1 = 24, L1 = 36, D1 = 22;
  const winA = (i, j, nx) => j === 0 ? (i % 6 !== 0) : (j % 4 === 1 || j % 4 === 2) && (i % 6 >= 1 && i % 6 <= 3);
  const winB = (i, j) => j === 0 ? true : (j % 4 === 2);
  facade(L1, H1, cols[0], winA, -L1, 0, 0);                 // front (+z), x from -L1..0
  facade(D1, H1, cols[1], winB, 0, 0, Math.PI / 2);          // side, along -z from corner
  // second lower volume
  facade(18, 10, cols[1], winB, -L1 - 18, 6, 0);
  // roof slab
  const roof = box(L1, .3, D1, new THREE.MeshStandardMaterial({ color: 0x777777 })); at(roof, -L1 / 2, H1 + .05, -D1 / 2); B.add(roof);
  const roof2 = box(18, .3, 10, new THREE.MeshStandardMaterial({ color: 0x777777 })); at(roof2, -L1 - 9, 10.05, 1); B.add(roof2);
  // canopy
  const can = box(10, .35, 3, new THREE.MeshStandardMaterial({ color: 0xe9e6e0, roughness: .6 })); at(can, -12, 3.6, 1.5); B.add(can);
  const canE = box(10, .1, .05, new THREE.MeshStandardMaterial({ color: 0xf26a1b, emissive: dark ? 0x7a2a00 : 0 })); at(canE, -12, 3.45, 3.02); B.add(canE);
  // trees
  const trunkM = new THREE.MeshStandardMaterial({ color: 0x3a3028 }), leafM = new THREE.MeshStandardMaterial({ color: dark ? 0x1f2a22 : 0x55684a, roughness: .9 });
  for (const [x, z, s] of [[-44, 12, 1], [8, 9, 1.1], [-26, 15, .8]]) {
    const t = cyl(.18 * s, .25 * s, 4 * s, trunkM, 12); at(t, x, 2 * s, z); scene.add(t);
    for (let q = 0; q < 6; q++) { const sp = mesh(new THREE.IcosahedronGeometry((1.6 + r()) * s, 1), leafM); at(sp, x + (r() - .5) * 2 * s, (4.6 + r() * 2) * s, z + (r() - .5) * 2 * s); scene.add(sp); }
  }
  // camera — low eye-level, two-point-ish
  const asp = W / H;
  camera.fov = asp < .7 ? 52 : 38; camera.updateProjectionMatrix();
  const camPos = asp < .7 ? new THREE.Vector3(16, 1.7, 44) : new THREE.Vector3(22, 1.7, 40);
  camera.position.copy(camPos); camera.lookAt(-14, asp < .7 ? 15 : 9, -4);
  renderer.render(scene, camera);
  document.title = 'done';
}


// ================================================================== 3D NODES (stepped cutaway)
// local frame: x along facade, y up, z out of wall (wall face at z=0)
function seg(len, hgt, o = {}) {
  const g = new THREE.Group();
  const WT = 200, IT = 100, GAP = 40, PT = 8, PZ = IT + GAP + 54;
  const cut = o.cut ?? 'end', st = (k) => cut ? k * 90 : 0;
  const span = (k, a0 = 0) => cut === 'start' ? [a0 + st(k), len] : cut === 'end' ? [a0, len - st(k)] : [a0, len];
  const B = (a, b2, y0, y1, z, d, m, r = 0) => { if (b2 - a <= 1) return; const x = box(b2 - a, y1 - y0, d, m, r); at(x, (a + b2) / 2, (y0 + y1) / 2, z); g.add(x); };
  if (!o.noWall) B(o.wallA ?? 0, len, 0, hgt, -WT / 2, WT, M.concrete());
  const bx = o.bx ?? [len * .3, len * .72], by = o.by ?? [hgt * .2, hgt * .75];
  for (const x of bx) for (const y of by) { const br = bracket(y < hgt / 2); br.scale.setScalar(.9); at(br, x, y, 2, 0, Math.PI / 2, 0); g.add(br); }
  const [ia, ib] = span(1, o.insA ?? 0);
  B(ia, ib, 0, hgt * .5 - 2, IT / 2, IT, M.wool(), 4); B(ia, ib, hgt * .5 + 2, hgt, IT / 2, IT, M.wool(), 4);
  const [ma, mb] = span(2, o.insA ?? 0); B(ma, mb, 0, hgt, IT + 1, 1.2, M.membrane());
  const [pa, pb] = span(3, o.panA ?? 0);
  for (const x of bx) if (x > pa - 60 && x < len) {
    const pr = x === bx[0] ? Tprofile(hgt, 80, 50, 2) : Lprofile(hgt, 40, 50, 2);
    pr.rotation.set(-Math.PI / 2, 0, Math.PI); pr.position.set(x + 20, 0, IT + GAP + 2); g.add(pr);
  }
  const joints = o.joints ?? [], ys = [...joints, hgt]; let y0 = 0;
  ys.forEach((y1, idx) => {
    const top = y1 - (idx < ys.length - 1 ? 8 : 0);
    B(pa, pb, y0, top, PZ + PT / 2, PT, [M.hplCore(), M.hplCore(), M.hplCore(), M.hplCore(), M.hpl(o.color || '#2a2c30'), M.hpl()]);
    if (o.fix !== 'glue' && o.fix !== 'hidden') for (const x of bx) if (x > pa + 15 && x < pb - 15) for (const yy of [y0 + 50, top - 50]) {
      const rv = rivet(); rv.scale.setScalar(.9); at(rv, x, yy, PZ + PT, Math.PI / 2); g.add(rv); }
    y0 = y1;
  });
  return g;
}

function nodeScene(kind) {
  const G = new THREE.Group();
  const fix = Q.get('fix') || 'rivet';
  const PZ = 194, ZP = 202;
  const rot = (o, th, x, z) => { o.rotation.y = th; o.position.set(x, 0, z); return o; };
  if (kind === 'outer_corner') {
    G.add(seg(700, 800, { fix, insA: -100, panA: -ZP - 4 }));
    G.add(rot(seg(600, 800, { fix, cut: 'start' }), -Math.PI / 2, 0, -600));
    const L = Lprofile(800, 50, 50, 2); L.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); L.position.set(-PZ + 50, 0, PZ - 4); G.add(L);
  } else if (kind === 'inner_corner') {
    G.add(seg(700, 800, { fix, insA: 100, panA: ZP + 14 }));
    G.add(rot(seg(600, 800, { fix, cut: 'start', noWall: false }), Math.PI / 2, 0, 600));
  } else if (kind === 'window') {
    const W0 = 260, W1 = 620, H0 = 300, H1 = 760, HT = 1000, LT = 900;
    G.add(seg(W0, HT, { fix, cut: 0, joints: [H0] }));
    const r = seg(LT - W1, HT, { fix, joints: [H0] }); r.position.x = W1; G.add(r);
    const bt = seg(W1 - W0, H0, { fix, cut: 0, bx: [] }); bt.position.x = W0; G.add(bt);
    const tp = seg(W1 - W0, HT - H1, { fix, cut: 0, bx: [] }); tp.position.set(W0, H1, 0); G.add(tp);
    const glass = new THREE.MeshPhysicalMaterial({ color: 0x8fa7ba, roughness: .04, clearcoat: 1, metalness: .1 });
    G.add(at(box(W1 - W0 - 60, H1 - H0 - 60, 6, glass), (W0 + W1) / 2, (H0 + H1) / 2, -60));
    const fm = M.white(); const fw = 40;
    G.add(at(box(W1 - W0, fw, 80, fm), (W0 + W1) / 2, H0 + fw / 2, -60)); G.add(at(box(W1 - W0, fw, 80, fm), (W0 + W1) / 2, H1 - fw / 2, -60));
    G.add(at(box(fw, H1 - H0, 80, fm), W0 + fw / 2, (H0 + H1) / 2, -60)); G.add(at(box(fw, H1 - H0, 80, fm), W1 - fw / 2, (H0 + H1) / 2, -60));
    const rev = [M.hplCore(), M.hplCore(), M.hpl(), M.hpl(), M.hplCore(), M.hplCore()];
    G.add(at(box(8, H1 - H0, 280, [M.hpl(), M.hpl(), M.hplCore(), M.hplCore(), M.hplCore(), M.hplCore()]), W0 + 4, (H0 + H1) / 2, 62));
    G.add(at(box(8, H1 - H0, 280, [M.hpl(), M.hpl(), M.hplCore(), M.hplCore(), M.hplCore(), M.hplCore()]), W1 - 4, (H0 + H1) / 2, 62));
    G.add(at(box(W1 - W0, 8, 280, rev), (W0 + W1) / 2, H1 - 4, 62));
    G.add(at(box(W1 - W0 + 40, 3, 300, M.alu()), (W0 + W1) / 2, H0 + 2, 80, .1, 0, 0));
    G.add(at(box(W1 - W0 + 40, 30, 3, M.alu()), (W0 + W1) / 2, H0 - 26, 228));
  } else if (kind === 'base') {
    G.add(seg(800, 800, { fix }));
    G.add(at(box(800, 4, 200, M.alu()), 400, -6, 100));
    for (let i = 0; i < 40; i++) G.add(at(box(8, 5, 120, M.rubber()), 10 + i * 20, -4, 90));
    G.add(at(box(800, 30, 4, M.alu()), 400, -18, 198));
    G.add(at(box(900, 300, 420, M.concrete()), 450, -180, -10));
  } else if (kind === 'parapet') {
    G.add(seg(800, 800, { fix }));
    G.add(at(box(800, 160, 200, M.concrete()), 400, 880, -100));
    G.add(at(box(820, 4, 470, M.alu()), 410, 968, 20, -.05, 0, 0));
    G.add(at(box(820, 90, 4, M.alu()), 410, 920, 254));
    G.add(at(box(820, 50, 4, M.alu()), 410, 940, -214));
  } else if (kind === 'hjoint') {
    G.add(seg(800, 900, { fix, joints: [450] }));
  } else if (kind === 'vjoint') {
    G.add(seg(500, 900, { fix, cut: 0, bx: [180, 492] }));
    const r = seg(500, 900, { fix, bx: [40, 330], panA: 8 }); r.position.x = 500; G.add(r);
  }
  return G;
}

async function nodeMain() {
  const key = await studio();
  const kind = NAME.slice(5);
  const grp = new THREE.Group(); grp.add(nodeScene(kind)); scene.add(grp);
  let bb = new THREE.Box3().setFromObject(grp); const size = bb.getSize(new THREE.Vector3());
  grp.scale.setScalar(1 / Math.max(size.x, size.y, size.z));
  bb = new THREE.Box3().setFromObject(grp); const c = bb.getCenter(new THREE.Vector3());
  grp.position.sub(new THREE.Vector3(c.x, bb.min.y, c.z));
  grp.rotation.y = +(Q.get('yaw') ?? -0.6);
  bb = new THREE.Box3().setFromObject(grp); const c2 = bb.getCenter(new THREE.Vector3()); const s2 = bb.getSize(new THREE.Vector3());
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(20, 20), new THREE.ShadowMaterial({ opacity: .18 }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = bb.min.y; ground.receiveShadow = true; scene.add(ground);
  key.shadow.camera.left = key.shadow.camera.bottom = -2; key.shadow.camera.right = key.shadow.camera.top = 2; key.target.position.copy(c2); scene.add(key.target);
  const pitch = +(Q.get('pitch') ?? .38);
  const dist = s2.length() * .5 / Math.sin(THREE.MathUtils.degToRad(camera.fov / 2)) * 1.1;
  camera.position.set(c2.x, c2.y + Math.sin(pitch) * dist, c2.z + Math.cos(pitch) * dist); camera.lookAt(c2);
  renderer.render(scene, camera); document.title = 'done';
}
