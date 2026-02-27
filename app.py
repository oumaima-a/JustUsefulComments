import streamlit as st
from youtube_comment_downloader import YoutubeCommentDownloader
import google.generativeai as genai
import itertools

# إعداد واجهة التطبيق
st.set_page_config(page_title="محلل تجارب العناية", layout="wide")
st.title("🧴 محلل آراء منتجات العناية بالبشرة")
st.write("ضع رابط فيديو مراجعة لمنتج، وسأقوم باستخراج التجارب الحقيقية فقط (باللهجات العربية).")

# إعداد الجانب الجانبي لوضع المفتاح (أو وضعه مباشرة في الكود)
api_key = "ضعي_مفتاح_API_الخاص_بكِ_هنا" 

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    video_url = st.text_input("رابط فيديو يوتيوب:")

    if st.button("تحليل التعليقات"):
        if video_url:
            with st.spinner('جاري سحب وتحليل التعليقات...'):
                # 1. سحب التعليقات
                downloader = YoutubeCommentDownloader()
                comments_iter = downloader.get_comments_from_url(video_url, sort_by=1)
                comments = [c['text'] for c in itertools.islice(comments_iter, 40)] # سحب 40 تعليق للتجربة
                
                if comments:
                    # 2. إرسالها لـ Gemini
                    prompt = f"حلل هذه التعليقات العربية (مغربي، مصري، خليجي). استخرج فقط التي تحكي تجربة شخصية مع المنتج. صنفه (إيجابي أو سلبي). تجاهل الأسئلة عن السعر أو السلام. التعليقات: {comments}"
                    response = model.generate_content(prompt)
                    
                    st.subheader("النتائج:")
                    st.write(response.text)
                else:
                    st.error("لم أجد تعليقات في هذا الفيديو.")
        else:
            st.warning("الرجاء وضع رابط الفيديو.")
