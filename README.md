# Technamooz Panel — Terminal UI Edition

نسخه‌ی جدید رابط کاربری پنل مدیریت کانفیگ با تم مشکی/قرمز، Glass UI، پشتیبانی فارسی/انگلیسی و مسیر ورود ترمینالی.

## مسیر کاربر

```text
/ → /terminal
login to panel → /login
login موفق → /terminal اصلی
amirparsa-panel-technamooz2026 → /panel
```

APIها، منطق تولید کانفیگ و هسته‌ی موجود پروژه حفظ شده‌اند. کد اجرایی در package `panel/` قرار گرفته و فایل‌های `Procfile` و `railway.json` برای اجرای Railway در ریشه باقی مانده‌اند.

راهنمای کامل اجرای Local، تنظیم Variables، Volume، Deploy روی Railway و تست‌ها:

- [RUN_GUIDE_FA.md](RUN_GUIDE_FA.md)

اجرای سریع محلی:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ADMIN_USERNAME='your-admin'
export ADMIN_PASSWORD='your-long-password'
export SECRET_KEY='your-long-secret'
export DATA_DIR="$PWD/data"
python -m uvicorn panel.main:app --host 0.0.0.0 --port "${PORT:-8000}" --proxy-headers --forwarded-allow-ips="*"
```

تست:

```bash
python -m compileall -q panel
python -m unittest discover -s panel/tests -v
```

برای Railway حتماً `ADMIN_USERNAME`، `ADMIN_PASSWORD` و `SECRET_KEY` واقعی را در Variables تنظیم کنید و برای ماندگاری state یک Volume با mount path برابر `/data` متصل کنید.
