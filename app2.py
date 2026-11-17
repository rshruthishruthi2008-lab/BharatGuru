import streamlit as st
from PIL import Image

st.set_page_config(page_title="BharatGuru ROCKET 14.0 ULTIMATE", layout="centered")
st.title("🚀 BharatGuru ROCKET 14.0 ULTIMATE")
st.caption("All India Exams | All Indian Languages | UPSC to PUC | Google FREE")

has_google = "GOOGLE_API_KEY" in st.secrets
if not has_google:
    st.error("❌ GOOGLE_API_KEY missing in Secrets")
    st.stop()
st.success("✅ Google API Connected - FREE Unlimited")

# ALL INDIA EXAMS - 50+ EXAMS
all_exams = [
    # SCHOOL & PUC
    "PUC I & II Combined", "PUC I", "PUC II", "CBSE Class 11", "CBSE Class 12", "ICSE Class 11", "ICSE Class 12", "SSLC Class 10 Karnataka", "SSLC Class 10 CBSE",
    # DEGREE
    "Degree BCom", "Degree BBA", "Degree BCA", "Degree BA", "Degree BSc", "Degree BTech VTU", "Mangalore University", "Bangalore University",
    # UPSC - ALL
    "UPSC CSE - IAS/IPS", "UPSC CAPF", "UPSC CDS", "UPSC NDA", "UPSC EPFO", "UPSC CMS",
    # KPSC - ALL
    "KPSC KAS / Gazetted", "KPSC FDA / SDA", "KPSC PSI / PC", "KPSC PDO / VAO", "KPSC Group C",
    # RAILWAY - ALL
    "Railway RRB NTPC", "Railway RRB Group D", "Railway RRB JE", "Railway RRB ALP", "Railway RPF",
    # BANKING - ALL
    "Banking IBPS PO", "Banking IBPS Clerk", "Banking SBI PO", "Banking SBI Clerk", "Banking RBI Grade B", "Banking RBI Assistant", "Banking IBPS RRB PO/Clerk",
    # DEFENCE
    "NDA - National Defence Academy", "CDS - Combined Defence", "AFCAT", "Agniveer Army/Navy/Airforce",
    # ENTRANCE
    "KCET", "COMEDK", "JEE Mains + Advanced", "NEET", "CUET", "KEA CET", "CLAT", "CAT / MAT",
    # STATE & SSC
    "SSC CGL", "SSC CHSL", "SSC GD", "SSC MTS", "SSC CPO", "Karnataka TET / CET", "Police Constable / PSI"
]

# ALL INDIAN LANGUAGES - 22 OFFICIAL + HINGLISH
all_languages = [
    "English", "Hinglish (Hindi+English)", "Hindi", "Kannada",
    "Telugu", "Tamil", "Malayalam", "Marathi", "Gujarati", "Bengali",
    "Punjabi", "Urdu", "Odia", "Assamese", "Manipuri", "Konkani",
    "Sanskrit", "Rajasthani", "Bhojpuri", "Haryanvi", "Kashmiri", "Nepali"
]

subjects = ["General Studies", "Computer Science", "Accountancy", "Business Studies", "Economics", "History", "Geography", "Polity", "Science", "Maths", "Reasoning", "Current Affairs", "Karnataka GK"]

from_ = st.selectbox("🇮🇳 SELECT EXAM (50+ All India Exams)", all_exams, index=0)
subject = st.selectbox("Subject", subjects, index=0)
language = st.selectbox("🌐 Language (22 Indian Languages)", all_languages, index=0)
board = st.selectbox("Board / Commission", ["Karnataka State", "CBSE", "UPSC", "KPSC", "Railway RRB", "IBPS / SBI / RBI", "SSC", "NDA / Defence"], index=0)
syllabus = st.selectbox("Syllabus Year", ["New 2025-26", "Old 2024-25", "UPSC 2025 Pattern", "KPSC New Syllabus"], index=0)

doubt_text = st.text_area(f"Doubt for {from_}?", height=120, placeholder="Ex: Explain Article 32 for UPSC / Explain Arrays for PUC / Explain RRB NTPC Maths shortcut")
uploaded = st.file_uploader("Upload Photo Doubt (Question Paper / Book)", type=["jpg","jpeg","png"])

if st.button("🚀 ROCKET ANSWER - ULTIMATE", type="primary", use_container_width=True):
    if not doubt_text and not uploaded:
        st.warning("Write your doubt")
        st.stop()
    try:
        with st.spinner(f"Checking {from_} as per {board} {syllabus} in {language}..."):
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            You are BharatGuru ULTIMATE - Expert for ALL India competitive exams.
            
            Exam: {from_}
            Commission: {board}
            Syllabus: {syllabus}
            Subject: {subject}
            Language: {language}
            Doubt: {doubt_text}
            
            Answer Format for {from_}:
            1. EXAM PATTERN: {from_} syllabus point + page/source (UPSC - Laxmikant, KPSC - Karnataka textbook, etc)
            2. COMPARISON: How this topic asked in UPSC vs KPSC vs SSC vs Banking vs Railway vs NDA
            3. EXPLANATION: Simple + shortcut trick if {from_} is competitive (UPSC, KPSC, Railway, Banking, SSC, NDA)
            4. PYQ: Previous year question from {from_} - Year wise
            5. ANSWER IN: {language} - If Kannada selected, use Kannada + English terms. If Hindi, use Hindi.
            
            For UPSC: Use UPSC pattern - Article, Supreme Court cases.
            For KPSC: Use Karnataka state - KPSC FDA/SDA pattern + Kannada terms.
            For Railway: RRB NTPC shortcut + formula.
            For Banking: IBPS PO speed trick.
            For NDA: NDA Maths + GK trick.
            For PUC/CBSE: Board pattern with GST rules.
            """
            
            if uploaded:
                img = Image.open(uploaded)
                res = model.generate_content([prompt, img])
            else:
                res = model.generate_content(prompt)
            
            st.success(f"✅ {from_} Answer Ready - {board}")
            st.markdown(res.text)
            st.markdown("---")
            st.caption(f"{from_} | {board} | {syllabus} | {subject} | {language} | All India Exams")
            
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("If error, check GOOGLE_API_KEY in Secrets - Must start with AIza or AQ")

