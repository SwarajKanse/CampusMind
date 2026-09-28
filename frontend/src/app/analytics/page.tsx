"use client";

import { useState, useEffect } from "react";
import { BarChart3, RefreshCw, Zap, Database, TrendingUp, ScatterChart as ScatterIcon, ShieldCheck, Activity, Award } from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  PieChart, Pie, Cell, ScatterChart, Scatter, LineChart, Line
} from "recharts";

export default function AnalyticsPage() {
  const [stats, setStats] = useState<any>(null);
  const [abTest, setAbTest] = useState<any>(null);
  const [regression, setRegression] = useState<any>(null);
  const [pcaData, setPcaData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const [statsRes, abRes, regRes, pcaRes] = await Promise.all([
        fetch("http://localhost:8000/api/analytics/query-stats"),
        fetch("http://localhost:8000/api/analytics/ab-test"),
        fetch("http://localhost:8000/api/analytics/regression"),
        fetch("http://localhost:8000/api/analytics/embeddings-pca"),
      ]);

      if (statsRes.ok) setStats(await statsRes.json());
      if (abRes.ok) setAbTest(await abRes.json());
      if (regRes.ok) setRegression(await regRes.json());
      if (pcaRes.ok) setPcaData(await pcaRes.json());
    } catch (e) {
      console.error("Failed to load analytics", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  // Intent pie chart colors
  const INTENT_COLORS: Record<string, string> = {
    academic: "#7c3aed",
    general: "#06b6d4",
    feedback: "#22c55e",
    greeting: "#f59e0b",
    unclassified: "#64748b",
  };

  const intentPieData = stats?.intent_distribution
    ? Object.entries(stats.intent_distribution).map(([name, value]) => ({ name, value }))
    : [];

  return (
    <div className="flex-1 max-w-7xl mx-auto w-full px-6 py-8 overflow-y-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs uppercase tracking-wider font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
              Applied Statistics Laboratory (Exp 1-14)
            </span>
          </div>
          <h1 className="text-3xl font-extrabold text-white mt-1">Analytics & EDA Dashboard</h1>
          <p className="text-sm text-slate-400">
            Real-time statistical evaluation, A/B hypothesis testing, and regression analysis of RAG & CAG queries.
          </p>
        </div>

        <button
          onClick={fetchAnalytics}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-xl glass hover:bg-white/10 text-slate-200 text-sm font-semibold border border-white/10 transition-colors shrink-0"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh Data</span>
        </button>
      </div>

      {/* KPI Metric Cards (Stats Exp 1: EDA) */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <div className="glass-card p-4">
          <p className="text-xs font-semibold text-slate-400">Total Queries</p>
          <p className="text-2xl font-bold text-white mt-1">{stats?.total_queries ?? 0}</p>
          <p className="text-[11px] text-slate-400 mt-1">Sample size $N$</p>
        </div>

        <div className="glass-card p-4">
          <p className="text-xs font-semibold text-slate-400">Mean Latency</p>
          <p className="text-2xl font-bold text-violet-400 mt-1">
            {stats?.response_time?.mean !== undefined ? `${stats.response_time.mean} ms` : "—"}
          </p>
          <p className="text-[11px] text-slate-400 mt-1">
            Std Dev: ±{stats?.response_time?.std_dev ?? 0} ms
          </p>
        </div>

        <div className="glass-card p-4">
          <p className="text-xs font-semibold text-slate-400">Median Latency</p>
          <p className="text-2xl font-bold text-cyan-400 mt-1">
            {stats?.response_time?.median !== undefined ? `${stats.response_time.median} ms` : "—"}
          </p>
          <p className="text-[11px] text-slate-400 mt-1">IQR: {stats?.response_time?.iqr ?? 0} ms</p>
        </div>

        <div className="glass-card p-4">
          <p className="text-xs font-semibold text-slate-400">CAG Hit Rate</p>
          <p className="text-2xl font-bold text-emerald-400 mt-1">
            {stats?.cache_rate !== undefined ? `${Math.round(stats.cache_rate * 100)}%` : "0%"}
          </p>
          <p className="text-[11px] text-slate-400 mt-1">AISC Exp 12 Cache</p>
        </div>

        <div className="glass-card p-4">
          <p className="text-xs font-semibold text-slate-400">Avg Confidence</p>
          <p className="text-2xl font-bold text-amber-400 mt-1">
            {stats?.confidence?.mean !== undefined ? `${Math.round(stats.confidence.mean * 100)}%` : "—"}
          </p>
          <p className="text-[11px] text-slate-400 mt-1">Cosine similarity</p>
        </div>
      </div>

      {/* Row 2: A/B Hypothesis Testing & Intent Pie */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* A/B Test Card (Stats Exp 5) */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <span className="text-[10px] uppercase font-bold text-violet-400 tracking-wider">Stats Exp 5</span>
              <h2 className="text-lg font-bold text-white">A/B Hypothesis Test (RAG vs CAG)</h2>
            </div>
            <Award className="w-5 h-5 text-violet-400" />
          </div>

          <p className="text-xs text-slate-300 mb-4 leading-relaxed">
            Independent two-sample Welch t-test testing null hypothesis H₀: μ(RAG) = μ(CAG) against alternative H₁: μ(RAG) &gt; μ(CAG).
          </p>

          {abTest?.is_statistically_significant !== undefined ? (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3 text-center">
                <div className="p-3 rounded-lg bg-slate-900/60 border border-white/5">
                  <p className="text-xs text-slate-400">RAG Mean Latency</p>
                  <p className="text-xl font-bold text-violet-400 mt-0.5">{abTest.rag_mean_ms} ms</p>
                </div>
                <div className="p-3 rounded-lg bg-slate-900/60 border border-white/5">
                  <p className="text-xs text-slate-400">CAG Mean Latency</p>
                  <p className="text-xl font-bold text-cyan-400 mt-0.5">{abTest.cag_mean_ms} ms</p>
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-violet-950/30 border border-violet-500/30 text-xs space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-slate-400">T-Statistic ($t$):</span>
                  <span className="font-mono font-bold text-violet-300">{abTest.t_statistic}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Degrees of Freedom ($df$):</span>
                  <span className="font-mono text-slate-300">{abTest.degrees_of_freedom}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Observed Speedup:</span>
                  <span className="font-mono font-bold text-emerald-400">{abTest.speedup_factor}x faster</span>
                </div>
                <div className="flex justify-between pt-1 border-t border-white/10">
                  <span className="text-slate-300 font-semibold">Hypothesis Verdict:</span>
                  <span className="font-bold text-emerald-300">
                    {abTest.is_statistically_significant ? "Reject H₀ (p < 0.05, Significant)" : "Fail to Reject H₀"}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-8 text-center text-xs text-slate-400 bg-slate-900/30 rounded-xl border border-white/5">
              <Activity className="w-6 h-6 mx-auto text-slate-400 mb-2 opacity-50" />
              <p>{abTest?.message || "Submit queries via Chat to collect comparative A/B samples."}</p>
            </div>
          )}
        </div>

        {/* Intent Distribution Pie (Stats Exp 10) */}
        <div className="glass-card p-6 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <span className="text-[10px] uppercase font-bold text-cyan-400 tracking-wider">Stats Exp 10 & AISC Exp 7</span>
              <h2 className="text-lg font-bold text-white">Query Intent Classification</h2>
            </div>
            <BarChart3 className="w-5 h-5 text-cyan-400" />
          </div>

          <p className="text-xs text-slate-300 mb-2">
            Multi-class Perceptron categorization distribution of student prompts.
          </p>

          <div className="flex-1 min-h-[220px] flex items-center justify-center">
            {intentPieData.length > 0 ? (
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie
                    data={intentPieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                  >
                    {intentPieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={INTENT_COLORS[entry.name] || "#7c3aed"} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: "#12122a", borderColor: "rgba(255,255,255,0.1)", borderRadius: "8px" }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-slate-400">No intent data logged yet.</p>
            )}
          </div>
        </div>
      </div>

      {/* Row 3: Linear Regression & PCA */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Linear Regression (Stats Exp 8 & 9) */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-2">
            <div>
              <span className="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">Stats Exp 8 & 9</span>
              <h2 className="text-lg font-bold text-white">Pearson Correlation & Linear Regression</h2>
            </div>
            <TrendingUp className="w-5 h-5 text-emerald-400" />
          </div>

          <p className="text-xs text-slate-300 mb-4 leading-relaxed">
            Modeling response latency $y$ as a linear function of prompt character length $x$: $y = \beta_1 x + \beta_0$.
          </p>

          {regression?.correlation_r !== undefined ? (
            <div className="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-400">Regression Equation:</span>
                <span className="font-mono font-bold text-cyan-300">{regression.equation}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Pearson Correlation ($r$):</span>
                <span className="font-mono font-bold text-violet-300">{regression.correlation_r}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Coefficient of Determination ($R^2$):</span>
                <span className="font-mono font-bold text-emerald-300">{regression.r_squared}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Slope ($\beta_1$):</span>
                <span className="font-mono text-slate-300">{regression.slope} ms/char</span>
              </div>
            </div>
          ) : (
            <div className="py-8 text-center text-xs text-slate-400 bg-slate-900/30 rounded-xl border border-white/5">
              <p>{regression?.message || "Waiting for query logs to perform regression analysis."}</p>
            </div>
          )}
        </div>

        {/* 2D PCA & Clustering (Stats Exp 12) */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-2">
            <div>
              <span className="text-[10px] uppercase font-bold text-cyan-400 tracking-wider">Stats Exp 12</span>
              <h2 className="text-lg font-bold text-white">PCA & Semantic Query Clustering</h2>
            </div>
            <ScatterIcon className="w-5 h-5 text-cyan-400" />
          </div>

          <p className="text-xs text-slate-300 mb-4 leading-relaxed">
            2D Principal Component Analysis dimensionality reduction of 384-dimensional query embeddings.
          </p>

          {pcaData?.points && pcaData.points.length > 0 ? (
            <div>
              <div className="h-[180px] w-full">
                <ResponsiveContainer width="100%" height={180}>
                  <ScatterChart>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis type="number" dataKey="x" name="PC1" stroke="#64748b" textAnchor="end" />
                    <YAxis type="number" dataKey="y" name="PC2" stroke="#64748b" />
                    <Tooltip
                      cursor={{ strokeDasharray: "3 3" }}
                      contentStyle={{ backgroundColor: "#12122a", borderColor: "rgba(255,255,255,0.1)", borderRadius: "8px", fontSize: "12px" }}
                    />
                    <Scatter name="Queries" data={pcaData.points} fill="#06b6d4" />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
              {pcaData.explained_variance && (
                <p className="text-[11px] text-slate-400 mt-2 text-center">
                  Explained Variance: PC1: {(pcaData.explained_variance[0] * 100).toFixed(1)}%, PC2: {(pcaData.explained_variance[1] * 100).toFixed(1)}%
                </p>
              )}
            </div>
          ) : (
            <div className="py-8 text-center text-xs text-slate-400 bg-slate-900/30 rounded-xl border border-white/5">
              <p>{pcaData?.message || "Submit more questions in chat to view 2D PCA cluster space."}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
