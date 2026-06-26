import streamlit as st
from screener import analyze_resume

st.set_page_config(page_title="AI Resume Screener", page_icon="📄")

st.title("📄 AI Resume Screener")
st.write("Paste a job description and your resume to see how well you match.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the job posting here",
        height=300,
        placeholder="e.g. We are looking for a Machine Learning Engineer..."
    )

with col2:
    st.subheader("Your Resume")
    resume_text = st.text_area(
        "Paste your resume text here",
        height=300,
        placeholder="e.g. John Doe | john@email.com | Skills: Python, SQL..."
    )

if st.button("🔍 Analyze Match", type="primary"):
    if not job_description or not resume_text:
        st.warning("Please fill in both fields first.")
    else:
        with st.spinner("Analyzing your resume..."):
            result = analyze_resume(resume_text, job_description)
        
        st.success("Analysis complete!")
        st.markdown("---")
        st.markdown(result)
