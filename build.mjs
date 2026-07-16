/* =========================================================================
   build.mjs — static multilingual site generator (zero dependencies)
   Reads content/<lang>.json + shared assets → emits one SEO-correct,
   self-contained HTML page per language, plus sitemap / robots / manifest.
   Run:  node build.mjs
   ========================================================================= */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));

/* ----------------------------- CONFIG ----------------------------------- */
// ▶ Set this to your real domain (used for canonical, hreflang & sitemap).
const BASE_URL = "https://sep.onwebs.dev";

// ▶ Confirm / edit these links (used in header, contact & résumé).
const LINKS = {
  github: "https://github.com/sepehrfathi",
  linkedin: "https://www.linkedin.com/in/sepehr-fathi",
  telegram: "https://t.me/sepehrfathi",
};

// Language table. Order = nav/menu order. First with `default:true` is x-default.
const LANGS = [
  { code: "fa", name: "فارسی",     htmlLang: "fa",      hreflang: "fa",    dir: "rtl", locale: "fa_IR", default: true },
  { code: "en", name: "English",   htmlLang: "en",      hreflang: "en",    dir: "ltr", locale: "en_US" },
  { code: "ar", name: "العربية",   htmlLang: "ar",      hreflang: "ar",    dir: "rtl", locale: "ar_AR" },
  { code: "zh", name: "简体中文",   htmlLang: "zh-Hans", hreflang: "zh-Hans", dir: "ltr", locale: "zh_CN" },
  { code: "ru", name: "Русский",   htmlLang: "ru",      hreflang: "ru",    dir: "ltr", locale: "ru_RU" },
  { code: "es", name: "Español",   htmlLang: "es",      hreflang: "es",    dir: "ltr", locale: "es_ES" },
  { code: "no", name: "Norsk",     htmlLang: "nb",      hreflang: "nb-NO", dir: "ltr", locale: "nb_NO" },
];

/* ----------------------------- HELPERS ---------------------------------- */
const esc = (s) => String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const escA = (s) => esc(s).replace(/"/g, "&quot;");
const url = (code) => `${BASE_URL}/${code}/`;

/* Inline SVG icon set (stroke, currentColor). */
const I = {
  mail: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></svg>`,
  arrow: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>`,
  pin: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>`,
  spark: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/></svg>`,
  star: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="m12 2 2.6 6.3L21 9l-5 4.3L17.5 20 12 16.3 6.5 20 8 13.3 3 9l6.4-.7L12 2Z"/></svg>`,
  shield: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 5-3.5 8-7 10-3.5-2-7-5-7-10V6l7-3Z"/><path d="m9 12 2 2 4-4"/></svg>`,
  quote: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M7 7h5v6a4 4 0 0 1-4 4H7v-2h1a2 2 0 0 0 2-2v-1H7V7Zm8 0h5v6a4 4 0 0 1-4 4h-1v-2h1a2 2 0 0 0 2-2v-1h-3V7Z"/></svg>`,
  copy: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M6 15H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v1"/></svg>`,
  sun: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>`,
  moon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>`,
  globe: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3Z"/></svg>`,
  menu: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>`,
  close: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>`,
  check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5 10 17l9-10"/></svg>`,
  lock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="4.5" y="10" width="15" height="10" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>`,
  github: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2C6.48 2 2 6.58 2 12.25c0 4.53 2.87 8.37 6.85 9.73.5.1.68-.22.68-.49l-.01-1.7c-2.79.62-3.38-1.22-3.38-1.22-.45-1.18-1.11-1.5-1.11-1.5-.91-.64.07-.62.07-.62 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.36 1.12 2.94.85.09-.66.35-1.12.63-1.38-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.71 0 0 .84-.28 2.75 1.05a9.4 9.4 0 0 1 5 0c1.91-1.33 2.75-1.05 2.75-1.05.55 1.41.2 2.45.1 2.71.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.81-4.57 5.06.36.32.68.94.68 1.9l-.01 2.82c0 .27.18.59.69.49A10.26 10.26 0 0 0 22 12.25C22 6.58 17.52 2 12 2Z"/></svg>`,
  linkedin: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M6.94 5a1.94 1.94 0 1 1-3.88 0 1.94 1.94 0 0 1 3.88 0ZM3.4 8.4h3.1V21H3.4V8.4Zm5.2 0h2.97v1.72h.04c.41-.78 1.42-1.6 2.93-1.6 3.13 0 3.71 2.06 3.71 4.74V21h-3.1v-5.58c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94V21H8.6V8.4Z"/></svg>`,
  telegram: `<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M21.9 4.6 18.6 20c-.24 1.08-.9 1.34-1.82.83l-5-3.68-2.42 2.33c-.27.27-.5.5-1 .5l.35-5.06L18.1 6.1c.4-.36-.09-.56-.62-.2L5.9 13.28.86 11.7c-1.1-.34-1.12-1.1.23-1.63L20.5 3.03c.9-.34 1.7.2 1.4 1.57Z"/></svg>`,
  user: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.2 3.6-6.5 8-6.5s8 2.3 8 6.5"/></svg>`,
  briefcase: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7.5" width="18" height="12.5" rx="2.5"/><path d="M8 7.5V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1.5M3 12h18"/></svg>`,
  grid: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"><rect x="3" y="3" width="7.5" height="7.5" rx="1.6"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.6"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.6"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.6"/></svg>`,
};

// Portfolio gallery — real client screenshots (assets/images/portfolio/).
const GALLERY = [
  { name: "Fanavaran Sabz", img: "fanavaransabz.webp", tag: "Web" },
  { name: "Talkoob", img: "talkoob.webp", tag: "Web" },
  { name: "Cuatro Group AS", img: "cuatro.webp", tag: "Norway · Web" },
  { name: "NanoMAR AS", img: "nanomar.webp", tag: "Norway · Web" },
  { name: "Kanoon (Farakanoon)", img: "kanoon.webp", tag: "Web" },
];

const socialsHTML = (cls) => `
  <a href="${escA(LINKS.github)}" target="_blank" rel="noopener" aria-label="GitHub" class="${cls}">${I.github}</a>
  <a href="${escA(LINKS.linkedin)}" target="_blank" rel="noopener" aria-label="LinkedIn" class="${cls}">${I.linkedin}</a>
  <a href="${escA(LINKS.telegram)}" target="_blank" rel="noopener" aria-label="Telegram" class="${cls}">${I.telegram}</a>`;

/* --------------------------- PAGE TEMPLATE ------------------------------ */
function renderPage(L, c, pages) {
  const m = c.meta || {};
  const nav = c.nav, hero = c.hero, contact = c.contact;
  const rtl = L.dir === "rtl";
  const relRoot = "../"; // pages live at /<code>/index.html
  const asset = (p) => relRoot + p;

  const alternates = pages
    .map((p) => `  <link rel="alternate" hreflang="${p.hreflang}" href="${escA(url(p.code))}" />`)
    .join("\n");
  const xDefault = pages.find((p) => p.default) || pages[0];

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Person",
    name: hero.name,
    jobTitle: hero.eyebrow,
    description: m.description,
    url: url(L.code),
    email: "mailto:" + contact.email,
    address: { "@type": "PostalAddress", addressLocality: "Mashhad", addressCountry: "IR" },
    sameAs: [LINKS.github, LINKS.linkedin, LINKS.telegram],
    knowsAbout: ["Prompt Engineering", "Applied AI", "Computer Vision", "Bioinformatics", "CAR-T", "Geospatial Intelligence", "Offline-first systems"],
    worksFor: [
      { "@type": "Organization", name: "Vira Web Aria" },
      { "@type": "Organization", name: "Nano Hobab Roshana" },
    ],
  };
  const ldStr = JSON.stringify(jsonLd, null, 0).replace(/</g, "\\u003c");

  /* menu links (to sibling language folders) */
  const menuLinks = pages.map((p) =>
    `<a href="../${p.code}/" hreflang="${p.hreflang}"${p.code === L.code ? ' aria-current="true"' : ""}>${esc(p.name)}<span>${p.hreflang}</span></a>`
  ).join("");

  const navItems = [
    ["#about", nav.about], ["#roles", nav.roles], ["#ventures", nav.ventures],
    ["#skills", nav.skills], ["#prompt", nav.prompt], ["#work", nav.work], ["#contact", nav.contact],
  ];
  const navHTML = navItems.map(([h, t]) => `<a href="${h}">${esc(t)}</a>`).join("");
  const mobileNavHTML = navItems.map(([h, t]) => `<a href="${h}" class="mlink">${esc(t)}<span>${I.arrow}</span></a>`).join("");

  /* sections */
  const statsHTML = (c.highlights || []).map((s) =>
    `<div class="stat reveal"><div class="stat__num">${esc(s.value)}</div><div class="stat__label">${esc(s.label)}</div></div>`
  ).join("");

  const aboutBody = (c.about.paragraphs || []).map((p) => `<p>${esc(p)}</p>`).join("");
  const aboutChips = (c.about.chips || []).map((ch, i) => `<span class="chip${i === 0 ? " chip--brand" : ""}">${esc(ch)}</span>`).join("");

  const rolesHTML = (c.roles.items || []).map((r) => `
      <article class="role reveal">
        <div><span class="role__badge">${esc(r.type)}</span></div>
        <div class="role__main">
          <h3 class="role__org">${esc(r.org)}</h3>
          <div class="role__role">${esc(r.role)}</div>
          <p class="role__detail">${esc(r.detail)}</p>
          ${r.location ? `<span class="role__loc">${I.pin}${esc(r.location)}</span>` : ""}
        </div>
      </article>`).join("");

  const venturesHTML = (c.ventures.items || []).map((v, i) => {
    const points = (v.points || []).map((p) => `<li>${esc(p)}</li>`).join("");
    const stack = (v.stack || []).map((s) => `<span class="tag">${esc(s)}</span>`).join("");
    return `
      <article class="venture reveal${i === 0 ? " venture--wide" : ""}">
        <div class="venture__head">
          <h3 class="venture__name">${esc(v.name)}</h3>
          <span class="venture__kicker">${esc(v.kicker)}</span>
        </div>
        <p class="venture__summary">${esc(v.summary)}</p>
        <ul class="venture__points">${points}</ul>
        <div class="venture__foot">
          <div class="venture__stack">${stack}</div>
          ${v.metric ? `<div class="venture__metric"><b>${esc(v.metric.value)}</b><span>${esc(v.metric.label)}</span></div>` : ""}
        </div>
      </article>`;
  }).join("");

  const promptCards = (c.prompt.points || []).map((p, i) => `
        <div class="pf-card reveal">
          <span class="pf-card__n">0${i + 1}</span>
          <h4>${esc(p.title)}</h4>
          <p>${esc(p.text)}</p>
        </div>`).join("");

  const skillsHTML = (c.skills.groups || []).map((g) => {
    const items = (g.items || []).map((it) => `<li>${esc(it)}</li>`).join("");
    return `
      <div class="skillgroup${g.featured ? " skillgroup--feat" : ""} reveal">
        <h3>${g.featured ? `<span class="star">${I.star}</span>` : ""}${esc(g.name)}</h3>
        <ul class="skillgroup__items">${items}</ul>
      </div>`;
  }).join("");

  const workHTML = (c.work.items || []).map((w) =>
    `<div class="work__item"><h4>${esc(w.title)}</h4><span class="tag">${esc(w.tag)}</span></div>`
  ).join("");

  const galleryHTML = GALLERY.map((g) =>
    `<figure class="shot reveal">
        <div class="shot__img"><img loading="lazy" decoding="async" src="${escA(asset("assets/images/portfolio/" + g.img))}" alt="${escA(g.name)}" /></div>
        <figcaption><b>${esc(g.name)}</b><span class="tag">${esc(g.tag)}</span></figcaption>
      </figure>`).join("");

  const dockItems = [
    ["#about", nav.about, I.user], ["#ventures", nav.ventures, I.briefcase],
    ["#skills", nav.skills, I.grid], ["#prompt", nav.prompt, I.spark], ["#contact", nav.contact, I.mail],
  ];
  const dockHTML = dockItems.map(([h, t, ic]) =>
    `<a href="${h}" class="dock__item" aria-label="${escA(t)}"><span class="dock__ic">${ic}</span><span class="dock__lbl">${esc(t)}</span></a>`
  ).join("");

  const channels = `
        <a class="channel" href="mailto:${escA(contact.email)}">${I.mail}${esc(contact.emailLabel)}</a>
        <a class="channel" href="${escA(LINKS.github)}" target="_blank" rel="noopener">${I.github}${esc(contact.channels.github)}</a>
        <a class="channel" href="${escA(LINKS.linkedin)}" target="_blank" rel="noopener">${I.linkedin}${esc(contact.channels.linkedin)}</a>
        <a class="channel" href="${escA(LINKS.telegram)}" target="_blank" rel="noopener">${I.telegram}${esc(contact.channels.telegram)}</a>
        <span class="channel">${I.pin}${esc(contact.channels.location)}</span>`;

  /* résumé (print only) */
  const R = c.resume;
  const rHigh = (c.highlights || []).map((s) => `<div><b>${esc(s.value)}</b><span>${esc(s.label)}</span></div>`).join("");
  const rExp = (c.roles.items || []).map((r) => `
        <div class="r-exp">
          <div class="r-exp-h"><span class="r-exp-org">${esc(r.org)}</span><span class="r-exp-loc">${esc(r.location || "")}</span></div>
          <div class="r-exp-role">${esc(r.role)}</div>
          <p>${esc(r.detail)}</p>
        </div>`).join("");
  const rVent = (c.ventures.items || []).map((v) => `
        <div class="r-vent"><b>${esc(v.name)}</b><i>${esc(v.kicker)}</i><p>${esc(v.summary)}</p></div>`).join("");
  const rSkills = (c.skills.groups || []).map((g) => `<div><b>${esc(g.name)}:</b> ${esc((g.items || []).join(" · "))}</div>`).join("");
  const rWork = (c.work.items || []).map((w) => `<span>${esc(w.title)} — ${esc(w.tag)}</span>`).join("");

  const resumeDoc = `
    <div class="resume-doc" aria-hidden="true">
      <div class="r-head">
        <div><div class="r-name">${esc(hero.name)}</div><div class="r-title">${esc(hero.eyebrow)}</div></div>
        <div class="r-contact">
          <div><a href="mailto:${escA(contact.email)}">${esc(contact.email)}</a></div>
          <div>${esc(LINKS.github.replace(/^https?:\/\//, ""))}</div>
          <div>${esc(LINKS.linkedin.replace(/^https?:\/\/(www\.)?/, ""))}</div>
          <div>${esc(contact.channels.location)}</div>
        </div>
      </div>
      <div class="r-sec"><h2>${esc(R.summary)}</h2><p class="r-summary">${esc(c.about.lead)} ${esc((c.about.paragraphs || [])[0] || "")}</p></div>
      <div class="r-sec"><h2>${esc(R.highlights)}</h2><div class="r-high">${rHigh}</div></div>
      <div class="r-sec"><h2>${esc(R.experience)}</h2>${rExp}</div>
      <div class="r-sec"><h2>${esc(R.ventures)}</h2>${rVent}</div>
      <div class="r-sec"><h2>${esc(R.skills)}</h2><div class="r-skills">${rSkills}</div></div>
      <div class="r-sec"><h2>${esc(R.work)}</h2><div class="r-work">${rWork}</div></div>
      <div class="r-foot">${esc(hero.name)} · ${esc(BASE_URL.replace(/^https?:\/\//, ""))} · <span data-year></span></div>
    </div>`;

  /* ----- full document ----- */
  return `<!doctype html>
<html lang="${escA(L.htmlLang)}" dir="${L.dir}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="color-scheme" content="light dark" />
  <meta name="theme-color" content="#fcfcfb" />
  <title>${esc(m.title)}</title>
  <meta name="description" content="${escA(m.description)}" />
  <meta name="keywords" content="${escA(m.keywords)}" />
  <meta name="author" content="${escA(hero.name)}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="${escA(url(L.code))}" />
${alternates}
  <link rel="alternate" hreflang="x-default" href="${escA(url(xDefault.code))}" />
  <meta property="og:type" content="profile" />
  <meta property="og:site_name" content="${escA(hero.name)}" />
  <meta property="og:title" content="${escA(m.title)}" />
  <meta property="og:description" content="${escA(m.description)}" />
  <meta property="og:url" content="${escA(url(L.code))}" />
  <meta property="og:locale" content="${escA(m.locale || L.locale)}" />
  <meta property="og:image" content="${escA(BASE_URL + "/assets/images/sepehrfathi.webp")}" />
  <meta property="og:image:alt" content="${escA(hero.name)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="${escA(m.title)}" />
  <meta name="twitter:description" content="${escA(m.description)}" />
  <meta name="twitter:image" content="${escA(BASE_URL + "/assets/images/sepehrfathi.webp")}" />
  <link rel="icon" type="image/png" sizes="512x512" href="${escA(asset("favicon.png"))}" />
  <link rel="icon" type="image/png" sizes="32x32" href="${escA(asset("favicon-32.png"))}" />
  <link rel="apple-touch-icon" href="${escA(asset("apple-touch-icon.png"))}" />
  <link rel="manifest" href="${escA(asset("manifest.webmanifest"))}" />
  <link rel="stylesheet" href="${escA(asset("assets/css/styles.css"))}" />
  <script type="application/ld+json">${ldStr}</script>
</head>
<body>
  <header class="header">
    <div class="container header__bar">
      <a href="#" class="brand" aria-label="${escA(hero.name)}">
        <img class="brand__logo" src="${escA(asset("assets/images/sepehrfathi.webp"))}" alt="${escA(hero.name)}" width="673" height="590" />
      </a>
      <nav class="nav" aria-label="Primary">${navHTML}</nav>
      <div class="header__actions">
        <button class="icon-btn" data-theme-btn aria-label="${escA(c.ui.theme)}" aria-pressed="false">
          <span class="only-dark">${I.sun}</span><span class="only-light">${I.moon}</span>
        </button>
        <div class="menu-wrap" data-lang-wrap>
          <button class="icon-btn" data-lang-btn aria-label="${escA(c.ui.language)}" aria-haspopup="true" aria-expanded="false">${I.globe}</button>
          <div class="menu" data-lang-menu role="menu">${menuLinks}</div>
        </div>
        <a href="#" class="btn btn--primary btn--sm" data-print>${I.arrow}${esc(nav.resume)}</a>
      </div>
    </div>
  </header>

  <div class="site">
    <!-- HERO -->
    <section class="hero" id="top">
      <div class="hero__glow" aria-hidden="true"></div>
      <div class="container hero__inner">
        <div class="hero__text">
          <span class="hero__eyebrow reveal">${esc(hero.eyebrow)}</span>
          <h1 class="hero__name reveal">${esc(hero.name)}</h1>
          <p class="hero__role reveal">${esc(hero.roleLine)}</p>
          <div class="hero__meta reveal"><span>${I.pin}${esc(hero.location)}</span></div>
          <div class="hero__cta reveal">
            <a href="#" class="btn btn--primary" data-print>${I.arrow}${esc(hero.ctaResume)}</a>
            <a href="#contact" class="btn btn--ghost">${esc(hero.ctaContact)}</a>
            <a href="#ventures" class="btn btn--ghost">${esc(hero.ctaWork)}</a>
          </div>
          <div class="hero__socials reveal">${socialsHTML("")}</div>
        </div>
        <div class="hero__photo reveal" aria-hidden="false">
          <span class="hero__photo-ring" aria-hidden="true"></span>
          <img src="${escA(asset("assets/images/sepehrft.png"))}" alt="${escA(hero.photoAlt || hero.name)}" width="520" height="480" loading="eager" decoding="async" />
        </div>
      </div>
    </section>

    <!-- STATS -->
    <section class="container" style="padding-block:0 var(--section-y)">
      <div class="stats">${statsHTML}</div>
    </section>

    <!-- ABOUT -->
    <section class="section" id="about">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">${esc(nav.about)}</span>
          <h2 class="section-title">${esc(c.about.title)}</h2>
        </div>
        <div class="about__grid">
          <div>
            <p class="about__lead reveal">${esc(c.about.lead)}</p>
            <div class="about__body">${aboutBody}</div>
          </div>
          <div class="reveal">
            <div class="about__chips">${aboutChips}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ROLES -->
    <section class="section" id="roles">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">${esc(nav.roles)}</span>
          <h2 class="section-title">${esc(c.roles.title)}</h2>
          <p class="section-sub">${esc(c.roles.subtitle)}</p>
        </div>
        <div class="roles__list">${rolesHTML}</div>
      </div>
    </section>

    <!-- VENTURES -->
    <section class="section" id="ventures">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">${esc(nav.ventures)}</span>
          <h2 class="section-title">${esc(c.ventures.title)}</h2>
          <p class="section-sub">${esc(c.ventures.subtitle)}</p>
        </div>
        <div class="ventures__grid">${venturesHTML}</div>
      </div>
    </section>

    <!-- PORTFOLIO GALLERY -->
    <section class="section" id="portfolio">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">${I.grid}Onwebs</span>
          <h2 class="section-title">${esc(c.gallery.title)}</h2>
          <p class="section-sub">${esc(c.gallery.subtitle)}</p>
        </div>
        <div class="gallery__grid">${galleryHTML}</div>
      </div>
    </section>

    <!-- PROMPT ENGINEERING -->
    <section class="section" id="prompt">
      <div class="container">
        <div class="promptfx reveal">
          <span class="eyebrow">${I.spark}${esc(c.prompt.kicker)}</span>
          <h2 class="section-title">${esc(c.prompt.title)}</h2>
          <p class="promptfx__lead">${esc(c.prompt.lead)}</p>
          <div class="promptfx__grid">${promptCards}</div>
          <p class="promptfx__note">${I.quote}${esc(c.prompt.note)}</p>
        </div>
      </div>
    </section>

    <!-- SKILLS -->
    <section class="section" id="skills">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">${esc(nav.skills)}</span>
          <h2 class="section-title">${esc(c.skills.title)}</h2>
          <p class="section-sub">${esc(c.skills.subtitle)}</p>
        </div>
        <div class="skills__grid">${skillsHTML}</div>
      </div>
    </section>

    <!-- SELECTED WORK -->
    <section class="section" id="work">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">${esc(nav.work)}</span>
          <h2 class="section-title">${esc(c.work.title)}</h2>
          <p class="section-sub">${esc(c.work.subtitle)}</p>
        </div>
        <div class="work__list">${workHTML}</div>
        <p class="work__note">${I.lock}${esc(c.work.note)}</p>
      </div>
    </section>

    <!-- CONTACT -->
    <section class="section contact" id="contact">
      <div class="container">
        <div class="contact__card reveal">
          <span class="eyebrow" style="justify-content:center">${esc(contact.subtitle)}</span>
          <h2 class="contact__title">${esc(contact.title)}</h2>
          <p class="contact__lead">${esc(contact.lead)}</p>
          <div class="contact__email">
            <a href="mailto:${escA(contact.email)}">${esc(contact.email)}</a>
            <button class="copy-btn" data-copy="${escA(contact.email)}" data-copied="${escA(contact.copied)}">${I.copy}<span class="copy-label">${esc(contact.copy)}</span></button>
          </div>
          <div class="contact__channels">${channels}</div>
        </div>
      </div>
    </section>
  </div>

  <footer class="footer">
    <div class="container footer__grid">
      <div>
        <img class="footer__logo" src="${escA(asset("assets/images/sepehrfathi.webp"))}" alt="${escA(hero.name)}" width="673" height="590" />
        <div class="footer__tag">${esc(hero.eyebrow)}</div>
      </div>
      <div class="footer__socials">${socialsHTML("")}</div>
    </div>
    <div class="container" style="margin-top:1.4rem">
      <div class="footer__rights">© <span data-year></span> ${esc(hero.name)}. ${esc(c.footer.rights)}</div>
    </div>
  </footer>

  <nav class="dock" aria-label="Primary">${dockHTML}</nav>

  ${resumeDoc}

  <script src="${escA(asset("assets/js/app.js"))}" defer></script>
</body>
</html>
`;
}

/* ------------------------------- ROOT ----------------------------------- */
function renderRoot(pages) {
  const xd = pages.find((p) => p.default) || pages[0];
  const alt = pages.map((p) => `  <link rel="alternate" hreflang="${p.hreflang}" href="${escA(url(p.code))}" />`).join("\n");
  const links = pages.map((p) => `<a href="./${p.code}/" hreflang="${p.hreflang}" style="display:inline-block;margin:.3rem .5rem;padding:.5rem .9rem;border:1px solid #ccc;border-radius:999px;color:inherit;text-decoration:none">${esc(p.name)}</a>`).join("");
  const map = pages.map((p) => `"${p.htmlLang.split("-")[0]}":"${p.code}"`).join(",");
  return `<!doctype html>
<html lang="${escA(xd.htmlLang)}" dir="${xd.dir}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sepehr Fathi — Deep-Tech Founder & Senior Software Engineer</title>
  <meta name="description" content="Sepehr Fathi — deep-tech founder & senior software engineer. Applied AI, computer vision, geospatial intelligence, bioinformatics. Offline-first, sovereign, honest engineering." />
  <link rel="canonical" href="${escA(url(xd.code))}" />
${alt}
  <link rel="alternate" hreflang="x-default" href="${escA(url(xd.code))}" />
  <link rel="icon" type="image/png" href="favicon.png" />
  <meta http-equiv="refresh" content="0; url=./${xd.code}/" />
  <style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#fcfcfb;color:#0c0f0e;display:grid;place-items:center;min-height:100vh;margin:0;text-align:center;padding:2rem}@media(prefers-color-scheme:dark){body{background:#080a0a;color:#ecf1ef}}h1{font-size:1.4rem;font-weight:800;margin:0 0 .3rem}p{color:#717b79;margin:0 0 1.5rem}</style>
  <script>
    (function(){var m={${map}};var l=(navigator.language||"en").toLowerCase().split("-")[0];
    var t=m[l]||"${xd.code}";location.replace("./"+t+"/");})();
  </script>
</head>
<body>
  <h1>Sepehr Fathi</h1>
  <p>Deep-tech founder &amp; senior software engineer</p>
  <div>${links}</div>
</body>
</html>
`;
}

/* ------------------------------ FAVICON --------------------------------- */
const FAVICON = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0fb3a1"/><stop offset="1" stop-color="#0a7c6f"/></linearGradient></defs>
  <rect width="64" height="64" rx="15" fill="url(#g)"/>
  <path d="M40.5 21.5c-2.1-1.8-5-2.8-8.4-2.8-6 0-9.7 2.9-9.7 7.4 0 4 2.7 6 8 7.2l3.1.7c3 .7 4 1.5 4 3 0 1.8-1.8 2.9-4.8 2.9-3 0-5.3-1-7.2-2.9"
    fill="none" stroke="#fff" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`;

/* --------------------------- SITEMAP / ROBOTS --------------------------- */
function renderSitemap(pages) {
  const urls = pages.map((p) => {
    const alts = pages.map((q) => `    <xhtml:link rel="alternate" hreflang="${q.hreflang}" href="${url(q.code)}"/>`).join("\n");
    const xd = pages.find((x) => x.default) || pages[0];
    return `  <url>
    <loc>${url(p.code)}</loc>
${alts}
    <xhtml:link rel="alternate" hreflang="x-default" href="${url(xd.code)}"/>
    <changefreq>monthly</changefreq>
    <priority>${p.default ? "1.0" : "0.8"}</priority>
  </url>`;
  }).join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urls}
</urlset>
`;
}

const ROBOTS = `User-agent: *
Allow: /

Sitemap: ${BASE_URL}/sitemap.xml
`;

function renderManifest(pages) {
  const xd = pages.find((p) => p.default) || pages[0];
  return JSON.stringify({
    name: "Sepehr Fathi",
    short_name: "Sepehr Fathi",
    description: "Deep-tech founder & senior software engineer.",
    start_url: `/${xd.code}/`,
    scope: "/",
    display: "standalone",
    background_color: "#fcfcfb",
    theme_color: "#0a7c6f",
    lang: xd.htmlLang,
    icons: [
      { src: "/favicon.png", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/apple-touch-icon.png", sizes: "180x180", type: "image/png", purpose: "any" },
    ],
  }, null, 2);
}

/* ------------------------------- RUN ------------------------------------ */
const present = LANGS.filter((L) => existsSync(join(ROOT, "content", `${L.code}.json`)));
if (!present.length) { console.error("No content/*.json found."); process.exit(1); }

let built = [];
for (const L of present) {
  const c = JSON.parse(readFileSync(join(ROOT, "content", `${L.code}.json`), "utf8"));
  const dir = join(ROOT, L.code);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "index.html"), renderPage(L, c, present));
  built.push(L.code);
}
writeFileSync(join(ROOT, "index.html"), renderRoot(present));
writeFileSync(join(ROOT, "sitemap.xml"), renderSitemap(present));
writeFileSync(join(ROOT, "robots.txt"), ROBOTS);
writeFileSync(join(ROOT, "manifest.webmanifest"), renderManifest(present));

console.log(`✔ Built ${built.length} language page(s): ${built.join(", ")}`);
console.log(`✔ Wrote index.html, sitemap.xml, robots.txt, manifest.webmanifest`);
console.log(`  Base URL: ${BASE_URL}  (edit BASE_URL in build.mjs to your real domain)`);
