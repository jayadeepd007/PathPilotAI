import React from "react";
import { Sun, Moon } from "lucide-react";

export default function Navbar({ activeTab, setActiveTab }) {
  const [dark, setDark] = React.useState(true);

  React.useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  const tabs = [
    { id: "analyzer", label: "Job Analyzer" },
    { id: "resume", label: "Upload Resume" },
    { id: "results", label: "Results" },
  ];

  return (
    <nav className="w-full bg-white/70 dark:bg-slate-900/70 backdrop-blur-lg border-b dark:border-slate-700">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="text-2xl font-bold text-indigo-500">PathPilot.AI</div>
        <div className="flex items-center gap-3">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`px-3 py-1 rounded-md text-sm ${
                activeTab === t.id
                  ? "bg-indigo-600 text-white"
                  : "text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
              }`}
            >
              {t.label}
            </button>
          ))}
          <button
            onClick={() => setDark(!dark)}
            className="p-2 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            {dark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </nav>
  );
}
