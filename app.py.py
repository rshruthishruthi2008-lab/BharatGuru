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
    exam = st.selectbox("Exam", ["UPSC", "KPSC", "SSC", "Banking", "CET"])

# FIXED TITLE - No IN now!
st.title("BharatGuru - AI For All Exams 🎓")
st.markdown("Your personal AI teacher for competitive exams")

query = st.text_area("Ask Any Doubt:", "define data type", height=150)

if st.button("Get Answer 🚀", type="primary"):
    if not api_key:
        st.error("Please add API Key in Streamlit Secrets!")
    else:
        with st.spinner("BharatGuru is thinking..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"You are BharatGuru expert for {exam}. Answer clearly in {language}. Question: {query}"
                
                # Models with high quota - Best for free tier
                models_list = ["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-flash"]
                answered = False
                
                for model_name in models_list:
                    try:
                        response = client.models.generate_content(
                            model=model_name, 
                            contents=prompt
                        )
                        st.success(f"Answer (from {model_name}):")
                        st.write(response.text)
                        answered = True
                        break
                    except Exception as e:
                        err = str(e)
                        if "404" in err or "429" in err or "quota" in err.lower():
                            time.sleep(1)
                            continue
                        else:
                            st.error(f"Error: {err}")
                            break
                
                if not answered:
                    st.warning("⏳ All models busy! Google free quota resets every 60 seconds. Please wait 1 minute and try again!")
                    st.info("Tip for IPR: Free tier = 50 requests/day. Add 2nd API key for 100/day.")

            except Exception as e:
                st.error(f"Error: {e}")
