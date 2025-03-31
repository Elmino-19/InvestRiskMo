from src.config.database import get_db
from src.models.assessment import UserAssessment
from tabulate import tabulate
import pandas as pd

def view_assessments():
    """نمایش تمام ارزیابی‌های ثبت شده در دیتابیس"""
    db = next(get_db())
    try:
        # دریافت تمام رکوردها
        assessments = db.query(UserAssessment).all()
        
        if not assessments:
            print("هیچ رکوردی در دیتابیس یافت نشد!")
            return
        
        # تبدیل به دیکشنری برای نمایش بهتر
        data = []
        for assessment in assessments:
            data.append({
                'شناسه': assessment.id,
                'تاریخ': assessment.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'مرحله': assessment.step,
                'امتیاز کل': assessment.total_score,
                'سطح ریسک': assessment.risk_level,
                'پاسخ‌های عددی': assessment.numeric_answers,
                'پاسخ‌های متنی': assessment.text_answers
            })
        
        # تبدیل به DataFrame
        df = pd.DataFrame(data)
        
        # نمایش با فرمت جدول
        print("\n=== اطلاعات ارزیابی‌های ثبت شده ===\n")
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
        
        # نمایش آمار کلی
        print("\n=== آمار کلی ===")
        print(f"تعداد کل ارزیابی‌ها: {len(assessments)}")
        if assessments:
            avg_score = sum(a.total_score for a in assessments if a.total_score) / len([a for a in assessments if a.total_score])
            print(f"میانگین امتیاز: {avg_score:.2f}")
            
    finally:
        db.close()

if __name__ == "__main__":
    view_assessments()