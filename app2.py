import streamlit as st
from PIL import Image

st.set_page_config(page_title="BharatGuru ROCKET 12.3", layout="centered")
st.title("🚀 BharatGuru ROCKET 12.3")
st.caption("Google Free | Photo Doubt Supported")

has_google = "GOOGLE_API_KEY" in st.secrets

if not has_google:
    st.error("❌ GOOGLE_API_KEY missing in Secrets")
    st.info("Add GOOGLE_API_KEY = \"AQ....\" in share.streamlit.io -> Settings -> Secrets")
    st.stop()

st.success("✅ Google API Connected - FREE")

from_ = st.selectbox("From", ["PUC I & II", "PUC I", "PUC II", "Degree BCom", "Degree BBA"], index=0)
subject = st.selectbox("Subject", ["Computer Science", "Accountancy", "Business Studies", "Economics"], index=0)
language = st.selectbox("Language", ["English", "Kannada", "Hinglish"], index=0)
board = st.selectbox("Board", ["Karnataka State PUC", "CBSE", "Mangalore University"], index=0)
syllabus = st.selectbox("Syllabus", ["New 2025-26", "Old 2024-25"], index=0)

doubt_text = st.text_area("What is asking? Eg: Explain Journal", height=100)
uploaded = st.file_uploader("Upload Photo Doubt", type=["jpg","jpeg","png"])

if st.button("🚀 ROCKET ANSWER", type="primary", use_container_width=True):
    if not doubt_text and not uploaded:
        st.warning("Write doubt or upload photo")
        st.stop()
    try:
        with st.spinner(f"Checking {subject} as per {board} {syllabus}..."):
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            You are BharatGuru for {from_} {board} {syllabus}.
            Class: {from_}, Board: {board}, Syllabus: {syllabus}
            Subject: {subject}, Language: {language}
            Doubt: {doubt_text}
            
            Give:
            1. BOARD: {board} {syllabus} page number
            2. EXPLANATION as per {board} pattern
            3. DIFFERENCE vs other boards
            4. PYQ from {board}
            5. Summary in {language}
            
            If Karnataka PUC 11th: No GST, No Voucher.
            If Mangalore Univ BCom: WITH GST 18% CGST9%+SGST9%.
            If CBSE 2025-26: Voucher No compulsory.
            """
            
            if uploaded:
                img = Image.open(uploaded)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            st.success("✅ Answer Ready!")
            st.markdown(response.text)
            st.caption(f"As per {board} | {syllabus} | {subject}")
            
    except Exception as e:
        st.error(f"Error: {e}")
        st.code(str(e))

st.caption("Made by R.SHRUTHI- FOUNDER BHARAT GURU| Board + Syllabus Wise+Exam point of view.")