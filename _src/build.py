# -*- coding: utf-8 -*-
"""Render every locale of the portfolio from content.py."""
import json
import os
import time
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import (L, LOCALES, SITE, EMAIL, GITHUB, LINKEDIN, TELEGRAM, INSTAGRAM,  # noqa
                     GALLERY, NAME_VARIANTS, ONWEBS, AVANOBAT, CUATRO)

ASSET_V = "16"
LASTMOD = time.strftime("%Y-%m-%d")   # bump when css/js change so hosts and browsers refetch
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
SJ = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"'
F = 'viewBox="0 0 24 24" fill="currentColor" stroke="none"'

IC = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "pin": '<svg %s><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>' % S,
    "sun": '<svg %s><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>' % S,
    "moon": '<svg %s><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>' % S,
    "globe": '<svg %s><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3Z"/></svg>' % S,
    "mail": '<svg %s><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></svg>' % S,
    "copy": '<svg %s><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M6 15H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v1"/></svg>' % S,
    "grid": '<svg %s><rect x="3" y="3" width="7.5" height="7.5" rx="1.6"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.6"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.6"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.6"/></svg>' % SJ,
    "search": '<svg %s><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>' % S,
    "user": '<svg %s><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.2 3.6-6.5 8-6.5s8 2.3 8 6.5"/></svg>' % S,
    "case": '<svg %s><rect x="3" y="7.5" width="18" height="12.5" rx="2.5"/><path d="M8 7.5V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1.5M3 12h18"/></svg>' % S,
    "cap": '<svg %s><path d="m12 4 10 4.6-10 4.6L2 8.6 12 4Z"/><path d="M6.5 10.8V15c0 1.8 2.5 3.2 5.5 3.2s5.5-1.4 5.5-3.2v-4.2"/></svg>' % S,
    "lock": '<svg %s><rect x="4.5" y="10" width="15" height="10" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>' % S,
    "star": '<svg %s><path d="m12 2 2.6 6.3L21 9l-5 4.3L17.5 20 12 16.3 6.5 20 8 13.3 3 9l6.4-.7L12 2Z"/></svg>' % F,
    "quote": '<svg %s><path d="M7 7h5v6a4 4 0 0 1-4 4H7v-2h1a2 2 0 0 0 2-2v-1H7V7Zm8 0h5v6a4 4 0 0 1-4 4h-1v-2h1a2 2 0 0 0 2-2v-1h-3V7Z"/></svg>' % F,
    "github": '<svg %s><path d="M12 2C6.48 2 2 6.58 2 12.25c0 4.53 2.87 8.37 6.85 9.73.5.1.68-.22.68-.49l-.01-1.7c-2.79.62-3.38-1.22-3.38-1.22-.45-1.18-1.11-1.5-1.11-1.5-.91-.64.07-.62.07-.62 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.36 1.12 2.94.85.09-.66.35-1.12.63-1.38-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.71 0 0 .84-.28 2.75 1.05a9.4 9.4 0 0 1 5 0c1.91-1.33 2.75-1.05 2.75-1.05.55 1.41.2 2.45.1 2.71.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.81-4.57 5.06.36.32.68.94.68 1.9l-.01 2.82c0 .27.18.59.69.49A10.26 10.26 0 0 0 22 12.25C22 6.58 17.52 2 12 2Z"/></svg>' % F,
    "linkedin": '<svg %s><path d="M6.94 5a1.94 1.94 0 1 1-3.88 0 1.94 1.94 0 0 1 3.88 0ZM3.4 8.4h3.1V21H3.4V8.4Zm5.2 0h2.97v1.72h.04c.41-.78 1.42-1.6 2.93-1.6 3.13 0 3.71 2.06 3.71 4.74V21h-3.1v-5.58c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94V21H8.6V8.4Z"/></svg>' % F,
    "telegram": '<svg %s><path d="M21.9 4.6 18.6 20c-.24 1.08-.9 1.34-1.82.83l-5-3.68-2.42 2.33c-.27.27-.5.5-1 .5l.35-5.06L18.1 6.1c.4-.36-.09-.56-.62-.2L5.9 13.28.86 11.7c-1.1-.34-1.12-1.1.23-1.63L20.5 3.03c.9-.34 1.7.2 1.4 1.57Z"/></svg>' % F,
    "instagram": '<svg %s><path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.2.05 1.8.25 2.2.42.6.22 1 .48 1.4.9.43.42.7.83.92 1.4.17.44.37 1.05.42 2.25.06 1.28.07 1.66.07 4.9s0 3.6-.07 4.9c-.05 1.2-.25 1.8-.42 2.2a3.9 3.9 0 0 1-.92 1.4c-.42.43-.83.7-1.4.92-.44.17-1.05.37-2.25.42-1.28.06-1.66.07-4.9.07s-3.6 0-4.9-.07c-1.2-.05-1.8-.25-2.2-.42a3.9 3.9 0 0 1-1.4-.92 3.9 3.9 0 0 1-.92-1.4c-.17-.44-.37-1.05-.42-2.25C2.21 15.6 2.2 15.2 2.2 12s0-3.6.07-4.9c.05-1.2.25-1.8.42-2.2a3.9 3.9 0 0 1 .92-1.4c.42-.43.83-.7 1.4-.92.44-.17 1.05-.37 2.25-.42C8.4 2.21 8.8 2.2 12 2.2Zm0 1.8c-3.17 0-3.5.01-4.74.07-.92.04-1.41.2-1.74.32-.44.17-.75.37-1.08.7-.33.33-.53.64-.7 1.08-.13.33-.28.82-.32 1.74C3.4 8.5 3.4 8.83 3.4 12s.01 3.5.07 4.74c.4.92.2 1.41.32 1.74.17.44.37.75.7 1.08.33.33.64.53 1.08.7.33.13.82.28 1.74.32 1.24.06 1.57.07 4.74.07s3.5-.01 4.74-.07c.92-.04 1.41-.2 1.74-.32.44-.17.75-.37 1.08-.7.33-.33.53-.64.7-1.08.13-.33.28-.82.32-1.74.06-1.24.07-1.57.07-4.74s-.01-3.5-.07-4.74c-.04-.92-.2-1.41-.32-1.74a2.9 2.9 0 0 0-.7-1.08 2.9 2.9 0 0 0-1.08-.7c-.33-.13-.82-.28-1.74-.32C15.5 4.01 15.17 4 12 4Zm0 3.03a4.97 4.97 0 1 1 0 9.94 4.97 4.97 0 0 1 0-9.94Zm0 1.8a3.17 3.17 0 1 0 0 6.34 3.17 3.17 0 0 0 0-6.34Zm5.17-3.2a1.16 1.16 0 1 1 0 2.32 1.16 1.16 0 0 1 0-2.32Z"/></svg>' % F,
}


# Tech orbs in the About column. Positions/sizes are % of a square field and
# were picked by hand so the shapes never collide while still reading as a
# random scatter; each floats on its own cycle. orbs3d.js turns these into
# faceted 3D icosahedrons with the same logo decals.
# file, x, y, size, float duration, delay, drift-x, drift-y
ORBS = [
    ("reactjs",    "4%",  "16%", "30%", "9.5s",  "0s",    "5px",  "-15px"),
    ("typescript", "41%", "2%",  "22%", "11s",   "-2.4s", "-6px", "-11px"),
    ("javascript", "70%", "19%", "26%", "8.6s",  "-1.1s", "4px",  "-16px"),
    ("figma",      "48%", "37%", "18%", "12s",   "-3.6s", "-5px", "-9px"),
    ("tailwind",   "16%", "55%", "24%", "10.2s", "-0.7s", "6px",  "-13px"),
    ("html",       "74%", "56%", "20%", "9s",    "-2.9s", "-4px", "-12px"),
    ("git",        "43%", "72%", "23%", "11.6s", "-1.8s", "5px",  "-10px"),
    ("css",        "5%",  "82%", "17%", "8.2s",  "-4.2s", "-5px", "-14px"),
]


SKILL_ICONS = [
    '<svg %s><path d="M12 3.5 4 7.6v8.8L12 20.5l8-4.1V7.6L12 3.5Z"/><path d="M12 12v8.5M4 7.6l8 4.4 8-4.4"/></svg>' % S,
    '<svg %s><path d="m9 8-5 4 5 4M15 8l5 4-5 4M13.5 5l-3 14"/></svg>' % S,
    '<svg %s><ellipse cx="12" cy="6" rx="7.5" ry="3"/><path d="M4.5 6v6c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6M4.5 12v6c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3v-6"/></svg>' % S,
    '<svg %s><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>' % S,
    '<svg %s><path d="M12 3v3.5M12 17.5V21M3 12h3.5M17.5 12H21M6 6l2.4 2.4M15.6 15.6 18 18M18 6l-2.4 2.4M8.4 15.6 6 18"/><circle cx="12" cy="12" r="3"/></svg>' % S,
    '<svg %s><path d="M12 21a8 8 0 1 0-8-8"/><path d="m12 12 4.5-3.5M4 13H2M12 5V3"/></svg>' % S,
    '<svg %s><path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-.9 2-1.8 0-1.5-1.3-1.7-1.3-2.9 0-.9.7-1.5 1.7-1.5H16a5 5 0 0 0 5-5c0-3.7-4-6.8-9-6.8Z"/><circle cx="8.5" cy="10" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="15.5" cy="10" r="1"/></svg>' % S,
    '<svg %s><circle cx="9" cy="8.5" r="3.2"/><path d="M2.5 20c0-3.3 2.9-5.2 6.5-5.2s6.5 1.9 6.5 5.2"/><path d="M16.5 6.2a3 3 0 0 1 0 5.6M18 20c0-2.4-.9-4-2.4-4.9"/></svg>' % S,
]


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def socials(cls):
    return (
        '<div class="%s">'
        '<a href="%s" target="_blank" rel="noopener" aria-label="GitHub">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="LinkedIn">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Telegram">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Instagram">%s</a>'
        "</div>"
    ) % (cls, GITHUB, IC["github"], LINKEDIN, IC["linkedin"], TELEGRAM, IC["telegram"], INSTAGRAM, IC["instagram"])


def render(code, hreflang, d):
    dirn = d["dir"]
    u = d["ui"]
    nav = d["nav"]
    url = "%s/%s/" % (SITE, code)

    alts = "\n  ".join(
        '<link rel="alternate" hreflang="%s" href="%s/%s/" />' % (hl, SITE, c)
        for c, hl, _ in LOCALES
    )
    alts += '\n  <link rel="alternate" hreflang="x-default" href="%s/fa/" />' % SITE

    langmenu = "".join(
        '<a href="../%s/" hreflang="%s"%s>%s<span>%s</span></a>'
        % (c, hl, ' aria-current="true"' if c == code else "", lbl, hl)
        for c, hl, lbl in LOCALES
    )

    # ---- structured data ----
    # A @graph rather than a lone Person: search and generative engines resolve
    # the entity far more reliably when the person, the site, the page and an
    # answer-first FAQ all cross-reference each other by @id.
    person_id = SITE + "/#person"
    site_id = SITE + "/#website"
    person = {
        "@type": "Person",
        "@id": person_id,
        "name": d["name"],
        "alternateName": NAME_VARIANTS,
        "givenName": "Amir Hossein",
        "familyName": "Moghtader",
        "jobTitle": d["tagline"].replace(" · ", ", "),
        "description": d["desc"],
        "url": SITE + "/",
        "mainEntityOfPage": url,
        "image": {"@type": "ImageObject", "url": SITE + "/assets/images/og-cover.jpg",
                  "width": 1200, "height": 630},
        "email": "mailto:" + EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Mashhad",
                    "addressRegion": "Razavi Khorasan", "addressCountry": "IR"},
        "nationality": {"@type": "Country", "name": "Iran"},
        "knowsLanguage": ["fa", "en"],
        "sameAs": [GITHUB, LINKEDIN, TELEGRAM, INSTAGRAM, ONWEBS, AVANOBAT],
        "knowsAbout": [
            "Web Development", "Front-end Development", "UI/UX Design",
            "Next.js", "React", "TypeScript", "JavaScript", "Tailwind CSS", "PHP", "MySQL",
            "Search Engine Optimization", "Technical SEO", "Local SEO",
            "Generative Engine Optimization", "Core Web Vitals", "Schema.org structured data",
        ],
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": "Shahid Rajaee University, Mashhad"},
            {"@type": "CollegeOrUniversity", "name": "Azad University — Mechatronics (M.Sc.)"},
            {"@type": "HighSchool", "name": "Shahid Hasheminejad High School (NODET), Mashhad"},
        ],
        "worksFor": [
            {"@type": "Organization", "name": "Onwebs — Vira Web Aria", "url": ONWEBS},
            {"@type": "Organization", "name": "Cuatro Group (4cuatro)", "url": CUATRO},
        ],
        "founder": [
            {"@type": "Organization", "name": "Onwebs — Vira Web Aria", "url": ONWEBS},
            {"@type": "Organization", "name": "Avanobat", "url": AVANOBAT},
        ],
    }
    graph = [
        person,
        {"@type": "WebSite", "@id": site_id, "url": SITE + "/", "name": d["name"],
         "inLanguage": hreflang, "publisher": {"@id": person_id},
         "about": {"@id": person_id}},
        {"@type": "ProfilePage", "@id": url + "#page", "url": url, "name": d["title"],
         "description": d["desc"], "inLanguage": hreflang,
         "isPartOf": {"@id": site_id}, "mainEntity": {"@id": person_id},
         "primaryImageOfPage": {"@type": "ImageObject",
                                "url": SITE + "/assets/images/og-cover.jpg"}},
        {"@type": "FAQPage", "@id": url + "#faq",
         "inLanguage": hreflang, "isPartOf": {"@id": url + "#page"},
         "mainEntity": [
             {"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": a}}
             for q, a in d["faq"]
         ]},
    ]
    ld = {"@context": "https://schema.org", "@graph": graph}

    # ---- header ----
    brand = (
        '<a href="#top" class="brand" aria-label="%s">'
        '<span class="brand__mark" aria-hidden="true"></span>'
        '<span>%s<small>%s</small></span></a>'
    ) % (esc(d["name"]), esc(d["short"]), esc(d["brandline"]))

    navlinks = "".join(
        '<a href="#%s">%s</a>' % (k, esc(nav[k]))
        for k in ("about", "roles", "ventures", "geo", "skills", "work", "contact")
    )

    # ---- stats ----
    stats = "".join(
        '<div class="stat reveal"><div class="stat__num" data-count>%s</div>'
        '<div class="stat__label">%s</div></div>'
        % (n, esc(l)) for n, l in d["stats"]
    )

    # A role's detail paragraph doubles as the timeline bullets: the copy is
    # already written as discrete clauses, so split on sentence enders.
    def bullets(text):
        out, buf = [], ""
        for i, ch in enumerate(text):
            buf += ch
            nxt = text[i + 1] if i + 1 < len(text) else ""
            # "." only ends a sentence when whitespace or the end follows —
            # otherwise it is something like "Next.js" or "4.5".
            if ch in "؛。!؟?" or (ch == "." and nxt in ("", " ")):
                t = buf.strip()
                if len(t) > 2:
                    out.append(t)
                buf = ""
        t = buf.strip()
        if len(t) > 2:
            out.append(t)
        return out or [text]

    # ---- experience timeline ----
    meta = d.get("role_meta") or []
    tl = []
    for i, (badge, org, role, detail, loc) in enumerate(d["roles"]):
        logo, date = (meta[i] if i < len(meta) else ("onwebs", ""))
        pts = "".join("<li>%s</li>" % esc(b) for b in bullets(detail))
        tl.append(
            '\n        <article class="tl__item reveal">\n'
            '          <div class="tl__date">%s</div>\n'
            '          <span class="tl__badge" aria-hidden="true">'
            '<img src="../assets/images/brands/%s.png" alt="" width="256" height="256" loading="lazy" decoding="async" /></span>\n'
            '          <div class="tl__card">\n'
            '            <h3 class="tl__role">%s</h3>\n'
            '            <div class="tl__org">%s</div>\n'
            '            <ul class="tl__points">%s</ul>\n'
            '            <span class="tl__loc">%s%s</span>\n'
            '          </div>\n'
            '        </article>' % (esc(date), logo, esc(badge), esc(org), pts, IC["pin"], esc(loc))
        )
    timeline = "".join(tl)

    # ---- role / education cards ----
    def rolecards(items):
        out = []
        for badge, org, role, detail, loc in items:
            out.append(
                '\n      <article class="role reveal">\n'
                '        <div><span class="role__badge">%s</span></div>\n'
                '        <div class="role__main">\n'
                '          <h3 class="role__org">%s</h3>\n'
                '          <div class="role__role">%s</div>\n'
                '          <p class="role__detail">%s</p>\n'
                '          <span class="role__loc">%s%s</span>\n'
                '        </div>\n'
                '      </article>' % (esc(badge), esc(org), esc(role), esc(detail), IC["pin"], esc(loc))
            )
        return "".join(out)

    # ---- ventures ----
    vents = []
    for v in d["ventures"]:
        pts = "".join("<li>%s</li>" % esc(p) for p in v["p"])
        tags = "".join('<span class="tag">%s</span>' % esc(t) for t in v["t"])
        vents.append(
            '\n      <article class="venture reveal%s">\n'
            '        <div class="venture__head">\n'
            '          <h3 class="venture__name">%s</h3>\n'
            '          <span class="venture__kicker">%s</span>\n'
            '        </div>\n'
            '        <p class="venture__summary">%s</p>\n'
            '        <ul class="venture__points">%s</ul>\n'
            '        <div class="venture__foot">\n'
            '          <div class="venture__stack">%s</div>\n'
            '          <div class="venture__metric"><b>%s</b><span>%s</span></div>\n'
            '        </div>\n'
            '      </article>'
            % (" venture--wide" if v["wide"] else "", esc(v["n"]), esc(v["k"]),
               esc(v["s"]), pts, tags, esc(v["mb"]), esc(v["ms"]))
        )

    # ---- gallery ----
    deck = [{"d": stem + ".webp", "m": stem + "-m.webp", "t": t, "g": g, "u": u}
            for (stem, u), (t, g) in zip(GALLERY, d["gal_items"])]
    shots = "".join(
        '<a class="shot reveal" href="%s"%s>\n'
        '        <div class="shot__img">'
        '<img loading="%s" decoding="async" src="../assets/images/portfolio/%s" alt="%s" width="1000" height="625" />'
        '</div>\n'
        '        <div class="shot__mobile" aria-hidden="true">'
        '<img loading="lazy" decoding="async" src="../assets/images/portfolio/%s" alt="" width="650" height="1445" />'
        '</div>\n'
        '        <figcaption><b>%s</b><span class="tag">%s</span></figcaption>\n'
        '      </a>' % (
            it["u"] or "#",
            ' target="_blank" rel="noopener"' if it["u"] else "",
            "eager" if i < 2 else "lazy",
            it["d"], esc(it["t"]), it["m"], esc(it["t"]), esc(it["g"]))
        for i, it in enumerate(deck[:4])
    )
    deck_json = esc(json.dumps(deck, ensure_ascii=False)).replace('"', "&quot;")

    # ---- GEO cards ----
    geocards = "".join(
        '\n        <div class="pf-card reveal">\n'
        '          <span class="pf-card__n">%02d</span>\n'
        '          <h4>%s</h4>\n'
        '          <p>%s</p>\n'
        '        </div>' % (i + 1, esc(h), esc(p))
        for i, (h, p) in enumerate(d["geo_cards"])
    )

    # ---- skills ----
    sk = []
    for i, (title, items) in enumerate(d["skills"]):
        lis = "".join("<li>%s</li>" % esc(x) for x in items)
        icon = SKILL_ICONS[i] if i < len(SKILL_ICONS) else SKILL_ICONS[-1]
        if i == 0:
            sk.append(
                '\n      <div class="skillgroup skillgroup--feat reveal">\n'
                '        <h3><span class="gi">%s</span>%s<span class="star">%s</span></h3>\n'
                '        <ul class="skillgroup__items">%s</ul>\n'
                '      </div>' % (icon, esc(title), IC["star"], lis))
        else:
            sk.append(
                '\n      <div class="skillgroup reveal">\n'
                '        <h3><span class="gi">%s</span>%s</h3>\n'
                '        <ul class="skillgroup__items">%s</ul>\n'
                '      </div>' % (icon, esc(title), lis))

    works = "".join(
        '<a class="work__item" href="%s" target="_blank" rel="noopener">'
        '<h4>%s</h4><span class="tag">%s</span></a>' % (u, esc(t), esc(g))
        for t, g, u in d["work"]
    )

    # ---- dock ----
    dock_items = [("about", "user"), ("ventures", "case"), ("geo", "search"),
                  ("skills", "grid"), ("contact", "mail")]
    dock = "".join(
        '<a href="#%s" class="dock__item" aria-label="%s"><span class="dock__ic">%s</span>'
        '<span class="dock__lbl">%s</span></a>' % (k, esc(nav[k]), IC[ic], esc(nav[k]))
        for k, ic in dock_items
    )

    # ---- mobile nav ----
    mnav_keys = ("about", "roles", "edu", "ventures", "geo", "skills", "work", "contact")
    chev = ('<span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>')
    mlinks = "".join('<a class="mlink" href="#%s">%s%s</a>' % (k, esc(nav[k]), chev) for k in mnav_keys)

    # ---- résumé ----
    r = d["r"]
    r_high = "".join("<div><b>%s</b><span>%s</span></div>" % (n, esc(l)) for n, l in d["stats"])
    r_exp = "".join(
        '\n        <div class="r-exp">\n'
        '          <div class="r-exp-h"><span class="r-exp-org">%s</span><span class="r-exp-loc">%s</span></div>\n'
        '          <div class="r-exp-role">%s</div>\n'
        '          <p>%s</p>\n'
        '        </div>' % (esc(org), esc(loc), esc(role), esc(detail))
        for _b, org, role, detail, loc in d["roles"])
    r_edu = "".join(
        '\n        <div class="r-exp">\n'
        '          <div class="r-exp-h"><span class="r-exp-org">%s</span><span class="r-exp-loc">%s</span></div>\n'
        '          <div class="r-exp-role">%s</div>\n'
        '          <p>%s</p>\n'
        '        </div>' % (esc(org), esc(loc), esc(role), esc(detail))
        for _b, org, role, detail, loc in d["edu"])
    r_vent = "".join(
        '\n        <div class="r-vent"><b>%s</b><i>%s</i><p>%s</p></div>'
        % (esc(v["n"]), esc(v["k"]), esc(v["s"])) for v in d["ventures"])
    r_skills = "".join(
        "<div><b>%s:</b> %s</div>" % (esc(t), esc(" · ".join(items))) for t, items in d["skills"])
    r_work = "".join("<span>%s — %s</span>" % (esc(t), esc(g)) for t, g, _u in d["work"])

    html = """<!doctype html>
<html lang="{code}" dir="{dirn}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="color-scheme" content="light dark" />
  <meta name="theme-color" content="#fcfcfb" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="author" content="{name}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta name="geo.region" content="IR-30" />
  <meta name="geo.placename" content="Mashhad" />
  <meta name="geo.position" content="36.2605;59.6168" />
  <meta name="ICBM" content="36.2605, 59.6168" />
  <link rel="canonical" href="{url}" />
  {alts}
  <meta property="og:type" content="profile" />
  <meta property="og:site_name" content="{name}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:locale" content="{og}" />
  <meta property="og:image" content="{site}/assets/images/og-cover.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:type" content="image/jpeg" />
  <meta property="profile:first_name" content="Amir Hossein" />
  <meta property="profile:last_name" content="Moghtader" />
  <meta property="og:image:alt" content="{name}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@Amir_Mg6" />
  <meta name="twitter:creator" content="@Amir_Mg6" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{site}/assets/images/og-cover.jpg" />
  <meta name="twitter:image:alt" content="{name} — {tagline}" />
  <link rel="icon" type="image/png" sizes="512x512" href="../favicon.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png" />
  <link rel="apple-touch-icon" href="../apple-touch-icon.png" />
  <link rel="manifest" href="../manifest.webmanifest" />
  <link rel="preload" as="image" href="../assets/images/amir-moghtader.webp" fetchpriority="high" />
  <link rel="preload" as="font" type="font/ttf" href="../assets/fonts/iransans/IRANSansX-Regular.ttf" crossorigin />
  <link rel="stylesheet" href="../assets/css/styles.css?v={av}" />
  <script type="application/ld+json">{ld}</script>
</head>
<body>
  <header class="header">
    <div class="container header__bar">
      {brand}
      <nav class="nav" aria-label="Primary">{navlinks}</nav>
      <div class="header__actions">
        <button class="icon-btn" data-theme-btn aria-label="{t_theme}" aria-pressed="false">
          <span class="only-dark">{i_sun}</span><span class="only-light">{i_moon}</span>
        </button>
        <div class="menu-wrap" data-lang-wrap>
          <button class="icon-btn" data-lang-btn aria-label="{t_lang}" aria-haspopup="true" aria-expanded="false">{i_globe}</button>
          <div class="menu" data-lang-menu role="menu">{langmenu}</div>
        </div>
        <a href="#" class="btn btn--primary btn--sm" data-print>{i_arrow}{t_resume}</a>
        <button class="icon-btn menu-btn" data-menu-open aria-label="{t_menu}" aria-expanded="false">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
      </div>
    </div>
  </header>

  <div class="mobile-nav" data-mobile-nav>
    <div class="mobile-nav__top">
      <span class="brand"><span class="brand__mark" aria-hidden="true"></span>{short}</span>
      <button class="icon-btn" data-menu-close aria-label="{t_menu}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="m6 6 12 12M18 6 6 18"/></svg>
      </button>
    </div>
    {mlinks}
    <a href="#" class="btn btn--primary" data-print>{i_arrow}{t_resume}</a>
  </div>

  <div class="site">
    <!-- HERO -->
    <section class="hero" id="top">
      <div class="hero__glow" aria-hidden="true"></div>
      <div class="container hero__inner">
        <div class="hero__text">
          <span class="hero__eyebrow reveal">{tagline}</span>
          <h1 class="hero__name reveal">{name}</h1>
          <p class="hero__role reveal">{hero_role}</p>
          <div class="hero__meta reveal"><span>{i_pin}{t_loc}</span></div>
          <div class="hero__cta reveal">
            <a href="#" class="btn btn--primary" data-print>{i_arrow}{t_resume}</a>
            <a href="#contact" class="btn btn--ghost">{t_contact_me}</a>
            <a href="#ventures" class="btn btn--ghost">{t_see_work}</a>
          </div>
          {hero_socials}
        </div>
        <div class="hero__photo reveal">
          <span class="hero__photo-ring" aria-hidden="true"></span>
          <img src="../assets/images/amir-moghtader.webp" alt="{name}" width="473" height="760" loading="eager" decoding="async" fetchpriority="high" />
        </div>
      </div>
    </section>

    <!-- STATS -->
    <section class="container" style="padding-block:0 var(--section-y)">
      <div class="stats">{stats}</div>
    </section>

    <!-- ABOUT -->
    <section class="section" id="about">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{about_eyebrow}</span>
          <h2 class="section-title">{about_title}</h2>
        </div>
        <div class="about__grid">
          <div>
            <p class="about__lead reveal">{about_lead}</p>
            <div class="about__body">{about_body}</div>
          </div>
          <div class="reveal">
            <div class="orbs" data-orbs aria-hidden="true">{orbs}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ROLES -->
    <section class="section" id="roles">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{roles_eyebrow}</span>
          <h2 class="section-title">{roles_title}</h2>
          <p class="section-sub">{roles_sub}</p>
        </div>
        <div class="tl">{timeline}</div>
      </div>
    </section>

    <!-- EDUCATION -->
    <section class="section" id="edu">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{i_cap}{edu_eyebrow}</span>
          <h2 class="section-title">{edu_title}</h2>
          <p class="section-sub">{edu_sub}</p>
        </div>
        <div class="roles__list">{edu}</div>
      </div>
    </section>

    <!-- VENTURES -->
    <section class="section" id="ventures">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{ven_eyebrow}</span>
          <h2 class="section-title">{ven_title}</h2>
          <p class="section-sub">{ven_sub}</p>
        </div>
        <div class="ventures__grid">{ventures}</div>
      </div>
    </section>

    <!-- PORTFOLIO GALLERY -->
    <section class="section gallery" id="portfolio">
      <div class="container">
        <div class="section-head reveal" style="margin-inline:auto">
          <span class="eyebrow">{i_grid}{gal_eyebrow}</span>
          <h2 class="section-title">{gal_title}</h2>
          <p class="section-sub">{gal_sub}</p>
        </div>
        <div class="gallery__grid" data-deck="{deck_json}">{shots}</div>
      </div>
    </section>

    <!-- SEO & GEO -->
    <section class="section" id="geo">
      <div class="container">
        <div class="promptfx reveal">
          <span class="eyebrow">{i_search}{geo_eyebrow}</span>
          <h2 class="section-title">{geo_title}</h2>
          <p class="promptfx__lead">{geo_lead}</p>
          <div class="promptfx__grid">{geo_cards}</div>
        </div>
      </div>
    </section>

    <!-- SKILLS -->
    <section class="section" id="skills">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{skills_eyebrow}</span>
          <h2 class="section-title">{skills_title}</h2>
          <p class="section-sub">{skills_sub}</p>
        </div>
        <div class="skills__grid">{skills}</div>
      </div>
    </section>

    <!-- MORE PROJECTS -->
    <section class="section" id="work">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{work_eyebrow}</span>
          <h2 class="section-title">{work_title}</h2>
          <p class="section-sub">{work_sub}</p>
        </div>
        <div class="work__list">{works}</div>
        <p class="work__note">{i_lock}{work_note}</p>
      </div>
    </section>

    <!-- FAQ (answer-first, mirrors the FAQPage schema) -->
    <section class="section faq" id="faq">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{faq_eyebrow}</span>
          <h2 class="section-title">{faq_title}</h2>
        </div>
        <div class="faq__list">{faq_items}</div>
      </div>
    </section>

    <!-- CONTACT -->
    <section class="section contact" id="contact">
      <div class="container">
        <div class="contact__card reveal">
          <span class="eyebrow" style="justify-content:center">{contact_eyebrow}</span>
          <h2 class="contact__title">{contact_title}</h2>
          <p class="contact__lead">{contact_lead}</p>
          <form class="cform" data-cform action="../contact.php" method="post"
                data-endpoint="../contact.php" data-to="{email}" data-subject="{f_subject}"
                data-msg-required="{f_required}" data-msg-sending="{f_sending}"
                data-msg-sent="{f_sent}" data-msg-email="{f_bademail}" data-msg-rate="{f_rate}" novalidate>
            <input type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true"
                   class="cform__hp" />
            <div class="cform__row">
              <label class="field"><input type="text" name="name" placeholder=" " autocomplete="name" required /><span>{f_name}</span></label>
              <label class="field"><input type="email" name="email" placeholder=" " autocomplete="email" required /><span>{f_email}</span></label>
            </div>
            <label class="field"><textarea name="message" placeholder=" " required></textarea><span>{f_message}</span></label>
            <button type="submit" class="btn btn--primary">{i_arrow}{f_send}</button>
            <p class="cform__note" role="status" aria-live="polite"></p>
          </form>
          <div class="contact__or">{f_or}</div>
          <div class="contact__email">
            <a href="mailto:{email}">{email}</a>
            <button type="button" class="copy-btn" data-copy="{email}" data-copied="{t_copied}">{i_copy}<span class="copy-label">{t_copy}</span></button>
          </div>
          <div class="contact__channels">
        <a class="channel" href="mailto:{email}">{i_mail}{t_email}</a>
        <a class="channel" href="{github}" target="_blank" rel="noopener">{i_github}{t_github}</a>
        <a class="channel" href="{linkedin}" target="_blank" rel="noopener">{i_linkedin}{t_linkedin}</a>
        <a class="channel" href="{telegram}" target="_blank" rel="noopener">{i_telegram}{t_telegram}</a>
        <a class="channel" href="{instagram}" target="_blank" rel="noopener">{i_instagram}{t_instagram}</a>
        <span class="channel">{i_pin}{t_loc}</span></div>
        </div>
      </div>
    </section>
  </div>

  <footer class="footer">
    <div class="container footer__grid">
      <div>
        <span class="brand"><span class="brand__mark" aria-hidden="true"></span>{short}</span>
        <div class="footer__tag">{tagline}</div>
      </div>
      {footer_socials}
    </div>
    <div class="container" style="margin-top:1.4rem">
      <div class="footer__rights">© <span data-year></span> {name}. {t_rights}</div>
    </div>
  </footer>

  <nav class="dock" aria-label="Primary">{dock}</nav>

    <div class="resume-doc" aria-hidden="true">
      <div class="r-head">
        <div><div class="r-name">{name}</div><div class="r-title">{tagline}</div></div>
        <div class="r-contact">
          <div><a href="mailto:{email}">{email}</a></div>
          <div>github.com/AmirMoghtader</div>
          <div>linkedin.com/in/amir-h-moghtader</div>
          <div>{t_loc}</div>
        </div>
      </div>
      <div class="r-sec"><h2>{r_summary}</h2><p class="r-summary">{about_lead} {about_p0}</p></div>
      <div class="r-sec"><h2>{r_high}</h2><div class="r-high">{r_high_items}</div></div>
      <div class="r-sec"><h2>{r_exp}</h2>{r_exp_items}</div>
      <div class="r-sec"><h2>{r_edu}</h2>{r_edu_items}</div>
      <div class="r-sec"><h2>{r_sel}</h2>{r_vent_items}</div>
      <div class="r-sec"><h2>{r_skills}</h2><div class="r-skills">{r_skills_items}</div></div>
      <div class="r-sec"><h2>{r_more}</h2><div class="r-work">{r_work_items}</div></div>
      <div class="r-foot">{name} · amir.onwebs.ir · <span data-year></span></div>
    </div>

  <script src="../assets/js/app.js?v={av}" defer></script>
  <script type="module" src="../assets/js/orbs3d.js?v={av}"></script>
</body>
</html>
""".format(
        av=ASSET_V,
        code=hreflang,
        dirn=dirn, title=esc(d["title"]), desc=esc(d["desc"]), keywords=esc(d["keywords"]),
        name=esc(d["name"]), short=esc(d["short"]),
        tagline=esc(d["tagline"]), url=url, site=SITE, og=d["og"], alts=alts,
        ld=json.dumps(ld, ensure_ascii=False),
        brand=brand, navlinks=navlinks, langmenu=langmenu, mlinks=mlinks,
        i_sun=IC["sun"], i_moon=IC["moon"], i_globe=IC["globe"], i_arrow=IC["arrow"],
        i_pin=IC["pin"], i_grid=IC["grid"], i_search=IC["search"], i_quote=IC["quote"],
        i_lock=IC["lock"], i_copy=IC["copy"], i_mail=IC["mail"], i_cap=IC["cap"],
        i_github=IC["github"], i_linkedin=IC["linkedin"], i_telegram=IC["telegram"], i_instagram=IC["instagram"],
        t_theme=esc(u["theme"]), t_lang=esc(u["lang"]), t_resume=esc(u["resume"]),
        t_menu=esc(u["menu"]), t_loc=esc(u["loc"]), t_contact_me=esc(u["contact_me"]),
        t_see_work=esc(u["see_work"]), t_copy=esc(u["copy"]), t_copied=esc(u["copied"]),
        t_email=esc(u["email"]), t_github=esc(u["github"]), t_linkedin=esc(u["linkedin"]),
        t_telegram=esc(u["telegram"]), t_instagram=esc(u["instagram"]), t_rights=esc(u["rights"]),
        hero_role=esc(d["hero_role"]), hero_socials=socials("hero__socials reveal"),
        footer_socials=socials("footer__socials"),
        stats=stats,
        about_eyebrow=esc(d["about_eyebrow"]), about_title=esc(d["about_title"]),
        about_lead=esc(d["about_lead"]),
        about_body="".join("<p>%s</p>" % esc(p) for p in d["about_p"]),
        about_p0=esc(d["about_p"][0]),
        orbs="".join(
            '<span class="orb" style="--x:%s;--y:%s;--s:%s;--dur:%s;--dly:%s;--dx:%s;--dy:%s">'
            '<img src="../assets/images/tech/%s.png" alt="" width="256" height="256"'
            ' loading="lazy" decoding="async" /></span>'
            % (x, y, sz, dur, dly, dx, dy, f)
            for f, x, y, sz, dur, dly, dx, dy in ORBS),
        roles_eyebrow=esc(d["roles_eyebrow"]), roles_title=esc(d["roles_title"]),
        roles_sub=esc(d["roles_sub"]), timeline=timeline,
        edu_eyebrow=esc(d["edu_eyebrow"]), edu_title=esc(d["edu_title"]),
        edu_sub=esc(d["edu_sub"]), edu=rolecards(d["edu"]),
        ven_eyebrow=esc(d["ven_eyebrow"]), ven_title=esc(d["ven_title"]),
        ven_sub=esc(d["ven_sub"]), ventures="".join(vents),
        gal_eyebrow=esc(d["gal_eyebrow"]), gal_title=esc(d["gal_title"]),
        gal_sub=esc(d["gal_sub"]), shots=shots,
        geo_eyebrow=esc(d["geo_eyebrow"]), geo_title=esc(d["geo_title"]),
        geo_lead=esc(d["geo_lead"]), geo_cards=geocards,
        skills_eyebrow=esc(d["skills_eyebrow"]), skills_title=esc(d["skills_title"]),
        skills_sub=esc(d["skills_sub"]), skills="".join(sk),
        work_eyebrow=esc(d["work_eyebrow"]), work_title=esc(d["work_title"]),
        work_sub=esc(d["work_sub"]), works=works, work_note=esc(d["work_note"]),
        faq_eyebrow=esc(d["faq_eyebrow"]), faq_title=esc(d["faq_title"]),
        faq_items="".join(
            '<details class="faq__item reveal"%s>'
            '<summary><h3>%s</h3></summary><p>%s</p></details>'
            % (" open" if i == 0 else "", esc(q), esc(a))
            for i, (q, a) in enumerate(d["faq"])),
        contact_eyebrow=esc(d["contact_eyebrow"]), contact_title=esc(d["contact_title"]),
        contact_lead=esc(d["contact_lead"]),
        email=EMAIL, github=GITHUB, linkedin=LINKEDIN, telegram=TELEGRAM, instagram=INSTAGRAM,
        f_name=esc(d["form"]["name"]), f_email=esc(d["form"]["email"]),
        f_message=esc(d["form"]["message"]), f_send=esc(d["form"]["send"]),
        f_subject=esc(d["form"]["subject"]), f_required=esc(d["form"]["required"]),
        f_sending=esc(d["form"]["sending"]), f_or=esc(d["form"]["or"]),
        f_sent=esc(d["form"]["sent"]), f_bademail=esc(d["form"]["bademail"]),
        f_rate=esc(d["form"]["rate"]),
        deck_json=deck_json,
        dock=dock,
        r_summary=esc(r["summary"]), r_high=esc(r["high"]), r_exp=esc(r["exp"]),
        r_edu=esc(r["edu"]), r_sel=esc(r["sel"]), r_skills=esc(r["skills"]), r_more=esc(r["more"]),
        r_high_items=r_high, r_exp_items=r_exp, r_edu_items=r_edu, r_vent_items=r_vent,
        r_skills_items=r_skills, r_work_items=r_work,
    )
    return html


def main():
    for code, hreflang, _label in LOCALES:
        d = L[code]
        path = os.path.join(OUT, code, "index.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(code, hreflang, d))
        print("wrote", path, len(open(path, encoding="utf-8").read()), "bytes")

    # ---- root redirect page ----
    pills = "".join(
        '<a href="./%s/" hreflang="%s" style="display:inline-block;margin:.3rem .5rem;padding:.5rem .9rem;'
        'border:1px solid #ccc;border-radius:999px;color:inherit;text-decoration:none">%s</a>'
        % (c, hl, lbl) for c, hl, lbl in LOCALES)
    alts = "\n  ".join('<link rel="alternate" hreflang="%s" href="%s/%s/" />' % (hl, SITE, c)
                       for c, hl, _ in LOCALES)
    root = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Amir H. Moghtader — Web Developer, UI/UX Designer &amp; SEO Specialist</title>
  <meta name="description" content="Amir H. Moghtader — web developer, UI/UX designer and SEO &amp; GEO specialist. Founder of Onwebs, maker of Avanobat, web developer at 4cuatro." />
  <link rel="canonical" href="{site}/fa/" />
  {alts}
  <link rel="alternate" hreflang="x-default" href="{site}/fa/" />
  <link rel="icon" type="image/png" href="favicon.png" />
  <meta http-equiv="refresh" content="0; url=./fa/" />
  <style>body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#fcfcfb;color:#0c0f0e;display:grid;place-items:center;min-height:100vh;margin:0;text-align:center;padding:2rem}}@media(prefers-color-scheme:dark){{body{{background:#080a0a;color:#ecf1ef}}}}h1{{font-size:1.4rem;font-weight:800;margin:0 0 .3rem}}p{{color:#717b79;margin:0 0 1.5rem}}</style>
  <script>
    /* Only a fallback: .htaccess normally negotiates this server-side.
       Anything we do not publish falls back to Persian. */
    (function(){{var m={{fa:"fa",en:"en",ar:"ar",zh:"zh",ru:"ru",es:"es",nb:"no",nn:"no",no:"no"}};
    var l=(navigator.language||"fa").toLowerCase().split("-")[0];
    location.replace("./"+(m[l]||"fa")+"/");}})();
  </script>
</head>
<body>
  <h1>Amir H. Moghtader</h1>
  <p>Web developer &amp; UI/UX designer</p>
  <div>{pills}</div>
</body>
</html>
""".format(site=SITE, alts=alts, pills=pills)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(root)
    print("wrote index.html")

    # ---- sitemap ----
    rows = []
    for code, hreflang, _ in LOCALES:
        links = "".join(
            '\n    <xhtml:link rel="alternate" hreflang="%s" href="%s/%s/" />' % (hl, SITE, c)
            for c, hl, _ in LOCALES)
        links += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s/fa/" />' % SITE
        rows.append(
            '  <url>\n    <loc>%s/%s/</loc>%s\n    <lastmod>%s</lastmod>\n'
            '    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>'
            % (SITE, code, links, LASTMOD, "1.0" if code == "fa" else "0.9"))
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
               '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
               + "\n".join(rows) + "\n</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap)
    print("wrote sitemap.xml")

    # ---- manifest ----
    manifest = {
        "name": "Amir H. Moghtader",
        "short_name": "A. Moghtader",
        "description": "Web developer, UI/UX designer and SEO & GEO specialist.",
        "start_url": "/fa/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#fcfcfb",
        "theme_color": "#1e4c8f",
        "lang": "fa",
        "icons": [
            {"src": "/favicon.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png", "purpose": "any"},
        ],
    }
    with open(os.path.join(OUT, "manifest.webmanifest"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("wrote manifest.webmanifest")

    # ---- robots ----
    # AI crawlers are named explicitly: several of them ignore a bare wildcard
    # allow, and being citable by them is the whole point of the GEO work.
    ai_agents = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot",
                 "Perplexity-User", "ClaudeBot", "Claude-User", "Claude-SearchBot",
                 "Google-Extended", "Applebot", "Applebot-Extended", "Bingbot",
                 "CCBot", "meta-externalagent", "Amazonbot", "YandexBot"]
    robots = "User-agent: *\nAllow: /\n\n"
    for a in ai_agents:
        robots += "User-agent: %s\nAllow: /\n\n" % a
    robots += "Sitemap: %s/sitemap.xml\n" % SITE
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(robots)
    print("wrote robots.txt")

    # ---- llms.txt ----
    # Plain-language entity summary for generative engines. Same facts as the
    # page, in the format they parse most cleanly.
    en = L["en"]
    llms = ["# Amir H. Moghtader", "",
            "> " + en["desc"], "",
            "Also written: " + ", ".join(NAME_VARIANTS) + ".", "",
            "## Profile", ""]
    llms += [
        "- Name: Amir H. Moghtader (سید امیرحسین مقتدر)",
        "- Role: Web developer, UI/UX designer, SEO & GEO specialist",
        "- Location: Mashhad, Iran",
        "- Founder of: Onwebs / Vira Web Aria (%s), Avanobat (%s)" % (ONWEBS, AVANOBAT),
        "- Web developer at: Cuatro Group / 4cuatro, Bergen, Norway (%s)" % CUATRO,
        "- Education: B.Sc. Mechanical Engineering, Shahid Rajaee University, Mashhad; "
        "M.Sc. student in Mechatronics, Azad University",
        "- Email: " + EMAIL,
        "- GitHub: " + GITHUB,
        "- LinkedIn: " + LINKEDIN,
        "", "## Selected work", "",
    ]
    llms += ["- %s — %s %s" % (v["n"], v["s"], ("(" + v["u"] + ")") if v.get("u") else "")
             for v in en["ventures"]]
    llms += ["", "## FAQ", ""]
    for q, a in en["faq"]:
        llms += ["### " + q, "", a, ""]
    llms += ["## Pages", ""]
    llms += ["- [%s](%s/%s/) — %s" % (lbl, SITE, c, L[c]["title"]) for c, _hl, lbl in LOCALES]
    llms += ["", "## Licence", "",
             "Facts on this page may be quoted with attribution to Amir H. Moghtader, "
             + SITE + "/.", ""]
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(llms))
    print("wrote llms.txt")


if __name__ == "__main__":
    # The current Sepehr edition is maintained from the final multilingual
    # pages. Keep the legacy generator above for reference, but never let it
    # overwrite the personalised site with the previous portfolio content.
    import finalize_sep  # noqa: F401
    print("updated Sepehr Fathi portfolio pages")
