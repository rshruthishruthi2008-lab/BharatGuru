import streamlit as st
from google import genai
from gtts import gTTS
import os

# >>> PASTE YOUR AQ KEY HERE <<<
API_KEY = "AQ.Ab8RN6LsTuyum09IfrkE9xb3wgf0wFqA022CcDlqWiIg3F1u4w"

st.set_page_config(page_title="BharatGuru 2.0")
st.title("BharatGuru 2.0 - app2")
st.caption("Class 10,12 | NDA | UPSC | KPSC | JEE | KCET | Railway | Banking | All Indian Languages + Voice")

lang = st.selectbox("Language", ["Kannada","Hindi","English","Tamil","Telugu","Malayalam","Marathi","Gujarati","Bengali","Punjabi","Odia","Hinglish"])
exam = st.selectbox("Exam", ["Class 10","Class 12","NDA","UPSC","KPSC","JEE","KCET","Railway","Banking"])
sub = st.selectbox("Subject", ["Maths","Science","GK","All"])

voice_map = {"Kannada":"kn","Hindi":"hi","English":"en","Tamil":"ta","Telugu":"te","Malayalam":"ml","Marathi":"mr","Gujarati":"gu","Bengali":"bn","Punjabi":"pa","Odia":"or","Hinglish":"hi"}

q = st.text_input(f"Ask {exam} Doubt in {lang} (Ex: calculus formula sheet)")

if st.button("Get Answer + Voice"):
    if not q:
        st.warning("Type question first!")
    else:
        try:
            client = genai.Client(api_key=API_KEY)
            prompt = f"You are BharatGuru. Answer in {lang} for {exam} {sub} student. Question: {q}"
            response = client.models.generate_content(model="gemini-3.5-flash-lite", contents=prompt)
            ans = response.text
            st.success(ans)
            # Voice
            tts = gTTS(text=ans[:4000], lang=voice_map.get(lang,"en"))
            tts.save("ans.mp3")
            st.audio("ans.mp3")
        except Exception as e:
            st.error(f"Error: {e}")