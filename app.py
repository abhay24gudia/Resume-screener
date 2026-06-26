import streamlit as st
from screener import analyze_resume
import re
import time
import threading
import fitz  # pymupdf

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stApp { background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%); }
    .title { 
        text-align: center; 
        font-size: 3rem; 
        font-weight: 800;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .score-box {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .score-number {
        font-size: 5rem;
        font-weight: 900;
        color: white;
    }
    .score-label {
        color: #e2e8f0;
        font-size: 1.2rem;
    }
    .section-box {
        background: #1e2530;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #6366f1;
    }
    .strength-box {
        background: #0f2417;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #22c55e;
    }
    .missing-box {
        background: #2a1a1a;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ef4444;
    }
    .suggestion-box {
        background: #1a1f0f;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #f59e0b;
    }
    .loading-box {
        background: #1e2530;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #334155;
    }
    .upload-box {
        background: #1e2530;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px dashed #6366f1;
        text-align: center;
    }
    .stTextArea textarea {
        background-color: #1e2530 !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="title">📄 AI Resume Screener</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your resume or paste text to get an instant AI-powered match analysis</p>', unsafe_allow_html=True)

# Input columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💼 Job Description")
    job_description = st.text_area(
        "job",
        height=300,
        placeholder="Paste the job posting here...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 📝 Your Resume")
    
    # Toggle between upload and paste
    input_method = st.radio(
        "Input method",
        ["📤 Upload PDF", "✏️ Paste Text"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    resume_text = ""
    
    if input_method == "📤 Upload PDF":
        uploaded_file = st.file_uploader(
            "Upload your resume PDF",
            type=["pdf"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            # Extract text from PDF
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            resume_text = ""
            for page in doc:
                resume_text += page.get_text()
            st.success(f"✅ PDF uploaded! ({len(resume_text)} characters extracted)")
    else:
        resume_text = st.text_area(
            "resume",
            height=250,
            placeholder="Paste your resume text here...",
            label_visibility="collapsed"
        )

# Analyze button
col_btn = st.columns([1,2,1])[1]
with col_btn:
    analyze = st.button("🔍 Analyze My Resume")

if analyze:
    if not job_description or not resume_text:
        st.warning("⚠️ Please fill in both fields first.")
    else:
        # Animated loading screen
        loading_messages = [
            ("🔍", "Reading your resume..."),
            ("💼", "Scanning the job description..."),
            ("🧠", "AI is thinking hard..."),
            ("📊", "Calculating your match score..."),
            ("✨", "Polishing the results..."),
        ]

        loading_placeholder = st.empty()

        def show_loading(emoji, message):
            loading_placeholder.markdown(f"""
            <div class="loading-box">
                <div style="font-size: 3rem">{emoji}</div>
                <div style="color: #e2e8f0; font-size: 1.3rem; margin-top: 1rem">{message}</div>
            </div>
            """, unsafe_allow_html=True)

        result_container = [None]
        done_flag = [False]

        def fetch_result():
            result_container[0] = analyze_resume(resume_text, job_description)
            done_flag[0] = True

        thread = threading.Thread(target=fetch_result)
        thread.start()

        i = 0
        while not done_flag[0]:
            emoji, msg = loading_messages[i % len(loading_messages)]
            show_loading(emoji, msg)
            time.sleep(0.8)
            i += 1

        loading_placeholder.empty()
        result = result_container[0]

        # Extract score
        score_match = re.search(r'MATCH SCORE:\s*(\d+)', result)
        score = int(score_match.group(1)) if score_match else 0

        # Score display
        st.markdown("---")
        col_score = st.columns([1,1,1])[1]
        with col_score:
            color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
            st.markdown(f"""
            <div class="score-box">
                <div class="score-number" style="color:{color}">{score}</div>
                <div class="score-label">Match Score out of 100</div>
            </div>
            """, unsafe_allow_html=True)

        # Progress bar
        st.progress(score/100)

        # Parse and display sections
        sections = {
            "STRENGTHS": ("strength-box", "✅ Strengths", "#22c55e"),
            "MISSING KEYWORDS": ("missing-box", "❌ Missing Keywords", "#ef4444"),
            "SUGGESTIONS": ("suggestion-box", "💡 Suggestions", "#f59e0b"),
            "SUMMARY": ("section-box", "📋 Summary", "#6366f1"),
        }

        for key, (box_class, title, color) in sections.items():
            pattern = rf'{key}:(.*?)(?=\n[A-Z]|\Z)'
            match = re.search(pattern, result, re.DOTALL)
            if match:
                content = match.group(1).strip()
                st.markdown(f"""
                <div class="{box_class}">
                    <h3 style="color:{color}; margin-top:0">{title}</h3>
                    <p style="color:#e2e8f0; white-space: pre-line">{content}</p>
                </div>
                """, unsafe_allow_html=True)
