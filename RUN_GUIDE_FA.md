# راهنمای کامل اجرای Technamooz Panel

این نسخه بر پایه‌ی پروژه‌ی `Panel_Technamooz_Railway_Ready` ساخته شده است. منطق API، تولید کانفیگ، ذخیره‌سازی، relay و endpointهای موجود حفظ شده‌اند و تغییر اصلی روی رابط کاربری و مسیرهای HTML اعمال شده است.

## ساختار پروژه

```text
.
├── panel/
│   ├── main.py              # FastAPI application و routeهای API/HTML
│   ├── pages.py             # قالب جدید Terminal، Login و Control Panel
│   ├── relay_vless.py       # relay موجود VLESS/Trojan
│   ├── xhttp_siz10.py       # handler موجود XHTTP
│   ├── speed_limit.py       # کنترل سرعت و IP
│   ├── telegram_bot.py      # ربات و تنظیمات تلگرام
│   └── tests/               # تست‌های پروژه
├── requirements.txt
├── Procfile
├── railway.json
├── .env.example
└── RUN_GUIDE_FA.md
```

## جریان ورود جدید

1. بازکردن دامنه‌ی اصلی، کاربر را به `/terminal` می‌فرستد.
2. در ترمینال اولیه باید این دستور وارد شود:

```text
login to panel
```

3. کاربر به `/login` منتقل می‌شود.
4. پس از ورود موفق، کاربر دوباره به `/terminal` می‌رود؛ این بار ترمینال اصلی و احراز‌شده نمایش داده می‌شود.
5. برای فعال‌سازی پنل باید این دستور دقیق وارد شود:

```text
amirparsa-panel-technamooz2026
```

6. پس از تأیید سمت سرور، کاربر وارد `/panel` می‌شود.
7. مسیر قدیمی `/dashboard` فقط برای bookmarkهای قدیمی باقی مانده و به مسیر جدید هدایت می‌شود.

> این command یک gate اضافی برای UX و مسیر ورود است، نه رمزنگاری واقعی؛ چون کد Frontend قابل مشاهده است. امنیت اصلی توسط username، password، captcha و session cookie تأمین می‌شود.

## اجرای محلی

### ۱. ساخت محیط مجازی

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### ۲. تنظیم متغیرهای محیطی

Linux/macOS:

```bash
export ADMIN_USERNAME='choose-a-new-admin-username'
export ADMIN_PASSWORD='choose-a-long-random-password'
export SECRET_KEY='generate-a-long-random-secret-key'
export DATA_DIR="$(pwd)/data"
export PORT=8000
export PYTHONUNBUFFERED=1
```

PowerShell:

```powershell
$env:ADMIN_USERNAME = 'choose-a-new-admin-username'
$env:ADMIN_PASSWORD = 'choose-a-long-random-password'
$env:SECRET_KEY = 'generate-a-long-random-secret-key'
$env:DATA_DIR = "$PWD/data"
$env:PORT = '8000'
$env:PYTHONUNBUFFERED = '1'
```

برای ساخت secret تصادفی:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

### ۳. اجرای production-like

```bash
python -m uvicorn panel.main:app \
  --host 0.0.0.0 \
  --port "${PORT:-8000}" \
  --proxy-headers \
  --forwarded-allow-ips="*"
```

سپس مرورگر را باز کنید:

```text
http://127.0.0.1:8000/
```

### ۴. تست health

```bash
curl -i http://127.0.0.1:8000/health
```

پاسخ باید HTTP 200 باشد.

## اجرای تست‌ها

```bash
python -m compileall -q panel
python -m unittest discover -s panel/tests -v
```

برای بررسی JavaScript ترمینال نیز می‌توان script را از HTML استخراج و با `node --check` بررسی کرد. تست integration مسیر ورود، unlock و logout در زمان ساخت این نسخه اجرا شده است.

## استقرار روی Railway

### ۱. Repository

محتویات این پوشه را در یک repository جدید قرار دهید. فایل‌های زیر را commit نکنید:

```text
.env
.env.*.local
data/
__pycache__/
```

فایل `.env.example` فقط نمونه است و نباید با secret واقعی commit شود.

### ۲. متغیرهای Railway

در بخش **Variables** این مقادیر را اضافه کنید:

```env
ADMIN_USERNAME=یک_نام_کاربری_جدید_و_غیرقابل_حدس
ADMIN_PASSWORD=یک_رمز_طولانی_و_تصادفی
SECRET_KEY=یک_کلید_تصادفی_حداقل_۳۲_بایتی
DATA_DIR=/data
PYTHONUNBUFFERED=1
TRUST_PROXY_HEADERS=true
SECURE_COOKIES=true
```

برای نمونه‌ی متغیرهای دیگر، `.env.example` را ببینید. مقدار نمونه‌ی داخل مستندات را به‌عنوان credential واقعی استفاده نکنید.

### ۳. Volume

چون نسخه‌ی پایه state را در فایل ذخیره می‌کند:

1. در Railway یک Volume به سرویس متصل کنید.
2. mount path را روی این مقدار بگذارید:

```text
/data
```

3. مقدار `DATA_DIR=/data` را تنظیم کنید.

بدون Volume، state فایل در restart یا deploy ممکن است ماندگار نباشد.

### ۴. Deploy

Railway با `Procfile` یا `railway.json` این فرمان را اجرا می‌کند:

```bash
python -m uvicorn panel.main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips="*"
```

Railway باید مقدار `PORT` را خودش تزریق کند؛ پورت را hardcode نکنید.

### ۵. Healthcheck و دامنه

در تنظیمات سرویس:

```text
Healthcheck path: /health
```

بعد از ساخت دامنه، این URL را بررسی کنید:

```text
https://YOUR-DOMAIN.up.railway.app/health
```

### ۶. ورود نهایی

```text
https://YOUR-DOMAIN.up.railway.app/
```

ترتیب ورود:

```text
/terminal
login to panel
/login
username + password + captcha
/terminal
amirparsa-panel-technamooz2026
/panel
```

## نکات مهم امنیتی

- از credential پیش‌فرض استفاده نکنید.
- `ADMIN_PASSWORD` و `SECRET_KEY` را در GitHub، Screenshot یا چت عمومی منتشر نکنید.
- اگر credential قبلی در نسخه‌ای افشا شده، آن را در Railway rotate کنید.
- command ترمینال را قابلیت امنیتی اصلی در نظر نگیرید؛ session و password امنیت واقعی هستند.
- در Railway فقط HTTP/HTTPS عمومی در دسترس است؛ اجرای مستقیم همه‌ی پورت‌های TCP/UDP V2Ray به محدودیت شبکه و TCP Proxy Railway وابسته است.
- اگر چند replica اجرا می‌کنید، state حافظه‌ای session و unlock بین replicaها مشترک نیست؛ برای چند replica باید session و state به storage مشترک منتقل شود.

## مسیرهای اصلی

| مسیر | کاربرد |
|---|---|
| `/` | redirect به ترمینال اولیه |
| `/terminal` | ترمینال اولیه یا ترمینال احراز‌شده |
| `/login` | ورود مدیر |
| `/panel` | پنل جدید پس از unlock |
| `/dashboard` | compatibility redirect قدیمی |
| `/health` | healthcheck Railway |
| `/api/*` | APIهای موجود پروژه |

## وضعیت راستی‌آزمایی این نسخه

موفق:

- compile کامل package `panel`
- import و route contract
- تست‌های موجود backend
- تست `health` روی Uvicorn واقعی
- redirect ریشه به `/terminal`
- redirect کاربر ناشناس از `/panel`
- ورود با captcha
- ردکردن command اشتباه
- قبول command صحیح
- نمایش `/panel` پس از unlock
- قفل‌شدن مجدد `/panel` بعد از logout
- syntax JavaScript ترمینال

تست‌نشده:

- deploy واقعی روی حساب Railway کاربر
- رفتار Volume واقعی Railway
- تست مرورگرهای Android/iOS و کلاینت‌های V2Ray
- اجرای عمومی TCP/UDP که به قابلیت شبکه‌ی Railway وابسته است
