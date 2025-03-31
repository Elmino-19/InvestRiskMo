from src.config.database import Base, engine
from src.models.assessment import UserAssessment, Demographics

def create_tables():
    """ایجاد تمام جداول تعریف شده در مدل‌ها"""
    print("در حال ایجاد جداول...")
    Base.metadata.create_all(bind=engine)
    print("جداول با موفقیت ایجاد شدند!")

if __name__ == "__main__":
    create_tables()
