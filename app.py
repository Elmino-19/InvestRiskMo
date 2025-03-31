import sys
from pathlib import Path
import streamlit as st
import json
import time

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.config.database import get_db
from src.crud.assessment import create_assessment, save_demographics

def load_css(file_name: Path):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("فایل CSS یافت نشد!")

css_path = BASE_DIR / "static" / "css" / "styles.css"
load_css(css_path)
img_path = css_path = BASE_DIR / "static" / "logo-bedan.png"

def load_questionnaire():
    try:
        with open(BASE_DIR / 'data' / 'combined_questionnaire.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("فایل پرسشنامه یافت نشد!")
        return {}
    except json.JSONDecodeError:
        st.error("خطا در خواندن فایل JSON!")
        return {}

state = st.session_state

def calculate_risk_score(answers):
    valid_answers = [answer for answer in answers if answer is not None]
    return sum(valid_answers) if valid_answers else 0

def save_answers(step_answers, current_step):
    numeric_answers = {q: a for q, a in step_answers.items() if isinstance(a, (int, float))}
    text_answers = {q: a for q, a in step_answers.items() if not isinstance(a, (int, float))}
    
    db = next(get_db())
    try:
        assessment = create_assessment(
            db=db,
            step=current_step,
            numeric_answers=numeric_answers,
            text_answers=text_answers,
            total_score=state.get('total_score', 0)
        )
        if current_step == "step-2":
            save_demographics(db=db, assessment_id=assessment.id, data=text_answers)
        return True
    except Exception as e:
        st.error(f"خطا در ذخیره اطلاعات: {e}")
        return False
    finally:
        db.close()

def main():
    # مقداردهی اولیه فقط در اینجا انجام می‌شود
    if 'step' not in state:
        state.step = 1
    if 'scores' not in state:
        state.scores = []
    if 'total_score' not in state:
        state.total_score = 0

    st.title("پرسشنامه ارزیابی ریسک سرمایه‌گذاری")
    with st.sidebar:
        st.image(img_path, width=200)
        st.header("درباره پرسشنامه")
        st.text("این پرسشنامه برای ارزیابی ریسک‌پذیری سرمایه‌گذاران طراحی شده است. با پاسخ دادن به سوالات، شما می‌توانید درک بهتری از سطح ریسک خود داشته باشید.")
        st.text("این پرسشنامه شامل چهار مرحله است که هر یک شامل سوالات مختلفی است. لطفاً به هر سوال پاسخ بدهید.")
        st.text("پاسخ‌های شما در دیتابیس ذخیره می‌شوند و برای تحلیل و ارائه نتایج استفاده می‌شوند.")
        with st.form("form1"):
            side_col1, side_col2 = st.columns(2)
            side_col1.text_input("نام")
            side_col2.text_input("نام خانوادگی")
            st.text_input("ایمیل")
            st.text_input("شماره تماس")
            st.form_submit_button("ثبت مشخصات")
    # بررسی مراحل 1 تا 3
    if 1 <= state.step <= 3:
        questionnaire = load_questionnaire()
        if not questionnaire:
            return
        
        current_step = f"step-{state.step}"
        if current_step in questionnaire:
            step_data = questionnaire[current_step]
            st.header(step_data["title"])
            st.write(step_data["content"])
            
            with st.form(key=f'step_{state.step}'):
                step_answers = {}
                for question in step_data["questions"]:
                    q_number = question["number"]
                    q_content = question.get("content", question.get("CONTENT", ""))
                    options = question.get("answer-options", question.get("answer-option", []))
                    if not options:
                        st.error(f"گزینه‌های پاسخ برای سوال {q_number} یافت نشد!")
                        return
                    
                    choices = [opt.get("content", opt.get("CONTENT", "")) for opt in options]
                    scores = {opt.get("content", opt.get("CONTENT", "")): opt.get("score", opt.get("SCORE", None)) for opt in options}
                    
                    answer = st.radio(f"سوال {q_number}: {q_content}", choices, key=f"q_{state.step}_{q_number}")
                    step_answers[q_number] = scores[answer] if scores[answer] is not None else answer
                
                if st.form_submit_button("ثبت پاسخ‌ها"):
                    with st.spinner('در حال پردازش...'):
                        if save_answers(step_answers, current_step):
                            if state.step == 1:
                                numeric_answers = [v for v in step_answers.values() if isinstance(v, (int, float))]
                                state.total_score = calculate_risk_score(numeric_answers)
                            st.success("پاسخ‌ها ثبت شد!")
                            state.step = min(state.step + 1, 4)  # حداکثر به 4 محدود می‌شود
                            st.rerun()
    
    # نمایش نتایج در مرحله 4
    elif state.step == 4:
        st.header("نتیجه نهایی ارزیابی")
        
        # نمایش انیمیشن
        st.balloons()
        
        # نمایش امتیاز با طراحی جذاب
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
                <div class="risk-score-container">
                    <h2 class="risk-score-title">امتیاز ریسک‌پذیری شما</h2>
                    <h1 class="risk-score-value">{state.total_score}</h1>
                </div>
            """, unsafe_allow_html=True)
        
        st.subheader("تفسیر نتیجه")
        if state.total_score <= 18:
            st.info("شما یک سرمایه‌گذار محافظه‌کار هستید. پیشنهاد می‌شود بیشتر در دارایی‌های کم‌ریسک سرمایه‌گذاری کنید.") 
        elif state.total_score <= 30:
            st.info("شما یک سرمایه‌گذار متعادل هستید. می‌توانید ترکیبی از دارایی‌های کم‌ریسک و پرریسک داشته باشید.")
        else:
            st.info("شما یک سرمایه‌گذار ریسک‌پذیر هستید. می‌توانید بخش بیشتری از سرمایه خود را در دارایی‌های پرریسک سرمایه‌گذاری کنید.")
        
        if st.button("شروع مجدد پرسشنامه"):
            state.step = 1
            state.scores = []
            state.total_score = 0
            st.rerun()
    
    # مدیریت مقادیر نامعتبر state.step
    else:
        st.error(f"مرحله نامعتبر ({state.step})! لطفاً پرسشنامه را از ابتدا شروع کنید.")
        if st.button("شروع مجدد پرسشنامه"):
            state.step = 1
            state.scores = []
            state.total_score = 0
            st.rerun()

if __name__ == "__main__":
    main()