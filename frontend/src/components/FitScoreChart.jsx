import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

export default function FitScoreChart({ fitScore }) {
  const data = [
    { name: "Fit", value: fitScore },
    { name: "Gap", value: 100 - fitScore },
  ];

  const COLORS = ["#10B981", "#EF4444"]; // green, red

  return (
    <div className="p-4 bg-white dark:bg-slate-800 rounded-lg shadow">
      <h3 className="text-sm font-medium text-slate-700 dark:text-slate-200 mb-2">
        Career Fit Score
      </h3>
      <div style={{ height: 220 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={90}
              dataKey="value"
            >
              {data.map((entry, i) => (
                <Cell key={i} fill={COLORS[i]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-2 text-center text-sm text-slate-600 dark:text-slate-300">
        Fit: {fitScore}%
      </div>
    </div>
  );
}
