# پرسشنامه ارزیابی ریسک سرمایه‌گذاری 📊

این پروژه یک سیستم پرسشنامه آنلاین برای ارزیابی ریسک‌پذیری سرمایه‌گذاران است که با استفاده از Streamlit و PostgreSQL پیاده‌سازی شده است.

## ویژگی‌ها 🌟

- پرسشنامه چند مرحله‌ای با امتیازدهی خودکار
- ذخیره‌سازی پاسخ‌ها در دیتابیس PostgreSQL
- داشبورد مدیریتی برای تحلیل نتایج
- رابط کاربری فارسی و راست‌به‌چپ
- پشتیبانی از Docker برای اجرای ساده

## پیش‌نیازها 📋

- Python 3.12 یا بالاتر
- Docker و Docker Compose
- uv (برای مدیریت پکیج‌ها)

## نصب و راه‌اندازی 🚀

### روش اول: استفاده از Docker

1. کلون کردن مخزن:
```bash
git clone https://github.com/Elmino-19/InvestRiskMo.git
cd InvestRiskMo
```

2. ساخت فایل `.env` از روی نمونه:
```bash
cp .env.example .env
```

3. تنظیم متغیرهای محیطی در `.env`

4. اجرای برنامه:
```bash
docker-compose up --build
```

## لایسنس 📄

این پروژه تحت لایسنس MIT منتشر شده است.
