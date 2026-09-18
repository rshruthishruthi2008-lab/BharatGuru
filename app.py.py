import streamlit as st
from google import genai

st.set_page_config(page_title="BharatGuru", layout="wide")

with st.sidebar:
    st.title("Settings")
    # Get key from Secrets first
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key loaded from Secrets ✅")
    else:
        api_key = st.text_input("Paste API Key Here", type="password")
    
    language = st.selectbox("Language", ["English", "Kannada", "Hindi"])
    exam = st.selectbox("Exam", ["UPSC", "KPSC", "SSC", "Banking"])

st.title("🎓 BharatGuru - AI For All Exams")
query = st.text_area("Ask Any Doubt:", "what is the capital of india and where it is located")

if st.button("Get Answer 🚀"):
    if not api_key:
        st.error("Paste API key in sidebar!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"You are BharatGuru, expert for {exam} exam. Answer in {language} language. Question: {query}. Give detailed exam-oriented answer."
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            st.success(response.text)
        except Exception as e:
            st.error(f"Error: {e}. Try again after 30 sec if model overloaded.")
