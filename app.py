import streamlit as st
from youtube_comment_downloader import YoutubeCommentDownloader
import google.generativeai as genai
import itertools
import pandas as pd

# 1. تنسيق واجهة التطبيق (الجماليات)
st.set_page_config(page_title="رادار آراء منتجات العناية", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fff5f7; }
    .stButton>button { background: linear-gradient(to right, #ff4b2b, #ff416c); color: white; border-radius: 25px; border: none; height: 3em; font-weight: bold; }
    h1 { color: #ff416c; font-family: 'Arial'; text-align: center; }
    .status-box { padding: 20px; border-radius: 15px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ رادار تجارب منتجات العناية")
st.write("<h4 style='text-align: center; color: #666;'>استخلصي الحقيقة من التعليقات في ثوانٍ</h4>", unsafe_allow_html=True)

# 2. إعدادات الـ API (تأكدي أن المفتاح صحيح وبدون مسافات)
API_KEY = "AIzaSyAdU0ZkZe6fWgfiN7-Q9GteWSQ19gWsY3I" 
genai.configure(api_key=API_KEY)
try:
model = genai.GenerativeModel('gemini-1.5-flash')
except:
model = genai.GenerativeModel('gemini-pro')

# 3. واجهة المستخدم
video_url = st.text_input("🔗 ضعي رابط فيديو اليوتيوب هنا:", placeholder="https://youtube.com/watch?v=...")

if st.button("🚀 ابدأ التحليل العميق"):
    if not video_url:
        st.warning("الرجاء إدخال الرابط أولاً!")
    else:
        try:
            with st.spinner('جاري جمع آراء الناس...'):
                # سحب التعليقات
                downloader = YoutubeCommentDownloader()
                comments_iter = downloader.get_comments_from_url(video_url, sort_by=1)
                # سحب عدد قليل (20 تعليق) لتفادي الـ Timeout الذي حدث معكِ
                raw_comments = [c['text'] for c in itertools.islice(comments_iter, 20)]
                
                if not raw_comments:
                    st.error("تعذر العثور على تعليقات.")
                else:
                    # طلب التحليل من Gemini مع تحديد تنسيق واضح
                    prompt = f"""
                    حلل التعليقات التالية بلهجاتها العربية المختلفة. 
                    استخرج فقط الآراء الحقيقية في المنتج. 
                    صنفها لـ (إيجابي) و (سلبي). 
                    أعطني النتيجة كقائمة قصيرة جداً ومباشرة.
                    التعليقات: {raw_comments}
                    """
                    response = model.generate_content(prompt)
                    
                    # عرض النتائج بشكل احترافي
                    st.balloons()
                    st.markdown("### 📊 ملخص التحليل الذكي")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #ff416c;'>{response.text}</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.write("💡 **نصيحة التطبيق:**")
                        st.info("النتائج تعتمد على تحليل عينة من التعليقات باستخدام الذكاء الاصطناعي.")

        except Exception as e:
            st.error(f"حدثت مشكلة تقنية: {e}")
