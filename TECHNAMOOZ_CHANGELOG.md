# Panel Technamooz v1.0.0.0 Stable

نسخهٔ stable اختصاصی Technamooz با کپچای سروری، username/password، تغییر credential، localization دو‌زبانه، تم‌های dark/light، لوگوی رسمی، مرکز کنترل ربات Telegram و تنظیمات Railway آماده شد.

## Railway-ready hardening — 2026-10-11
- secure cookie قابل تنظیم با پشتیبانی از HTTPS پشت reverse proxy.
- هدرهای امنیتی مرورگر و flush/fsync برای state file.
- hashهای جدید رمز عبور با bcrypt با حفظ سازگاری PBKDF2 قدیمی.
- `.python-version`، `.env.example`، `.gitignore` و تست‌های واحد.
- مستندسازی Volume، single-worker و محدودیت TCP/UDP Railway.
