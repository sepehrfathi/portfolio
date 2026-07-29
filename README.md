# Sepehr Fathi — Portfolio / وب‌سایت شخصی سپهر فتحی

وب‌سایت رسمی و چندزبانهٔ سپهر فتحی با زبان پیش‌فرض فارسی، طراحی سبز اختصاصی،
حالت روشن/تیره، پشتیبانی کامل RTL/LTR و چیدمان ریسپانسیو.

Official multilingual portfolio for Sepehr Fathi. The site is self-hosted,
responsive, RTL/LTR-ready and has no CDN dependency.

## Preview

```bash
php -S 127.0.0.1:4173 _src/dev-router.php
```

سپس آدرس `http://127.0.0.1:4173/fa/` را باز کنید.

## Project structure

```text
fa/, en/, ar/, zh/, ru/, es/, no/  Final localized pages
assets/                            CSS, JavaScript, fonts and images
contact.php                        Contact form endpoint
_src/                              Maintenance and build helpers
DEPLOY.md                          cPanel deployment guide
```

صفحه‌های نهایی مستقیماً داخل پوشه‌های زبان نگهداری می‌شوند. برای اجرای دوبارهٔ
تنظیمات مشترک، متادیتا و اصلاحات همسان روی تمام زبان‌ها:

```bash
python3 _src/build.py
```

## Contact form

فرم تماس از `contact.php` استفاده می‌کند. تنظیمات خصوصی SMTP باید فقط روی سرور
داخل فایل `.smtp-config.php` قرار بگیرد. این فایل عمداً در `.gitignore` است و
نباید داخل مخزن Git ذخیره شود.

نمونهٔ ساختار تنظیمات موردنیاز در راهنمای [DEPLOY.md](DEPLOY.md) توضیح داده شده
است. سایت بدون این فایل نمایش داده می‌شود، اما ارسال فرم نیازمند تنظیم SMTP است.

## Deployment

محتوای لازم برای هاست:

```text
index.html
fa/ en/ ar/ zh/ ru/ es/ no/
assets/
contact.php
.htaccess
manifest.webmanifest
robots.txt
sitemap.xml
favicon.png
favicon-32.png
apple-touch-icon.png
llms.txt
```

راهنمای کامل انتشار روی cPanel در [DEPLOY.md](DEPLOY.md) قرار دارد.

## SEO

- زبان پیش‌فرض فارسی و مسیر اصلی `/fa/`
- canonical و hreflang برای هفت زبان
- Schema.org Person JSON-LD
- Open Graph و Twitter metadata
- sitemap، robots و `llms.txt`
- بهینه‌شده برای «سپهر فتحی»، `Sepehr Fathi`، رزومهٔ شخصی و سوپراپ بردسکن
