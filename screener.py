import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an expert recruiter and career coach.
    
    Analyze how well this resume matches the job description below.
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME:
    {resume_text}
    
    Provide your analysis in exactly this format:
    
    MATCH SCORE: [0-100]
    
    STRENGTHS:
    - [list 3 things the resume does well for this role]
    
    MISSING KEYWORDS:
    - [list important skills/keywords from the job description not in the resume]
    
    SUGGESTIONS:
    - [list 3 specific improvements the candidate should make]
    
    SUMMARY:
    [2-sentence overall assessment]
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    return response.choices[0].message.content
