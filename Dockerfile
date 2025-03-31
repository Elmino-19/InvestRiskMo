# استفاده از تصویر پایه پایتون 3.12
FROM python:3.12-slim

# تنظیم متغیرهای محیطی
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# تنظیم دایرکتوری کاری
WORKDIR /app

# نصب uv
RUN pip install uv

# کپی فایل‌های پروژه
COPY pyproject.toml requirements.txt ./
COPY src/ ./src/
COPY static/ ./static/
COPY data/ ./data/

# نصب وابستگی‌ها با استفاده از uv
RUN uv pip install -r requirements.txt

# تنظیم PYTHONPATH
ENV PYTHONPATH=/app

# پورت پیش‌فرض برای Streamlit
EXPOSE 8501

# دستور اجرای برنامه
CMD ["streamlit", "run", "src/app.py", "--server.address", "0.0.0.0"]
