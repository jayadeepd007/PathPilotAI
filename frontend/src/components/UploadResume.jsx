// frontend/src/components/UploadResume.jsx
import React, { useState } from "react";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";
import { ClipLoader } from "react-spinners"; // spinner

export default function UploadResume({ onResumeResult, setActiveTab }) {
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("http://127.0.0.1:8000/analyze-resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      onResumeResult(res.data);

      toast.success("Resume analyzed! Switching to results...");

      // auto-switch
      setTimeout(() => {
        setActiveTab("results");
      }, 1500);
    } catch (err) {
      console.error(err);
      toast.error("Error analyzing resume. Try again!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <input
        type="file"
        accept=".pdf,.docx,.png,.jpg,.jpeg"
        onChange={handleUpload}
        disabled={loading}
        className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4
        file:rounded-md file:border-0 file:text-sm file:font-semibold
        file:bg-sky-50 file:text-sky-700 hover:file:bg-sky-100
        dark:file:bg-slate-800 dark:file:text-slate-200 disabled:opacity-50"
      />

      {loading && (
        <div className="flex items-center gap-3 text-sky-500">
          <ClipLoader size={28} color="#0ea5e9" />
          <span className="text-sm">Analyzing resume... Please wait</span>
        </div>
      )}

      <Toaster position="top-right" />
    </div>
  );
}
