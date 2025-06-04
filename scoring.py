import textstat

def compute_resume_quality(resume_text):
    score = textstat.flesch_reading_ease(resume_text)
    if score > 70:
        return 9
    elif score > 50:
        return 7
    elif score > 30:
        return 5
    else:
        return 3