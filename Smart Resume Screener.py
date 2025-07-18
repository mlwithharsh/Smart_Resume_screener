import re
import torch
import fitz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
print(fitz.__doc__)

def extract_file(file_path):
    docs = fitz.open(file_path)
    text = ""
    for page in docs:
        text += page.get_text()
        return text

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def semantics(resume_text,job_text):
    resume_embeddings = sbert_model.encode([resume_text])[0]
    job_embeddings = sbert_model.encode([job_text])[0]
    similarity = cosine_similarity([resume_embeddings], [job_embeddings])[0][0]

    return round(similarity , 2)

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


SKILLS = [
"python", "pandas", "scikit-learn", "aws", "flask", "machine learning", "nlp",
    "data analysis", "xgboost", "tensorflow", "keras", "rest api"
]

def skills(text):
    text = normalize(text)
    found = set()
    for skill in SKILLS:
        skill_clean = skill.lower().replace("-", " ")
        if skill in text:
            found.add(skill_clean)

    return found

def extract_experience(text):
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    years = [ int(y) for y in years ]
    if len(years) >= 2 :
        start = min(years)
        end = max(years)
        experience = max(0,end- start)

        print("Extracted Years:", years)
        print("📅 Experience:", experience, "years")

        return experience
    else:
        print("Extracted Years:", years)
        print("📅 Experience: 0 years")
        return 0

def extract_keywords(resume_text , job_text):
    resume_text = resume_text.lower()
    job_text = job_text.lower()
    resume_skills = resume_text.split()
    job_skills = job_text.split()
    match = len(set(resume_skills) & set(job_skills))
    total = len(job_skills)

    return round(match/total , 2 ) if total > 0 else 0

def final_resume_score(resume_text, job_text):
    semantic = semantics(resume_text, job_text)
    keywords = extract_keywords(resume_text, job_text)
    resume_skills = skills(resume_text)
    job_skills = skills(job_text)

    print("Debug:")
    print("Matched Words:", set(normalize(resume_text).split()) & set(normalize(job_text).split()))

    experience = extract_experience(resume_text)


    final = 0.6*semantic + 0.4*keywords
    final_percent = final*100


    if final_percent >= 80:
        level = "✅ Strong Match"
    elif 50 <= final_percent < 80:
        level = "⚠️ Moderate Fit"
    else:
        level = "❌ Weak Match"

    return {
        'semantic_score': round(semantic,2),
        'keyword_match_score': round(keywords,2),
        'experience_years': experience,
        'match_level': level,
        "matched_skills": resume_skills & job_skills,
        'final_percent': final_percent,
    }


resume = """ """

job_desc = """ """


result = final_resume_score(resume, job_desc)

print("📊 Semantic Similarity:", result['semantic_score'])
print("📄 Keyword Match:", result['keyword_match_score'])
print("🎯 Final Resume Match Score:", result['final_percent'], "%")
print(" Match Level:", result['match_level'])
print("📅 Experience:", result['experience_years'], "years")
print(" Matched Skills:", result['matched_skills'])
