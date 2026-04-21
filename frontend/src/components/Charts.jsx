import React, { useEffect, useState } from "react";
import { getStats } from "../services/api";
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from "recharts";

const PIE_COLORS  = ["#e85d04", "#f48c06", "#74c69d", "#48cae4"];
const BAR_COLORS  = { Breakfast: "#f48c06", Lunch: "#74c69d", Dinner: "#e85d04", Snack: "#48cae4" };

export default function Charts() {
  const [stats,   setStats]   = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStats()
      .then((r) => setStats(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="card"><p className="loading-text">Loading charts…</p></div>;
  if (!stats)  return null;

  const pieData = Object.entries(stats.breakdown).map(([name, value]) => ({ name, value }));
  const barData = Object.entries(stats.meal_types).map(([name, value]) => ({ name, value }));

  return (
    <div className="card">
      <h2 className="section-title">📊 Recipe Insights</h2>
      <p className="stat-total">Total recipes: <strong>{stats.total}</strong></p>

      <div className="charts-grid">
        <div className="chart-box">
          <h3 className="chart-title">Dietary Breakdown</h3>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" outerRadius={80}
                   dataKey="value" label={({ name, percent }) =>
                     `${name} ${(percent * 100).toFixed(0)}%`}
                   labelLine={false}>
                {pieData.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-box">
          <h3 className="chart-title">Recipes by Meal Type</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={barData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0e8d8" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {barData.map((entry, i) => (
                  <Cell key={i} fill={BAR_COLORS[entry.name] || "#e85d04"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
