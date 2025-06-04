import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
assert GROQ_API_KEY, "GROQ_API_KEY not found in environment variables!"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def call_groq(prompt, model="llama3-8b-8192", temperature=0.5):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert AI resume assistant. Only use information explicitly found in the input. Do not guess, hallucinate, or invent new skills or experiences. Provide actionable, honest, and concise suggestions based on exact resume and JD text."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload)
        res.raise_for_status()
        res_json = res.json()

        if 'choices' in res_json and len(res_json['choices']) > 0:
            return res_json['choices'][0]['message']['content']
        else:
            print("⚠️ Unexpected Groq API response:", res_json)
            return "❌ Groq API returned an unexpected format. Please try again later."

    except requests.exceptions.RequestException as e:
        print("❌ HTTP error from Groq:", e)
        return "❌ Error connecting to Groq API. Please check your API key or network."

    except Exception as e:
        print("❌ Exception parsing Groq response:", e)
        return "❌ Unexpected error while processing Groq API response."


def get_gap_suggestions(resume, jd):
    prompt = f"""
You are a resume optimization assistant.

TASK:
Compare the resume and job description below. Only use explicitly stated skills or content. Do NOT suggest skills or tools that are not mentioned in the JD.

Return exactly 5 clear, numbered, actionable suggestions to improve the resume **only if the resume lacks content that is present in the JD**.

Resume:
\"\"\"
{resume}
\"\"\"

Job Description:
\"\"\"
{jd}
\"\"\"
"""
    return call_groq(prompt)
