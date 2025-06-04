import streamlit as st
from utils.skill_matcher import extract_skills, compute_match_score
from utils.gap_analyzer import suggest_improvements, generate_resume_rewrite, recommend_titles
from api.llm_wrapper import get_gap_suggestions
from api.scoring import compute_resume_quality
from PyPDF2 import PdfReader  # For PDF text extraction

st.set_page_config(page_title="AI Resume Matcher (Groq)", layout="wide")
st.title("Smart Resume Matcher + Optimizer (Groq LLM)")

uploaded_resume = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
uploaded_jd = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

if uploaded_resume and uploaded_jd:
    if uploaded_resume.name.endswith(".txt"):
        resume_text = uploaded_resume.read().decode("utf-8", errors="ignore")
    elif uploaded_resume.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_resume)
    else:
        st.error("Unsupported resume file format")
        st.stop()

    jd_text = uploaded_jd.read().decode("utf-8", errors="ignore")

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    match_score, matched, missing = compute_match_score(resume_skills, jd_skills)

    st.subheader(" Extracted Skills")
    st.write(f"**Resume Skills:** {resume_skills}")
    st.write(f"**JD Skills:** {jd_skills}")

    st.subheader("Skill Matching")
    st.metric("Match Score", f"{match_score:.2f}%")
    st.write(f"**Matched Skills:** {matched}")
    st.write(f"**Missing Skills:** {missing}")

    st.subheader("Resume Quality Score")
    quality_score = compute_resume_quality(resume_text)
    st.write(f"**Quality Score:** {quality_score}/10")

    st.subheader("Gap Suggestions (Groq LLM)")
    suggestions = get_gap_suggestions(resume_text, jd_text)
    st.write(suggestions)

    st.subheader("Resume Rewrite Suggestions (Groq LLM)")
    rewrite = generate_resume_rewrite(resume_text, jd_text)
    st.code(rewrite)

    st.subheader("Recommended Job Titles")
    titles = recommend_titles(resume_text)
    st.write(titles)
