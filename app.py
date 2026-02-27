import streamlit as st
import google.generativeai as genai
from youtube_comment_downloader import YoutubeCommentDownloader
import itertools


API_KEY = "AIzaSyAdU0ZkZe6fWgfiN7-Q9GteWSQ19gWsY3I" 
genai.configure(api_key=API_KEY,transport='rest')
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. تصميم الواجهة
st.set_page_config(page_title="رادار تجارب منتجات العناية", page_icon="✨")
st.title("✨ رادار تجارب منتجات العناية")

video_url = st.text_input("🔗 ضعي رابط فيديو اليوتيوب هنا:")

if st.button("🚀 تحليل التجارب"):
    if video_url:
        try:
            with st.spinner('جاري قراءة التعليقات...'):
                # سحب عدد بسيط لضمان السرعة
                downloader = YoutubeCommentDownloader()
                comments_iter = downloader.get_comments_from_url(video_url, sort_by=1)
                raw_comments = [c['text'] for c in itertools.islice(comments_iter, 10)]
                
                if not raw_comments:
                    st.error("لم أجد تعليقات في هذا الفيديو.")
                else:
                    # إرسال التعليقات للموديل الذي نجح في الاختبار
                    prompt = f"حلل هذه التعليقات. استخرج باختصار التجارب الإيجابية والسلبية فقط:\n{raw_comments}"
                    response = model.generate_content(prompt)
                    
                    st.balloons()
                    st.success("تم التحليل بنجاح!")
                    st.markdown("### 📝 ملخص التجارب:")
                    st.write(response.text)
        except Exception as e:
            st.error(f"حدث خطأ بسيط: {str(e)}")
    else:
        st.warning("الرجاء إدخال الرابط.")
