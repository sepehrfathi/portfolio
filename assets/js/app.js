/* Sepehr Fathi portfolio — behavior. Vanilla, dependency-free, offline-safe. */
(function () {
  "use strict";
  var root = document.documentElement;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---- Theme (persisted, with system default) ---- */
  var THEME_KEY = "am-theme";
  function systemDark() { return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches; }
  function applyTheme(t) {
    if (t === "light" || t === "dark") root.setAttribute("data-theme", t);
    else root.removeAttribute("data-theme");
    var isDark = t === "dark" || (t !== "light" && systemDark());
    var meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", isDark ? "#080a0d" : "#fcfcfd");
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

  /* ---- Portfolio deck: 4 visible slots cycling through the full project list ----
     One slot at a time fades out, swaps its content, fades back in — so the grid
     never reflows and only one card moves per tick. */
  var deck = $("[data-deck]");
  if (deck && !reducedMotion) {
    var items = [];
    try { items = JSON.parse(deck.getAttribute("data-deck")); } catch (e) { items = []; }
    var slots = $$(".shot", deck);
    if (items.length > slots.length) {
      var next = slots.length;   // first project not currently on screen
      var slot = 0;              // slot to replace on the next tick
      var paused = false;
      deck.addEventListener("mouseenter", function () { paused = true; });
      deck.addEventListener("mouseleave", function () { paused = false; });

      var base = "../assets/images/portfolio/";
      var fill = function (el, it) {
        var imgs = $$("img", el);
        if (imgs[0]) { imgs[0].src = base + it.d; imgs[0].alt = it.t; }
        if (imgs[1]) { imgs[1].src = base + it.m; imgs[1].alt = it.t; }
        var b = $("figcaption b", el); if (b) b.textContent = it.t;
        var g = $("figcaption .tag", el); if (g) g.textContent = it.g;
        el.setAttribute("href", it.u || "#");
      };

      // Decode the next pair up front. Swapping to an undecoded <img> is what
      // made the change read as a jump: the card faded back in on a blank box.
      var preload = function (it) {
        return Promise.all([it.d, it.m].map(function (f) {
          return new Promise(function (done) {
            var img = new Image();
            img.onload = img.onerror = done;
            img.src = base + f;
          });
        }));
      };

      var FADE = 900;   // matches the .shot opacity transition
      var swap = function () {
        if (paused || document.hidden) return;
        var el = slots[slot];
        var it = items[next];
        next = (next + 1) % items.length;
        slot = (slot + 1) % slots.length;
        preload(it).then(function () {
          el.classList.add("is-out");
          setTimeout(function () {
            fill(el, it);
            // let the new content paint while still transparent, then fade in
            requestAnimationFrame(function () {
              requestAnimationFrame(function () { el.classList.remove("is-out"); });
            });
          }, FADE);
        });
      };
      setInterval(swap, 6000);
    }
  }

  /* ---- Contact form ----
     Posts to contact.php, which mails the message. If PHP is not there (local
     preview, or a host without it) we fall back to composing a mailto: so the
     message is never simply lost. */
  var cform = $("[data-cform]");
  if (cform) {
    var note = $(".cform__note", cform);
    var submitBtn = $("button[type=submit]", cform);
    var say = function (text, isErr) {
      note.textContent = text;
      note.classList.toggle("is-err", !!isErr);
    };
    var mailtoFallback = function (name, from, msg) {
      var subject = (cform.getAttribute("data-subject") || "Message") + " — " + name;
      var body = msg + "\n\n—\n" + name + "\n" + from;
      window.location.href = "mailto:" + cform.getAttribute("data-to") +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
    };

    cform.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = (cform.elements.name.value || "").trim();
      var from = (cform.elements.email.value || "").trim();
      var msg = (cform.elements.message.value || "").trim();
      if (!name || !from || !msg) {
        say(cform.getAttribute("data-msg-required") || "Please fill in every field.", true);
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(from)) {
        say(cform.getAttribute("data-msg-email") || "Please check your email address.", true);
        return;
      }

      var endpoint = cform.getAttribute("data-endpoint");
      if (!endpoint || !window.fetch) { mailtoFallback(name, from, msg); return; }

      submitBtn.disabled = true;
      say(cform.getAttribute("data-msg-sending") || "Sending…");

      var data = new FormData(cform);
      fetch(endpoint, { method: "POST", body: data })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (res) {
          submitBtn.disabled = false;
          if (res && res.ok) {
            cform.reset();
            say(cform.getAttribute("data-msg-sent") || "Sent — thank you.");
            return;
          }
          if (res && res.error === "rate_limited") {
            say(cform.getAttribute("data-msg-rate") || "Too many messages. Try again later.", true);
            return;
          }
          mailtoFallback(name, from, msg);
        })
        .catch(function () {
          submitBtn.disabled = false;
          mailtoFallback(name, from, msg);
        });
    });
  }

  /* ---- Count-up stats ----
     Digits are localised (Persian, Arabic-Indic, Latin), so the animation
     rewrites only the digit run and keeps the +/%/... decoration around it. */
  var DIGITS = { fa: "۰۱۲۳۴۵۶۷۸۹", ar: "٠١٢٣٤٥٦٧٨٩", en: "0123456789" };
  function digitSet(text) {
    for (var k in DIGITS) {
      for (var i = 0; i < 10; i++) {
        if (text.indexOf(DIGITS[k][i]) !== -1) return DIGITS[k];
      }
    }
    return DIGITS.en;
  }
  function localise(n, set) {
    return String(n).replace(/[0-9]/g, function (d) { return set[+d]; });
  }
  var counters = $$("[data-count]");
  if (counters.length) {
    counters.forEach(function (el) {
      var raw = el.textContent;
      var set = digitSet(raw);
      var map = {};
      for (var i = 0; i < 10; i++) map[set[i]] = i;
      var run = raw.replace(/[^0-9۰-۹٠-٩]/g, "");
      var target = 0;
      for (var j = 0; j < run.length; j++) target = target * 10 + (map[run[j]] || 0);
      if (!target) return;                       // nothing numeric to animate
      el.setAttribute("data-target", String(target));
      el.setAttribute("data-tpl", raw.replace(run, "\u0000"));
      el.setAttribute("data-set", set);
      el.textContent = raw.replace(run, localise(0, set));
    });

    var runCount = function (el) {
      if (el.dataset.done) return;
      el.dataset.done = "1";
      var target = +el.getAttribute("data-target");
      var tpl = el.getAttribute("data-tpl");
      var set = el.getAttribute("data-set");
      if (reducedMotion) { el.textContent = tpl.replace("\u0000", localise(target, set)); return; }
      var dur = 1400, t0 = 0;
      var step = function (now) {
        if (!t0) t0 = now;
        var p = Math.min((now - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);      // ease-out, settles on the number
        el.textContent = tpl.replace("\u0000", localise(Math.round(target * eased), set));
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };

    if ("IntersectionObserver" in window) {
      var cObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { runCount(en.target); cObs.unobserve(en.target); }
        });
      }, { threshold: 0.4 });
      counters.forEach(function (el) { cObs.observe(el); });
    } else {
      counters.forEach(runCount);
    }
  }

  /* ---- Timeline: reveal one entry at a time on scroll ---- */
  var tlItems = $$(".tl__item");
  if (tlItems.length && "IntersectionObserver" in window && !reducedMotion) {
    var tObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in-view");
        tObs.unobserve(en.target);
      });
    }, { threshold: 0.25, rootMargin: "0px 0px -8% 0px" });
    tlItems.forEach(function (el) { tObs.observe(el); });
  } else {
    tlItems.forEach(function (el) { el.classList.add("in-view"); });
  }

  /* ---- Year ---- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
