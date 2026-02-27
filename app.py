import streamlit as st
import google.generativeai as genai
from youtube_comment_downloader import YoutubeCommentDownloader
import itertools

# إعداد واجهة التطبيق
st.set_page_config(page_title="رادار الجمال", page_icon="✨")
st.title("✨ رادار تجارب منتجات العناية")

# جلب المفتاح بأمان من Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)

    with st.expander("فحص الموديلات المتاحة (List Models)"):
     try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.write(f"✅ متاح: `{m.name}`")
     except Exception as e:
        st.error(f"حدث خطأ أثناء فحص الموديلات: {e}")

    # استخدام الموديل المستقر
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("لم يتم العثور على مفتاح API في الإعدادات السرية.")
    st.stop()

video_url = st.text_input("🔗 رابط فيديو اليوتيوب:")

if st.button("🚀 ابدأ التحليل"):
    if video_url:
        try:
            with st.spinner('جاري التحليل...'):
                downloader = YoutubeCommentDownloader()
                comments_iter = downloader.get_comments_from_url(video_url, sort_by=1)
                # سحب 10 تعليقات
                raw_comments = [c['text'] for c in itertools.islice(comments_iter, 10)]
                
                if raw_comments:
                    prompt = f"حلل هذه التعليقات باختصار (إيجابي/سلبي): {raw_comments}"
                    response = model.generate_content(prompt)
                    st.success("أخيراً! التطبيق يعمل بنجاح.")
                    st.markdown(f"### النتيجة:\n{response.text}")
                else:
                    st.warning("لا توجد تعليقات.")
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
