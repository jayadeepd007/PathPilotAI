from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import faiss
import numpy as np
from collections import Counter
import fitz  # PyMuPDF for PDFs
import pytesseract
from PIL import Image
import io

# HuggingFace for NER
from transformers import pipeline
# SentenceTransformers for embeddings
from sentence_transformers import SentenceTransformer

# ------------------------------
# FastAPI Setup
# ------------------------------
app = FastAPI()

origins = [
    "http://localhost:5173",  # React/Vite frontend
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Data Models
# ------------------------------
class JDRequest(BaseModel):
    job_description: str

# ------------------------------
# Load Models
# ------------------------------
print("🔄 Loading NLP models...")
skill_extractor = pipeline("ner", model="dslim/bert-base-NER")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Models loaded!")

# ------------------------------
# Known Skills
# ------------------------------
COMMON_SKILLS = [
    "python", "machine learning", "deep learning", "sql", "react",
    "javascript", "c++", "java", "aws", "docker", "pytorch", "tensorflow",
    "statistics", "data analysis", "html", "css", "communication"
]

# ------------------------------
# Dummy Candidate Database
# ------------------------------
candidate_resumes = {
    "Alice": "Python, Machine Learning, Data Analysis, TensorFlow",
    "Bob": "JavaScript, React, HTML, CSS",
    "Charlie": "Java, Algorithms, Data Structures, Spring",
    "Diana": "C++, Deep Learning, PyTorch, Computer Vision",
    "Ethan": "Excel, Communication, Statistics, SQL"
}

candidate_names = list(candidate_resumes.keys())
resume_embeddings = embedder.encode(list(candidate_resumes.values())).astype("float32")

# FAISS index
resume_index = faiss.IndexFlatL2(resume_embeddings.shape[1])
resume_index.add(resume_embeddings)

# ------------------------------
# Utils
# ------------------------------
def extract_skills(text: str):
    """Extract skills using NER + keyword matching"""
    entities = skill_extractor(text)
    ner_skills = [e['word'] for e in entities]
    keyword_skills = [skill for skill in COMMON_SKILLS if skill.lower() in text.lower()]
    return list(set(ner_skills + keyword_skills))

def embed_skills(skills: List[str]):
    if not skills:
        return np.zeros((1, 384), dtype="float32")  # MiniLM dimension
    text = " ".join(skills)
    return embedder.encode([text]).astype("float32")

def cosine_similarity(a, b):
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

# ------------------------------
# Routes
# ------------------------------
@app.get("/")
def home():
    return {"message": "🚀 PathPilot.AI Backend is running!"}

@app.post("/match_job_description")
def match_jd(data: JDRequest):
    jd_skills = extract_skills(data.job_description)
    jd_embedding = embed_skills(jd_skills)
    D, I = resume_index.search(jd_embedding, 5)

    matches = []
    all_missing = []

    for rank, idx in enumerate(I[0]):
        candidate = candidate_names[idx]
        dist = float(D[0][rank])
        sim = cosine_similarity(jd_embedding, resume_embeddings[idx:idx+1])
        fit_score = round(float(sim * 100), 2)

        candidate_skills = [s.strip() for s in candidate_resumes[candidate].split(",")]
        missing = [s for s in jd_skills if s not in candidate_skills]
        all_missing.extend(missing)

        matches.append({
            "name": candidate,
            "distance": dist,
            "fit_score": fit_score,
            "missing_skills": missing
        })

    top_missing_skills = Counter(all_missing).most_common(5)

    return {
        "skills_extracted": jd_skills,
        "matches": matches,
        "top_missing_skills": top_missing_skills
    }

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    """Upload a resume (PDF/DOCX/Image) → extract skills + suggest career fit"""
    content = await file.read()
    text = ""

    # Detect file type
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=content, filetype="pdf")
        for page in doc:
            text += page.get_text()
    elif file.filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(image)
    elif file.filename.endswith(".docx"):
        from docx import Document
        doc = Document(io.BytesIO(content))
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        return {"error": "Unsupported file format. Please upload PDF, DOCX, or image."}

    # Extract skills
    resume_skills = extract_skills(text)
    resume_embedding = embed_skills(resume_skills)

    # Match careers
    D, I = resume_index.search(resume_embedding, 3)
    matches = []
    for rank, idx in enumerate(I[0]):
        candidate = candidate_names[idx]
        sim = cosine_similarity(resume_embedding, resume_embeddings[idx:idx+1])
        fit_score = round(float(sim * 100), 2)
        matches.append({
            "career_match": candidate,
            "fit_score": fit_score
        })

    return {
        "resume_preview": text[:400],  # preview first 400 chars
        "skills_extracted": resume_skills,
        "career_suggestions": matches
    }

# ------------------------------
# Run Server
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
