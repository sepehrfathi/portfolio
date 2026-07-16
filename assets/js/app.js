/* Sepehr Fathi portfolio — behavior. Vanilla, dependency-free, offline-safe. */
(function () {
  "use strict";
  var root = document.documentElement;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---- Theme (persisted, with system default) ---- */
  var THEME_KEY = "sf-theme";
  function systemDark() { return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches; }
  function applyTheme(t) {
    if (t === "light" || t === "dark") root.setAttribute("data-theme", t);
    else root.removeAttribute("data-theme");
    var isDark = t === "dark" || (t !== "light" && systemDark());
    var meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", isDark ? "#080a0a" : "#fcfcfb");
    $$("[data-theme-btn]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(isDark));
    });
  }
  var stored;
  try { stored = localStorage.getItem(THEME_KEY); } catch (e) {}
  applyTheme(stored || "system");
  $$("[data-theme-btn]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var current = root.getAttribute("data-theme");
      var next = (current === "dark") ? "light" : (current === "light" ? "dark" : (systemDark() ? "light" : "dark"));
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      applyTheme(next);
    });
  });

  /* ---- Sticky header shadow ---- */
  var header = $(".header");
  function onScroll() { if (header) header.classList.toggle("is-scrolled", window.scrollY > 8); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---- Language menu ---- */
  var langWrap = $("[data-lang-wrap]");
  if (langWrap) {
    var langBtn = $("[data-lang-btn]", langWrap);
    var langMenu = $("[data-lang-menu]", langWrap);
    var closeLang = function () { langMenu.classList.remove("open"); langBtn.setAttribute("aria-expanded", "false"); };
    langBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = langMenu.classList.toggle("open");
      langBtn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (e) { if (!langWrap.contains(e.target)) closeLang(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeLang(); });
  }

  /* ---- Mobile nav ---- */
  var mnav = $("[data-mobile-nav]");
  var openBtn = $("[data-menu-open]");
  var closeBtn = $("[data-menu-close]");
  function setNav(open) {
    if (!mnav) return;
    mnav.classList.toggle("open", open);
    document.body.style.overflow = open ? "hidden" : "";
    if (openBtn) openBtn.setAttribute("aria-expanded", String(open));
  }
  if (openBtn) openBtn.addEventListener("click", function () { setNav(true); });
  if (closeBtn) closeBtn.addEventListener("click", function () { setNav(false); });
  if (mnav) $$("a.mlink", mnav).forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setNav(false); });

  /* ---- Résumé / print ---- */
  $$("[data-print]").forEach(function (b) {
    b.addEventListener("click", function (e) { e.preventDefault(); setNav(false); window.print(); });
  });

  /* ---- Copy email ---- */
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var val = b.getAttribute("data-copy");
      var done = function () {
        var label = $(".copy-label", b);
        var old = label ? label.textContent : "";
        if (label) { label.textContent = b.getAttribute("data-copied") || "Copied"; setTimeout(function () { label.textContent = old; }, 1600); }
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(val).then(done, done);
      else {
        var t = document.createElement("textarea"); t.value = val; document.body.appendChild(t); t.select();
        try { document.execCommand("copy"); } catch (e) {} document.body.removeChild(t); done();
      }
    });
  });

  /* ---- Reveal on scroll (scroll-based = robust; can never leave content hidden) ---- */
  var reveals = $$(".reveal");
  var revealAll = function () { reveals.forEach(function (el) { el.classList.add("in"); }); reveals = []; };
  var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reducedMotion) {
    revealAll();
  } else {
    var revealCheck = function () {
      var vh = window.innerHeight || document.documentElement.clientHeight;
      for (var i = reveals.length - 1; i >= 0; i--) {
        var r = reveals[i].getBoundingClientRect();
        if (r.top < vh * 0.92 && r.bottom > -40) { reveals[i].classList.add("in"); reveals.splice(i, 1); }
      }
    };
    var ticking = false;
    var onRevealScroll = function () {
      if (ticking) return; ticking = true;
      window.requestAnimationFrame(function () { revealCheck(); ticking = false; });
    };
    revealCheck();
    window.addEventListener("scroll", onRevealScroll, { passive: true });
    window.addEventListener("resize", onRevealScroll, { passive: true });
    window.addEventListener("load", revealCheck);
    setTimeout(revealCheck, 250);
    // Safety net: never let content stay invisible.
    setTimeout(revealAll, 4000);
  }

  /* ---- Scroll-spy for header nav + mobile dock ---- */
  var spyLinks = $$(".nav a[href^='#'], .dock a[href^='#']");
  var spyIds = {};
  spyLinks.forEach(function (a) { var id = a.getAttribute("href").slice(1); if (id) spyIds[id] = true; });
  var sections = Object.keys(spyIds).map(function (id) { return document.getElementById(id); }).filter(Boolean);
  if ("IntersectionObserver" in window && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var id = en.target.id;
          spyLinks.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + id); });
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---- Year ---- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
