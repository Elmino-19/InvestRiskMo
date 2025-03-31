import streamlit as st
import pandas as pd
import plotly.express as px
from src.config.database import get_db
from src.models.assessment import UserAssessment
from datetime import datetime, timedelta

# تنظیمات صفحه
st.set_page_config(page_title="داشبورد مدیریت پرسشنامه", layout="wide")

# اعمال CSS برای راست به چپ کردن
st.markdown("""
    <style>
        .css-1d391kg {
            direction: rtl;
        }
        .stMarkdown {
            direction: rtl;
            text-align: right;
        }
        .stSelectbox label {
            direction: rtl;
            text-align: right;
        }
        div[data-testid="stMetricValue"] {
            direction: rtl;
        }
        .css-1629p8f h1 {
            text-align: right;
        }
        .css-1629p8f h2 {
            text-align: right;
        }
        .css-1629p8f h3 {
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

def load_data():
    """بارگیری داده‌ها از دیتابیس"""
    db = next(get_db())
    try:
        assessments = db.query(UserAssessment).all()
        data = []
        for assessment in assessments:
            data.append({
                'شناسه': assessment.id,
                'تاریخ': assessment.timestamp,
                'مرحله': assessment.step,
                'امتیاز': assessment.total_score,
                'سطح_ریسک': assessment.risk_level,
                'پاسخ‌های_عددی': assessment.numeric_answers,
                'پاسخ‌های_متنی': assessment.text_answers
            })
        return pd.DataFrame(data)
    finally:
        db.close()

def main():
    st.title("داشبورد مدیریت پرسشنامه")
    
    # بارگیری داده‌ها
    df = load_data()
    if df.empty:
        st.warning("هیچ داده‌ای در دیتابیس یافت نشد!")
        return
    
    # نمایش فیلترها در سایدبار
    with st.sidebar:
        st.header("فیلترها")
        
        # فیلتر تاریخ
        date_range = st.date_input(
            "محدوده تاریخ",
            value=(
                df['تاریخ'].min().date(),
                df['تاریخ'].max().date()
            )
        )
        
        # فیلتر سطح ریسک
        risk_levels = ['همه'] + list(df['سطح_ریسک'].unique())
        selected_risk = st.selectbox("سطح ریسک", risk_levels)
        
        # فیلتر مرحله
        steps = ['همه'] + list(df['مرحله'].unique())
        selected_step = st.selectbox("مرحله", steps)
    
    # اعمال فیلترها
    mask = (df['تاریخ'].dt.date >= date_range[0]) & (df['تاریخ'].dt.date <= date_range[1])
    filtered_df = df[mask]
    
    if selected_risk != 'همه':
        filtered_df = filtered_df[filtered_df['سطح_ریسک'] == selected_risk]
    if selected_step != 'همه':
        filtered_df = filtered_df[filtered_df['مرحله'] == selected_step]
    
    if filtered_df.empty:
        st.warning("هیچ داده‌ای با فیلترهای انتخاب شده یافت نشد!")
        return
        
    # نمایش آمار کلی
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("تعداد کل ارزیابی‌ها", len(filtered_df))
    with col2:
        avg_score = filtered_df['امتیاز'].mean()
        st.metric("میانگین امتیاز", f"{avg_score:.2f}" if pd.notnull(avg_score) else "نامشخص")
    with col3:
        risk_counts = filtered_df['سطح_ریسک'].value_counts()
        most_common_risk = risk_counts.index[0] if not risk_counts.empty else "نامشخص"
        st.metric("رایج‌ترین سطح ریسک", most_common_risk)
    with col4:
        total_count = len(filtered_df)
        if total_count > 0:
            completed_count = len(filtered_df[filtered_df['مرحله'] == 'step-3'])
            completion_rate = (completed_count / total_count) * 100
            st.metric("نرخ تکمیل پرسشنامه", f"{completion_rate:.1f}%")
        else:
            st.metric("نرخ تکمیل پرسشنامه", "0%")
    
    # نمودارها
    if len(filtered_df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("توزیع سطوح ریسک")
            fig_risk = px.pie(filtered_df, names='سطح_ریسک', title="توزیع سطوح ریسک")
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            st.subheader("روند امتیازات در طول زمان")
            fig_trend = px.line(
                filtered_df, 
                x='تاریخ', 
                y='امتیاز',
                title="روند امتیازات"
            )
            st.plotly_chart(fig_trend, use_container_width=True)
    
        # نمایش داده‌های خام
        st.subheader("داده‌های خام")
        st.dataframe(
            filtered_df.drop(['پاسخ‌های_عددی', 'پاسخ‌های_متنی'], axis=1),
            hide_index=True
        )
        
        # امکان دانلود داده‌ها
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="دانلود داده‌ها (CSV)",
            data=csv,
            file_name="assessment_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
