import streamlit as st
from google import genai
import time

st.set_page_config(page_title="BharatGuru", layout="wide")

with st.sidebar:
    st.title("Settings")
    # Try to get key from Secrets first
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key loaded from Secrets ✅")
    else:
        api_key = st.text_input("Paste API Key Here", type="password")

    language = st.selectbox("Language", ["English", "Kannada", "Hindi"])
    exam = st.selectbox("Exam", ["UPSC", "KPSC", "SSC", "Banking"])

st.title("🇮🇳 BharatGuru - AI For All Exams")
query = st.text_area("Ask Any Doubt:", "what is the capital of India")

if st.button("Get Answer 🚀"):
    if not api_key:
        st.error("Paste API key in sidebar!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"You are BharatGuru for {exam}. Answer in {language}. Question: {query}"
            
            # FIX for 429 - Auto try 3 models
            for model_name in ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-2.0-flash"]:
                try:
                    response = client.models.generate_content(model=model_name, contents=prompt)
                    st.success(f"Answer from {model_name}:")
                    st.write(response.text)
                    break
                except Exception as e:
                    if "429" in str(e):
                        st.warning(f"{model_name} busy, trying next...")
                        time.sleep(1)
                        continue
                    else:
                        raise e
        except Exception as e:
            if "429" in str(e):
                st.error("🙏 High Traffic! Wait 30 seconds and try again - Quota will reset!")
            else:
                st.error(f"Error: {e}")
