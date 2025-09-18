# PathPilotAI
📌 PathPilot.AI – The AI Career Copilot for Students

🌟 Overview

PathPilot.AI is an AI-powered career copilot that helps students and professionals:

Extract skills from resumes and job descriptions.

Predict career paths using deep learning.

Match resumes with job descriptions.

Analyze documents for keywords, entities, and sentiment.

Recommend GitHub repos, Kaggle datasets, and free learning resources.

Provide insights via interactive charts (missing skills, fit scores, career roadmap).

✨ Features

✅ Resume + JD Matching → Extracts and compares skills.
✅ Career Prediction → Suggests best-fit career path using DL.
✅ FAISS Indexing → Fast similarity search across resumes/jobs.
✅ Document Analyzer → Summarization, sentiment, NER, keyword extraction.
✅ GitHub & Kaggle Scraper → Suggests real projects & datasets.
✅ Charts & Visuals → Interactive graphs for skills gap & fit scores.
✅ Scalable Architecture → Frontend (React) + Backend (FastAPI) + ML services.

🛠 Tech Stack

Backend → FastAPI, spaCy, Hugging Face Transformers, FAISS, PyTorch
Frontend → React, Vite, TailwindCSS, Recharts
ML/DL → Sentence-Transformers, PyTorch (core), TensorFlow (hybrid demo)
Deployment → Hugging Face Spaces (backend), Vercel (frontend)

⚡ Setup Instructions
1. Clone Repo
git clone https://github.com/jayadeepd007/PathPilotAI.git
cd PathPilotAI

2. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
uvicorn main:app --reload


Backend runs at → http://127.0.0.1:8000

3. Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at → http://localhost:5173

🌐 Deployment (Coming Soon)

Backend → Hugging Face Spaces

Frontend → Vercel

Add live links here once deployed 🚀

📊 Demo Screenshots

📌 (Add screenshots here once your charts/UI are working)

Skill Extraction

JD Matching Results

Career Fit Score Chart

Missing Skills Radar Chart

🤝 Contributing

PRs are welcome! If you’d like to add new models, scrapers, or analytics → open a pull request.

📜 License

This project is open-source under the MIT License.