# Sepehr Fathi — Portfolio / وب‌سایت شخصی

یک وب‌سایت شخصی **مینیمال، تک‌رنگ (برند تیل)، ریسپانسیو و چندزبانه** (۷ زبان) که
**کاملاً خودبسنده و آفلاین‌محور** است — بدون هیچ CDN یا وابستگی خارجی، پس **روی اینترنت ملی کار می‌کند**.

A minimal, single‑brand‑colour, fully responsive, 7‑language personal site. **Zero external dependencies** (self‑hosted Kalameh font, inline SVG icons) so it works on Iran's national internet. Light/dark, RTL + LTR, and a **print‑to‑PDF résumé**.

---

## 🚀 ساخت و اجرا / Build & run

همهٔ صفحات از روی فایل‌های `content/<lang>.json` ساخته می‌شوند. برای بازسازی:

```bash
node build.mjs
```

این دستور برای هر زبانِ موجود یک صفحهٔ `<lang>/index.html` می‌سازد و همچنین
`index.html` (ریشه، ریدایرکت هوشمند زبان)، `sitemap.xml`، `robots.txt` و
`manifest.webmanifest` را تولید می‌کند. (فایل‌های `favicon.png`، `favicon-32.png` و
`apple-touch-icon.png` از روی لوگو ساخته شده‌اند و دارایی ثابت‌اند — build آن‌ها را بازنمی‌نویسد.)

پیش‌نمایش محلی / Local preview:

```bash
python3 -m http.server 8000
# سپس باز کنید: http://localhost:8000/
```

> صفحه‌ها با مسیرهای نسبی کار می‌کنند؛ روی هر هاست استاتیکی (یا اینترنت ملی) قابل میزبانی‌اند.

## 📦 بستهٔ آمادهٔ آپلود / Ready-to-upload package

فایل **`sepportfolio-deploy.zip`** شاملِ همهٔ فایل‌های موردنیاز برای هاست است (۷ زبان + `assets` +
آیکن‌ها + sitemap/robots/manifest، بدون سورس و بکاپ). کافی است محتوایش را داخل `public_html` اکسترکت کنی.

برای ساختن دوبارهٔ این zip بعد از هر تغییر:
```bash
node build.mjs
zip -r -X sepportfolio-deploy.zip fa en ar zh ru es no assets index.html \
  favicon.png favicon-32.png apple-touch-icon.png sitemap.xml robots.txt manifest.webmanifest \
  -x "assets/images/[0-9]*.webp" -x "*.DS_Store"
```

**ویژگی‌های موبایل/دسکتاپ:** روی موبایل ناوبری با یک **باتم‌بارِ شیشه‌ای (glass dock)** انجام می‌شود
(به‌جای منوی همبرگری)؛ بخش **گالری نمونه‌کارها** از تصاویر واقعی در `assets/images/portfolio/` استفاده می‌کند.

---

## ✏️ ویرایش محتوا / Editing content

- محتوای هر زبان در `content/<lang>.json` است (کلیدها در همهٔ زبان‌ها یکسان‌اند).
- فارسی و انگلیسی مرجع‌اند: `content/fa.json` و `content/en.json`.
- بعد از هر ویرایش، `node build.mjs` را دوباره اجرا کنید.
- برای افزودن زبان جدید: یک `content/<code>.json` بسازید و کد زبان را به آرایهٔ `LANGS` در `build.mjs` اضافه کنید.

## 🎨 تغییر رنگ برند / Rebranding

کل هویت بصری از **یک رنگ** ساخته شده. در ابتدای `assets/css/styles.css`:

```css
--brand:#0a7c6f;      /* رنگ اصلی برند (تیل) */
--brand-2:#0fb3a1;    /* هایلایت روشن‌تر */
```

و معادل‌های حالت تیره (`--brand`, `--brand-2`) در بلوک‌های `data-theme="dark"`.
همین دو مقدار را عوض کنید تا کل سایت رنگ‌بندی جدید بگیرد.

---

## ⚠️ قبل از انتشار این‌ها را تنظیم/تأیید کنید / Before you publish

| مورد | محل | مقدار فعلی |
|---|---|---|
| **دامنه** (برای canonical / hreflang / sitemap) | `build.mjs` → `BASE_URL` | `https://sep.onwebs.dev` |
| گیت‌هاب / لینکدین / تلگرام | `build.mjs` → `LINKS` | `github.com/sepehrfathi` و … |
| ایمیل | `content/*.json` → `contact.email` | `ftsepi@gmail.com` |

پس از تغییر `BASE_URL` یا `LINKS`، دوباره `node build.mjs` را اجرا کنید.
اگر شماره تماس هم می‌خواهید، می‌توان یک کانال جدید به بخش `contact.channels` اضافه کرد.

> **گیت‌هاب:** پروژه‌های واقعیت (پلاک‌یاب، تشخیص پهپاد، HomAI، CAR-T، PrismBench، NanoSWIM و …)
> با توضیح دقیق و متریکِ واقعی نمایش داده شده‌اند؛ بخشی از ریپوها عمومی و بقیه خصوصی‌اند.

---

## 📄 رزومه PDF / Résumé

دکمهٔ «دانلود رزومه» پنجرهٔ چاپ مرورگر را باز می‌کند؛ کاربر **«Save as PDF»** را می‌زند و یک
رزومهٔ تمیز و حرفه‌ای (به همان زبان صفحه) می‌گیرد. این رزومه با استایل چاپیِ اختصاصی از همان
محتوای صفحه ساخته می‌شود (بخش `.resume-doc`) و همیشه با سایت هماهنگ است — بدون هیچ کتابخانهٔ خارجی.

---

## 🗂 ساختار / Structure

```
content/<lang>.json     ← محتوا (منبع حقیقت)   / content source of truth
build.mjs               ← تولیدکنندهٔ استاتیک   / static generator
assets/css/styles.css   ← دیزاین سیستم (تک‌رنگ، RTL/LTR، لایت/دارک، چاپ)
assets/js/app.js        ← رفتار (تم، زبان، منو، ریویل، کپی، چاپ)
assets/fonts/TTF/…      ← فونت کلمه (محلی)     / local Kalameh font
<lang>/index.html       ← صفحهٔ ساخته‌شده هر زبان (خروجی)
index.html, sitemap.xml, robots.txt, manifest.webmanifest, favicon.png  (خروجی)
_old_backup/            ← نسخهٔ قدیمی سایت (بکاپ — برای انتشار لازم نیست)
```

## 🔍 سئو / SEO

hreflang کامل برای ۷ زبان + `x-default`، canonical به ازای هر زبان، JSON‑LD (Person)،
Open Graph / Twitter، `sitemap.xml` با لینک‌های چندزبانه، `robots.txt` و `manifest`.
هر صفحه `lang` و `dir` درست، و `<title>`/توضیحات بومی‌شده دارد.
