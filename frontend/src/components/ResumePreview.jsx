import React from "react";

export default function ResumePreview({ resume }) {
  if (!resume) return null;

  return (
    <div className="p-4 bg-white dark:bg-slate-800 rounded-lg shadow space-y-3">
      <h3 className="text-sm font-medium text-slate-700 dark:text-slate-200">
        Resume Analysis
      </h3>

      {/* Resume text preview */}
      <div className="bg-slate-50 dark:bg-slate-900 p-3 rounded text-sm max-h-40 overflow-y-auto">
        <p className="whitespace-pre-line">{resume.resume_preview}</p>
      </div>

      {/* Extracted skills */}
      <div>
        <h4 className="font-semibold text-slate-700 dark:text-slate-300 mb-1">
          Skills Extracted:
        </h4>
        <div className="flex flex-wrap gap-2">
          {resume.skills_extracted && resume.skills_extracted.length > 0 ? (
            resume.skills_extracted.map((skill, i) => (
              <span
                key={i}
                className="px-2 py-1 text-xs rounded bg-sky-100 text-sky-700 dark:bg-sky-800 dark:text-sky-100"
              >
                {skill}
              </span>
            ))
          ) : (
            <span className="text-sm text-slate-500">No skills found</span>
          )}
        </div>
      </div>

      {/* Career suggestions */}
      <div>
        <h4 className="font-semibold text-slate-700 dark:text-slate-300 mb-1">
          Suggested Careers:
        </h4>
        <ul className="list-disc list-inside text-sm text-slate-600 dark:text-slate-300">
          {resume.career_suggestions && resume.career_suggestions.length > 0 ? (
            resume.career_suggestions.map((s, i) => (
              <li key={i}>
                {s.career_match} —{" "}
                <span className="font-semibold text-sky-600 dark:text-sky-400">
                  {s.fit_score}%
                </span>
              </li>
            ))
          ) : (
            <li>No suggestions</li>
          )}
        </ul>
      </div>
    </div>
  );
}
