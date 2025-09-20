import React, { useState } from "react";
import { matchJD } from "../api";
import MissingSkillsChart from "./MissingSkillsChart";
import FitScoreChart from "./FitScoreChart";

export default function JobAnalyzer({ onResult }) {
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    setLoading(true);
    try {
      const res = await matchJD(jd);
      setResult(res);
      onResult(res);
    } catch (err) {
      console.error(err);
      alert("Backend error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <textarea
        rows={6}
        placeholder="Paste job description..."
        value={jd}
        onChange={(e) => setJd(e.target.value)}
        className="w-full p-3 rounded-md bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700"
      />
      <div className="flex gap-2">
        <button
          onClick={analyze}
          disabled={loading}
          className="bg-sky-600 text-white px-4 py-2 rounded"
        >
          {loading ? "Analyzing..." : "Analyze JD"}
        </button>
      </div>

      {result && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FitScoreChart fitScore={result.matches[0]?.fit_score || 0} />
          <MissingSkillsChart topMissing={result.top_missing_skills || []} />
        </div>
      )}
    </div>
  );
}
