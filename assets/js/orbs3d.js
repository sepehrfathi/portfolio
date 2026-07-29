/* Sepehr Fathi — 3D tech orbs (about section).
 *
 * Progressive enhancement: the CSS orbs in the markup are the baseline and stay
 * put if anything here bails (no WebGL, reduced motion, module load failure).
 * Only once the scene is actually rendering do we hide them and show the canvas.
 *
 * Vendored three.js — no CDN, no external request. See assets/vendor/.
 */
import * as THREE from "../vendor/three.module.min.js?v=5";

const field = document.querySelector("[data-orbs]");
if (field) init(field);

function init(field) {
  const reduced =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) return;

  const nodes = Array.prototype.slice.call(field.querySelectorAll(".orb"));
  if (!nodes.length) return;

  // Read layout straight off the CSS orbs so the 2D and 3D versions agree and
  // there is only one place to tune the scatter.
  const specs = nodes.map((el) => {
    const cs = getComputedStyle(el);
    const pct = (v) => parseFloat(v) / 100;
    const s = pct(cs.getPropertyValue("--s"));
    return {
      img: el.querySelector("img"),
      cx: pct(cs.getPropertyValue("--x")) + s / 2, // centre, 0..1 of the field
      cy: pct(cs.getPropertyValue("--y")) + s / 2,
      r: s / 2,
    };
  });

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  } catch (e) {
    return; // no WebGL — CSS orbs stay
  }

  const canvas = renderer.domElement;
  canvas.className = "orbs__canvas";
  field.appendChild(canvas);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  const scene = new THREE.Scene();
  // Orthographic keeps every orb the same visual scale regardless of where it
  // sits in the field — a perspective camera made the corner ones read smaller
  // than their CSS counterparts.
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 100);
  camera.position.set(0, 0, 10);

  const key = new THREE.DirectionalLight(0xffffff, 2.6);
  key.position.set(-3, 4, 5);
  const rim = new THREE.DirectionalLight(0xbdd4f5, 1.1);
  rim.position.set(4, -2, 2);
  const ambient = new THREE.AmbientLight(0xffffff, 0.75);
  scene.add(key, rim, ambient);

  // Faceted solid, not a smooth sphere — this is the look from the reference.
  const geometry = new THREE.IcosahedronGeometry(1, 1);
  const loader = new THREE.TextureLoader();
  const orbs = [];

  specs.forEach((spec, i) => {
    const group = new THREE.Group();

    const material = new THREE.MeshStandardMaterial({
      color: 0xf2f5fa,
      roughness: 0.55,
      metalness: 0.0,
      flatShading: true, // gives each triangle its own shade — the faceted look
    });
    const ball = new THREE.Mesh(geometry, material);
    group.add(ball);

    // Logo decal on the front face, riding just clear of the hull so it swings
    // with the solid and disappears round the back like a real sticker.
    let badge = null;
    if (spec.img && spec.img.getAttribute("src")) {
      const tex = loader.load(spec.img.getAttribute("src"));
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.anisotropy = 4;
      const mat = new THREE.MeshBasicMaterial({
        map: tex,
        transparent: true,
        depthWrite: false,
      });
      badge = new THREE.Mesh(new THREE.PlaneGeometry(1.12, 1.12), mat);
      badge.position.z = 1.02;
      group.add(badge);
    }

    scene.add(group);
    orbs.push({
      group,
      material,
      badge,
      spec,
      phase: i * 1.9,
      speed: 0.55 + (i % 4) * 0.13,
      swing: 0.16 + (i % 3) * 0.05,
    });
  });

  // ---- theme ----
  const applyTheme = () => {
    const root = document.documentElement;
    const attr = root.getAttribute("data-theme");
    const dark =
      attr === "dark" ||
      (attr !== "light" &&
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches);
    // The solids stay light in both themes (the logos are full colour and need
    // a pale body to read against); only the lighting balance shifts.
    orbs.forEach((o) => {
      o.material.color.set(dark ? 0xdfe6f2 : 0xf2f5fa);
    });
    ambient.intensity = dark ? 0.5 : 0.8;
    rim.color.set(dark ? 0x7aa7ea : 0xbdd4f5);
  };
  applyTheme();
  new MutationObserver(applyTheme).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
  if (window.matchMedia) {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", applyTheme);
  }

  // ---- layout ----
  // World units: the field is 2 units wide, so a spec radius of 0.15 (15% of the
  // field) becomes 0.3 world units.
  function layout() {
    const w = field.clientWidth;
    const h = field.clientHeight || w;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    const aspect = w / h;
    camera.left = -aspect;
    camera.right = aspect;
    camera.top = 1;
    camera.bottom = -1;
    camera.updateProjectionMatrix();

    orbs.forEach((o) => {
      const r = o.spec.r * 2 * aspect; // radius scales with field width
      o.group.scale.setScalar(r);
      o.baseX = (o.spec.cx * 2 - 1) * aspect;
      o.baseY = 1 - o.spec.cy * 2;
      o.group.position.set(o.baseX, o.baseY, 0);
    });
  }
  layout();
  window.addEventListener("resize", layout, { passive: true });

  // ---- pointer parallax ----
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  field.addEventListener(
    "pointermove",
    (e) => {
      const b = field.getBoundingClientRect();
      pointer.tx = ((e.clientX - b.left) / b.width) * 2 - 1;
      pointer.ty = ((e.clientY - b.top) / b.height) * 2 - 1;
    },
    { passive: true }
  );
  field.addEventListener("pointerleave", () => {
    pointer.tx = 0;
    pointer.ty = 0;
  });

  // ---- loop, only while on screen ----
  let visible = false;
  let raf = 0;
  let t0 = 0;
  let elapsed = 0;

  const frame = (now) => {
    raf = requestAnimationFrame(frame);
    if (!t0) t0 = now;
    const dt = Math.min((now - t0) / 1000, 0.05);
    t0 = now;
    elapsed += dt;

    pointer.x += (pointer.tx - pointer.x) * 0.06;
    pointer.y += (pointer.ty - pointer.y) * 0.06;

    orbs.forEach((o) => {
      const p = elapsed * o.speed + o.phase;
      o.group.position.y = o.baseY + Math.sin(p) * 0.055;
      o.group.position.x = o.baseX + Math.cos(p * 0.7) * 0.022;
      // gentle swing, never far enough to hide the badge round the back
      o.group.rotation.y = Math.sin(p * 0.6) * o.swing + pointer.x * 0.35;
      o.group.rotation.x = Math.cos(p * 0.5) * o.swing * 0.6 - pointer.y * 0.28;
    });

    renderer.render(scene, camera);
  };

  const start = () => {
    if (raf) return;
    t0 = 0;
    raf = requestAnimationFrame(frame);
  };
  const stop = () => {
    cancelAnimationFrame(raf);
    raf = 0;
  };

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(
      (entries) => {
        visible = entries[0].isIntersecting;
        if (visible && !document.hidden) start();
        else stop();
      },
      { rootMargin: "120px" }
    ).observe(field);
  } else {
    visible = true;
    start();
  }
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stop();
    else if (visible) start();
  });

  // One frame is on screen — now it is safe to hand over from the CSS orbs.
  renderer.render(scene, camera);
  field.classList.add("is-3d");
}
