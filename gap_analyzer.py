from api.llm_wrapper import call_groq

def suggest_improvements(resume_text, jd_text):
    prompt = f"""
You are a career coach. Analyze this resume and job description, and list top 5 improvements:

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    return call_groq(prompt)

def generate_resume_rewrite(resume_text, jd_text):
    prompt = f"""
Rewrite this resume summary to better match the job description:

Resume:
{resume_text}

Job:
{jd_text}
"""
    return call_groq(prompt)

def recommend_titles(resume_text):
    prompt = f"""
Suggest 5 most relevant job titles for this resume:

{resume_text}
"""
    return call_groq(prompt)

from utils.skill_matcher import extract_skills
import json

with open("data/skills_db.json") as f:
    SKILL_DB = set(json.load(f)['skills'])

def verify_suggestions_against_jd(suggestions_text, jd_text):
    jd_skills = extract_skills(jd_text)
    flagged = []
    for line in suggestions_text.split("\n"):
        for skill in SKILL_DB:
            if skill.lower() in line.lower() and skill.lower() not in [s.lower() for s in jd_skills]:
                flagged.append((skill, line))
    return flagged
