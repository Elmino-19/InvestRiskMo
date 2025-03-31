from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from typing import Generator

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# خواندن متغیرهای محیطی
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# ساخت رشته اتصال به دیتابیس با استفاده از urllib.parse برای escape کردن کاراکترهای خاص
from urllib.parse import quote_plus
password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""

DATABASE_URL = f"postgresql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ایجاد موتور SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # برای بررسی اتصال قبل از استفاده
    pool_recycle=3600,   # بازیافت اتصال‌ها بعد از یک ساعت
)

# ایجاد کلاس پایه برای مدل‌ها
Base = declarative_base()

# ایجاد کلاس SessionLocal برای مدیریت نشست‌ها
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """
    تابع کمکی برای دریافت نشست دیتابیس
    
    Returns:
        Generator: یک جنریتور که نشست دیتابیس را برمی‌گرداند
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
