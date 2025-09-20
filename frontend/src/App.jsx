// frontend/src/App.jsx
import React, { useState } from "react";
import { motion } from "framer-motion";
import { FileText, Upload, BarChart2 } from "lucide-react";

import Navbar from "./components/Navbar";
import JobAnalyzer from "./components/JobAnalyzer";
import UploadResume from "./components/UploadResume";
import ResumePreview from "./components/ResumePreview";

export default function App() {
  const [activeTab, setActiveTab] = useState("analyzer");
  const [lastResult, setLastResult] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-900 dark:via-slate-950 dark:to-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500">

      {/* Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Hero Section */}
      <header className="text-center py-12">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-4xl md:text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"
        >
          PathPilot.AI 🚀
        </motion.h1>
        <p className="mt-4 text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
          Analyze job descriptions and resumes, discover missing skills, and get
          AI-powered career insights.
        </p>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 pb-12 space-y-8">
        {activeTab === "analyzer" && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-lg rounded-xl shadow-xl p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-6 h-6 text-indigo-500" />
              <h2 className="text-xl font-semibold">Job Analyzer</h2>
            </div>
            <JobAnalyzer onResult={setLastResult} />
          </motion.div>
        )}

        {activeTab === "resume" && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-lg rounded-xl shadow-xl p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <Upload className="w-6 h-6 text-pink-500" />
              <h2 className="text-xl font-semibold">Upload Resume</h2>
            </div>
            <UploadResume
              onResumeResult={setLastResult}
              setActiveTab={setActiveTab}   // <-- add this
            />

          </motion.div>
        )}

        {activeTab === "results" && lastResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-lg rounded-xl shadow-xl p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <BarChart2 className="w-6 h-6 text-emerald-500" />
              <h2 className="text-xl font-semibold">Results</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FitScoreChart
                fitScore={
                  lastResult.matches && lastResult.matches.length
                    ? lastResult.matches[0].fit_score || 0
                    : 0
                }
              />
              <MissingSkillsChart
                topMissing={lastResult.top_missing_skills || []}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FitScoreChart
                fitScore={
                  lastResult.matches && lastResult.matches.length
                    ? lastResult.matches[0].fit_score || 0
                    : 0
                }
              />
              <MissingSkillsChart
                topMissing={lastResult.top_missing_skills || []}
              />
            </div>

            {/* Resume Preview */}
            <ResumePreview resume={lastResult} />
          </motion.div>
        )}
      </main>
    </div>
  );
}
