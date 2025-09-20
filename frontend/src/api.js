// frontend/src/api.js
import axios from "axios";

const BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function matchJD(job_description) {
  const res = await axios.post(`${BASE}/match_job_description`, { job_description });
  return res.data;
}

export async function predictCareer(skills) {
  const res = await axios.post(`${BASE}/predict-career`, { skills });
  return res.data;
}

// New: upload resume (PDF/DOCX/IMG)
export async function analyzeResume(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await axios.post(`${BASE}/analyze-resume`, form, {
    headers: { "Content-Type": "multipart/form-data" },
    timeout: 120000
  });
  return res.data;
}
