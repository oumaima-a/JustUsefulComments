import streamlit as st
import os
from youtube_comment_downloader import YoutubeCommentDownloader
import google.generativeai as genai
import itertools

# إعدادات الواجهة
st.set_page_config(page_title="رادار الجمال", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #fff5f7; direction: rtl; }
    .stButton>button { background: #ff416c; color: white; width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ رادار تجارب منتجات العناية")

# إعداد الـ API
# نصيحة: تأكدي أن المفتاح ليس به أي فراغات
API_KEY = "AIzaSyAdU0ZkZe6fWgfiN7-Q9GteWSQ19gWsY3I" 
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"]="never"
genai.configure(api_key=API_KEY)

# استخدام الموديل الأقدم والأكثر استقراراً لتجنب خطأ 404
model = genai.GenerativeModel(model_name='gemini-pro')

video_url = st.text_input("🔗 رابط فيديو اليوتيوب:")

if st.button("🚀 تحليل الآن"):
    if video_url:
        try:
            with st.spinner('جاري التحليل...'):
                # سحب 10 تعليقات فقط لضمان عدم حدوث Timeout
                downloader = YoutubeCommentDownloader()
                comments_iter = downloader.get_comments_from_url(video_url, sort_by=1)
                raw_comments = [c['text'] for c in itertools.islice(comments_iter, 10)]
                
                if not raw_comments:
                    st.error("لم يتم العثور على تعليقات.")
                else:
                    # صياغة أمر بسيط جداً لتقليل الضغط على السيرفر
                    text_to_analyze = "\n".join(raw_comments)
                    prompt = f"حلل هذه التعليقات لمنتج تجميل. استخرج الآراء (إيجابي/سلبي) باختصار باللغة العربية:\n{text_to_analyze}"
                    
                    response = model.generate_content(prompt)
                    
                    st.success("تم التحليل بنجاح!")
                    st.markdown("### النتائج:")
                    st.write(response.text)
                    
        except Exception as e:
            # إذا ظهر خطأ، سنعرضه هنا لنعرف السبب الحقيقي
            st.error(f"عذراً، حدث خطأ: {str(e)}")
    else:
        st.warning("يرجى إدخال الرابط.")
