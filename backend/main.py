from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import faiss
import numpy as np

# HuggingFace for skill extraction
from transformers import pipeline
# SentenceTransformers for embeddings
from sentence_transformers import SentenceTransformer

# ------------------------------
# FastAPI Setup
# ------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
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
# Skill Extraction
# ------------------------------
def extract_skills(text: str):
    entities = skill_extractor(text)
    # Filter out skills (NER labels vary by model, here we take all words except punctuation)
    skills = [e['word'] for e in entities if e['entity'] in ['MISC', 'ORG', 'PER', 'LOC']]
    return list(set(skills))

# ------------------------------
# Embeddings
# ------------------------------
def embed_skills(skills: List[str]):
    if not skills:
        return np.zeros((1, 384), dtype="float32")  # match dimension of MiniLM
    text = " ".join(skills)
    return embedder.encode([text]).astype("float32")

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
# Helper: Cosine Similarity
# ------------------------------
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
    # Extract skills from JD
    skills = extract_skills(data.job_description)

    # Embed JD skills
    jd_embedding = embed_skills(skills)

    # Search FAISS
    D, I = resume_index.search(jd_embedding, 5)

    # Build match results
    matches = []
    for rank, idx in enumerate(I[0]):
        candidate = candidate_names[idx]
        dist = float(D[0][rank])
        sim = cosine_similarity(jd_embedding, resume_embeddings[idx:idx+1])
        fit_score = round(float(sim * 100), 2)
        matches.append({
            "name": candidate,
            "distance": dist,
            "fit_score": fit_score
        })

    return {
        "skills_extracted": skills,
        "matches": matches
    }

# ------------------------------
# Run Server
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
