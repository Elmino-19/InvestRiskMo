from sqlalchemy.orm import Session
from src.models.assessment import UserAssessment, Demographics

def create_assessment(db: Session, step: str, numeric_answers: dict, text_answers: dict, total_score: float = None):
    """ایجاد یک ارزیابی جدید"""
    db_assessment = UserAssessment(
        step=step,
        numeric_answers=numeric_answers,
        text_answers=text_answers,
        total_score=total_score,
        risk_level=calculate_risk_level(total_score) if total_score else None
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def calculate_risk_level(score: float) -> str:
    """محاسبه سطح ریسک بر اساس امتیاز"""
    if score <= 18:
        return "محافظه‌کار"
    elif score <= 30:
        return "متعادل"
    else:
        return "ریسک‌پذیر"

def get_assessment(db: Session, assessment_id: int):
    """دریافت یک ارزیابی با شناسه"""
    return db.query(UserAssessment).filter(UserAssessment.id == assessment_id).first()

def save_demographics(db: Session, assessment_id: int, data: dict):
    """ذخیره اطلاعات دموگرافیک"""
    demographics = Demographics(
        assessment_id=assessment_id,
        gender=data.get('gender'),
        age_range=data.get('age_range'),
        education=data.get('education'),
        investment_experience=data.get('investment_experience')
    )
    db.add(demographics)
    db.commit()
    db.refresh(demographics)
    return demographics
