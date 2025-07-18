import streamlit as st
from sentence_transformers import SentenceTransformer
import re
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF
from streamlit import file_uploader, text_area, button, write, markdown
from streamlit import set_page_config

# Set up the Streamlit app configuration
@st.cache_resource
def load_sbert_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

sbert_model = load_sbert_model()

def text_normalize(text):
    """Normalize text by converting to lowercase and removing non-alphanumeric characters."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


# ----------------- Define skills ------------------- #
SKILLS =[
    "python", "pandas", "scikit-learn", "aws", "flask", "machine learning", 
    "nlp", "data analysis", "xgboost", "tensorflow", "keras", "rest api"
]

def extract_skills(text):
    """Extract skills from the text based on predefined skills list."""
    text = text_normalize(text)
    found = set()
    for skill in SKILLS:
        skill_clean = skill.lower().replace("-", " ")
        if skill_clean in text:
            found.add(skill_clean)

    return found


# ----------- Semantic Similarity Score ------------ #

def semantic_similarity(resume_text, job_text):
    """Calculate semantic similarity between resume and job description."""
    resume_embeddings = sbert_model.encode([resume_text])[0]
    job_embeddings = sbert_model.encode([job_text])[0]
    similarity = cosine_similarity([resume_embeddings], [job_embeddings])[0][0]

    return round(similarity, 2)

# ------------- Keyword Match Score ---------------- #

def extract_keywords(resume_text, job_text):
    """Extract keywords from resume and job description."""
    resume_text = text_normalize(resume_text)
    job_text = text_normalize(job_text)

    resume_keywords = set(resume_text.split())
    job_keywords = set(job_text.split())

    common_keywords = resume_keywords.intersection(job_keywords)
    total_keywords = len(job_keywords)

    if total_keywords == 0:
        return 0.0

    keyword_match_score = len(common_keywords) / total_keywords
    return round(keyword_match_score, 2)

# ----------------- Experience Extraction ----------------- #
def extract_experience(text):
    """Extract years of experience from the text."""
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    years = [int(y) for y in years]
    
    if len(years) >= 2:
        start = min(years)
        end = max(years)
        experience = max(0, end - start)
        return experience
    else:
        return 0

# ----------------- Final Resume Score ----------------- #
def final_resume_score(resume_text, job_text):
    """Calculate the final resume score based on semantic similarity, keyword match, and experience."""
    semantic_score = semantic_similarity(resume_text, job_text)
    keyword_score = extract_keywords(resume_text, job_text)
    experience_years = extract_experience(resume_text)

    # Combine scores with weights
    final_score = (semantic_score * 0.5) + (keyword_score * 0.3) + (experience_years * 0.2 / 10)  # Normalize experience to a scale of 0-1
    
    return {
        "semantic": semantic_score,
        "keyword": keyword_score,
        "final": round(final_score * 100, 2)
    }

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(stream=uploaded_resume.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ----------------- Streamlit App ----------------- 

st.title("Smart Resume Screener")
st.markdown("Compare your resume (PDF) with a job description and get a match score.")

st.write("Upload your resume and job description to get a match score.") 

uploaded_resume = st.file_uploader("📤 Upload Resume (PDF)", type="pdf")
job_text = st.text_area("💼 Paste Job Description Here", height=250)

if st.button("🔍 Analyze Resume"):
    if uploaded_resume is None or job_text.strip() == "":
       st.warning("Please upload a resume PDF and enter the job description.")

    else:
        resume_text = extract_text_from_pdf(uploaded_resume)

        result = final_resume_score(resume_text, job_text)

        st.markdown("### Match Results")
        st.write(f"**Semantic Similarity Score:** {result['semantic']}")
        st.write(f"**Keyword Match Score:** {result['keyword']}")
        st.write(f"**Years of Experience:** {extract_experience(resume_text)}")
        st.write(f"**Final Match Score:** {result['final']}%")
        if result['final'] >= 80:
            st.success("✅ Strong Match")
        elif 50 <= result['final'] < 80:
            st.warning("⚠️ Moderate Fit")
        else:
            st.error("❌ Weak Match")
