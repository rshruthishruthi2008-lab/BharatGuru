import streamlit as st
from google import genai
import time

st.set_page_config(page_title="BharatGuru", layout="wide")

with st.sidebar:
    st.title("Settings")
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key loaded ✅")
    else:
        api_key = st.text_input("Paste API Key Here", type="password")

    language = st.selectbox("Language", ["English", "Kannada", "Hindi"])
    exam = st.selectbox("Exam", ["UPSC", "KPSC", "SSC", "Banking"])

st.title("🇮🇳 BharatGuru - AI For All Exams")
query = st.text_area("Ask Any Doubt:", "define data type")

if st.button("Get Answer 🚀"):
    if not api_key:
        st.error("Add API Key in Secrets!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"You are BharatGuru for {exam}. Answer in {language}. Question: {query}"
            
            # NEW MODELS - Works in new SDK + High Quota
            models_list = ["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-flash"]
            
            for model_name in models_list:
                try:
                    st.toast(f"Trying {model_name}...")
                    response = client.models.generate_content(model=model_name, contents=prompt)
                    st.success(f"Answer from {model_name}:")
                    st.write(response.text)
                    break
                except Exception as e:
                    if "404" in str(e) or "429" in str(e):
                        time.sleep(1)
                        continue
                    else:
                        raise e
            else:
                st.error("All models busy! Wait 30 sec - Quota resets every minute!")

        except Exception as e:
            st.error(f"Error: {e}")
