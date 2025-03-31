import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from src.config.database import get_db
from src.crud.assessment import create_assessment, save_demographics
import json
from datetime import datetime
import time
import pathlib

def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

css_path = pathlib.Path("static/css/styles.css")
load_css(css_path)
# خواندن فایل JSON
def load_questionnaire():
    with open('data/combined_questionnaire.json', 'r', encoding='utf-8') as file:
        return json.load(file)

state = st.session_state
# تنظیم حالت اولیه
if 'step' not in state:
    state.step = 1
if 'scores' not in state:
    state.scores = []
if 'answers' not in state:
    state.answers = {}

def calculate_risk_score(answers):
    total_score = sum(answer for answer in answers if answer is not None)
    return total_score

def save_answers(step_answers, current_step):
    """ذخیره پاسخ‌ها در دیتابیس"""
    numeric_answers = {}
    text_answers = {}
    
    for q_number, answer in step_answers.items():
        if isinstance(answer, (int, float)):
            numeric_answers[q_number] = answer
        else:
            text_answers[q_number] = answer
    
    # دریافت نشست دیتابیس
    db = next(get_db())
    
    try:
        # ایجاد رکورد جدید در دیتابیس
        assessment = create_assessment(
            db=db,
            step=current_step,
            numeric_answers=numeric_answers,
            text_answers=text_answers,
            total_score=state.get('total_score')
        )
        
        # اگر مرحله دوم است، اطلاعات دموگرافیک را ذخیره کن
        if current_step == "step-2":
            save_demographics(
                db=db,
                assessment_id=assessment.id,
                data=text_answers
            )
            
    except Exception as e:
        st.error(f"خطا در ذخیره اطلاعات در دیتابیس: {e}")

def main():
    if 'step' not in state:
        state.step = 1
    if 'scores' not in state:
        state.scores = []
    if 'total_score' not in state:
        state.total_score = 0

    st.title("پرسشنامه ارزیابی ریسک سرمایه‌گذاری")
    
    if state.step <= 3:
        # لود کردن پرسشنامه
        questionnaire = load_questionnaire()
        current_step = f"step-{state.step}"
        
        if current_step in questionnaire:
            step_data = questionnaire[current_step]
            
            # نمایش عنوان و توضیحات مرحله
            st.header(step_data["title"])
            st.write(step_data["content"])
            
            # فرم سوالات
            with st.form(key=f'step_{state.step}'):
                step_answers = {}
                
                for question in step_data["questions"]:
                    q_number = question["number"]
                    q_content = question.get("content", question.get("CONTENT", ""))
                    
                    options = question.get("answer-options", question.get("answer-option", []))
                    choices = []
                    scores = {}
                    
                    for opt in options:
                        content = opt.get("content", opt.get("CONTENT", ""))
                        score = opt.get("score", opt.get("SCORE", None))
                        choices.append(content)
                        scores[content] = score
                    
                    answer = st.radio(
                        f"سوال {q_number}: {q_content}",
                        choices,
                        key=f"q_{q_number}"
                    )
                    
                    # اگر امتیاز null باشد، متن پاسخ ذخیره می‌شود
                    if scores[answer] is None:
                        step_answers[q_number] = answer
                    else:
                        step_answers[q_number] = scores[answer]
                
                submitted = st.form_submit_button("ثبت پاسخ‌ها")
                
                if submitted:
                    # نمایش اسپینر
                    with st.spinner('در حال پردازش پاسخ‌های شما...'):
                        time.sleep(1)  # اضافه کردن تاخیر برای نمایش بهتر اسپینر
                        
                        # ذخیره پاسخ‌ها
                        save_answers(step_answers, current_step)
                        
                        # محاسبه امتیاز در مرحله اول
                        if state.step == 1:
                            numeric_answers = [
                                score for score in step_answers.values() 
                                if isinstance(score, (int, float))
                            ]
                            if numeric_answers:
                                risk_score = calculate_risk_score(numeric_answers)
                                state.total_score = risk_score
                    
                    st.success("پاسخ‌های شما با موفقیت ثبت شد.")
                    
                    # رفتن به مرحله بعد
                    if state.step < 3:
                        state.step += 1
                        st.rerun()
                    else:
                        state.step = 4
                        st.rerun()
    
    # نمایش نتیجه نهایی در مرحله چهارم
    elif state.step == 4:
        st.header("نتیجه نهایی ارزیابی")
        
        # نمایش انیمیشن
        st.balloons()
        
        # نمایش امتیاز با طراحی جذاب
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div class="risk-score-container">
                    <h2 class="risk-score-title">امتیاز ریسک‌پذیری شما</h2>
                    <h1 class="risk-score-value">{}</h1>
                </div>
            """.format(state.total_score), unsafe_allow_html=True)
        
        # تفسیر امتیاز
        st.subheader("تفسیر نتیجه")
        if state.total_score <= 18:
            st.info("شما یک سرمایه‌گذار محافظه‌کار هستید. پیشنهاد می‌شود بیشتر در دارایی‌های کم‌ریسک سرمایه‌گذاری کنید.")
        elif state.total_score <= 30:
            st.info("شما یک سرمایه‌گذار متعادل هستید. می‌توانید ترکیبی از دارایی‌های کم‌ریسک و پرریسک داشته باشید.")
        else:
            st.info("شما یک سرمایه‌گذار ریسک‌پذیر هستید. می‌توانید بخش بیشتری از سرمایه خود را در دارایی‌های پرریسک سرمایه‌گذاری کنید.")
        
        # دکمه شروع مجدد
        if st.button("شروع مجدد پرسشنامه"):
            state.step = 1
            state.scores = []
            state.total_score = 0
            st.rerun()
    else:
        st.error("خطا در بارگذاری پرسشنامه")

if __name__ == "__main__":
    main()
