from sentence_transformers import SentenceTransformer, util
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('data/skills_db.json') as f:
    SKILL_DB = set(json.load(f)['skills'])

def extract_skills(text):
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="ignore")
    return list(set([skill for skill in SKILL_DB if skill.lower() in text.lower()]))


def compute_match_score(resume_skills, jd_skills):
    resume_vec = model.encode(" ".join(resume_skills), convert_to_tensor=True)
    jd_vec = model.encode(" ".join(jd_skills), convert_to_tensor=True)
    score = util.cos_sim(resume_vec, jd_vec).item() * 100
    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))
    return score, matched, missing
