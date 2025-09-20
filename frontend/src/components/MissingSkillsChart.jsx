import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function MissingSkillsChart({ topMissing }) {
  // Convert backend Counter list → [{ skill: "SQL", count: 3 }]
  const data = topMissing.map(([skill, count]) => ({
    skill,
    count,
  }));

  return (
    <div className="p-4 bg-white dark:bg-slate-800 rounded-lg shadow">
      <h3 className="text-sm font-medium text-slate-700 dark:text-slate-200 mb-2">
        Top Missing Skills
      </h3>
      <div style={{ height: 220 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="skill" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#3B82F6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
