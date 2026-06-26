import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are a strict, experienced technical recruiter at a top tech company.
    
    Carefully analyze how well this resume matches the job description.
    Be VERY precise and harsh with scoring. Most resumes score between 20-75.
    Only give 80+ if the resume is an almost perfect match.
    Give 20-40 if key skills are missing.
    Give 40-65 if some skills match but gaps exist.
    Give 65-80 if most skills match with minor gaps.
    
    Count the exact number of required skills from the job description,
    then count how many appear in the resume. Base your score on this ratio.
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME:
    {resume_text}
    
    Respond in EXACTLY this format with no extra text:

    MATCH SCORE: [single number 0-100 based strictly on skill overlap]

    STRENGTHS:
    - [specific strength 1 with evidence from resume]
    - [specific strength 2 with evidence from resume]
    - [specific strength 3 with evidence from resume]

    MISSING KEYWORDS:
    - [exact skill/keyword from job description missing in resume]
    - [exact skill/keyword from job description missing in resume]
    - [exact skill/keyword from job description missing in resume]

    SUGGESTIONS:
    - [specific actionable suggestion 1]
    - [specific actionable suggestion 2]
    - [specific actionable suggestion 3]

    SUMMARY:
    [2 sentences: first sentence states the match percentage and main reason, second gives the most important improvement needed]
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.3
    )

    return response.choices[0].message.content
