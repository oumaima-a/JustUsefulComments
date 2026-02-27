import streamlit as st
import google.generativeai as genai
from youtube_comment_downloader import YoutubeCommentDownloader
import itertools

# إعداد واجهة التطبيق
st.set_page_config(page_title="رادار تجارب منتجات العناية", page_icon="✨")
st.title("✨ رادار تجارب منتجات العناية")

# 1. إعداد الـ API
API_KEY = "AIzaSyAdU0ZkZe6fWgfiN7-Q9GteWSQ19gWsY3I"
genai.configure(api_key=API_KEY)

# 2. عرض الموديلات المتاحة (للتأكد من الاسم الصحيح)
with st.expander("فحص الموديلات المتاحة (List Models)"):
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.write(f"✅ متاح: `{m.name}`")
    except Exception as e:
        st.error(f"حدث خطأ أثناء فحص الموديلات: {e}")

# 3. اختيار الموديل (استخدام الاسم الكامل كما يظهر في القائمة)
# غالباً سيكون: models/gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

video_url = st.text_input("🔗 رابط فيديو اليوتيوب:")

if st.button("🚀 ابدأ التحليل"):
    if video_url:
        try:
            with st.spinner('جاري التحليل...'):
                downloader = YoutubeCommentDownloader()
                comments_iter = downloader.get_comments_from_url(video_url, sort_by=1)
                raw_comments = [c['text'] for c in itertools.islice(comments_iter, 5)]
                
                if raw_comments:
                    # نرسل النص مباشرة بدون تعقيدات البرومبت الطويلة حالياً
                    response = model.generate_content(f"حلل هذه الآراء باختصار: {raw_comments}")
                    st.success("تم الاتصال بنجاح!")
                    st.write(response.text)
                else:
                    st.warning("لم يتم العثور على تعليقات.")
        except Exception as e:
            st.error(f"خطأ تقني: {str(e)}")
