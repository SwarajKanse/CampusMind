import Link from "next/link";
import { MessageSquare, BarChart3, UploadCloud, Cpu, Zap, ShieldCheck, ArrowRight, Layers, Network, Database } from "lucide-react";

export default function Home() {
  const subjects = [
    { code: "AISC", name: "AI & Soft Computing", exps: "PEAS, Search (BFS/DFS/A*), Perceptron, RAG, CAG, Fuzzy & Neuro-Fuzzy" },
    { code: "CN", name: "Computer Networks", exps: "PING, Checksum (CRC/SHA256/Internet), Sockets, DNS Resolution" },
    { code: "Stats", name: "Applied Statistics", exps: "EDA, CLT, Hypothesis T-Test, Linear Regression, PCA & Clustering" },
    { code: "WMC", name: "Wireless & Mobile Computing", exps: "Interface Monitoring, Throughput/Latency Telemetry" },
    { code: "ASD&D", name: "Agile Software Development", exps: "Git Versioning, CI/CD, Containerization, IaC Manifests" },
  ];

  return (
    <div className="relative min-h-[calc(100vh-65px)] flex flex-col justify-between overflow-hidden bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(124,58,237,0.18),rgba(255,255,255,0))]">
      {/* Background glowing orbs */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-violet-600/15 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 w-[400px] h-[250px] bg-cyan-500/10 blur-[100px] rounded-full pointer-events-none" />

      {/* Hero Section */}
      <div className="relative max-w-6xl mx-auto px-6 pt-16 pb-12 text-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-violet-950/50 border border-violet-500/30 text-xs font-semibold text-violet-300 mb-6 shadow-inner">
          <Zap className="w-3.5 h-3.5 text-cyan-400" />
          <span>Powered by Groq Cloud LPU & Qwen 27B</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white mb-5">
          Intelligent Academic RAG & <br />
          <span className="bg-gradient-to-r from-violet-400 via-cyan-300 to-indigo-300 bg-clip-text text-transparent">
            Experimental Engineering Engine
          </span>
        </h1>

        <p className="max-w-2xl mx-auto text-base sm:text-lg text-slate-300 mb-8 leading-relaxed">
          One unified, high-performance microproject cross-covering curriculum experiments across
          <span className="text-violet-300 font-semibold"> AISC, CN, Stats, WMC, and ASD&D</span> with
          real-time vector retrieval, cache augmentation, and rigorous statistical analysis.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4">
          <Link
            href="/chat"
            className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-semibold shadow-lg shadow-violet-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            <MessageSquare className="w-4 h-4 text-cyan-300" />
            <span>Open Academic Chat</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </Link>

          <Link
            href="/analytics"
            className="flex items-center gap-2 px-6 py-3.5 rounded-xl glass hover:bg-white/10 text-slate-200 font-semibold border border-white/10 hover:border-violet-500/40 transition-all"
          >
            <BarChart3 className="w-4 h-4 text-cyan-400" />
            <span>View Statistics & EDA</span>
          </Link>

          <Link
            href="/admin"
            className="flex items-center gap-2 px-6 py-3.5 rounded-xl glass hover:bg-white/10 text-slate-200 font-semibold border border-white/10 hover:border-cyan-500/40 transition-all"
          >
            <UploadCloud className="w-4 h-4 text-emerald-400" />
            <span>Upload Documents</span>
          </Link>
        </div>
      </div>

      {/* Feature Cards Grid */}
      <div className="max-w-6xl mx-auto px-6 py-8 w-full">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1 */}
          <Link href="/chat" className="glass-card p-6 group hover:border-violet-500/50 hover:shadow-violet-600/20 transition-all">
            <div className="w-12 h-12 rounded-xl bg-violet-600/20 border border-violet-500/30 flex items-center justify-center text-violet-400 mb-4 group-hover:scale-110 transition-transform">
              <MessageSquare className="w-6 h-6 text-cyan-400" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2 group-hover:text-cyan-300 transition-colors">
              RAG & CAG Chatbot
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed mb-4">
              Context-grounded answering using ChromaDB embeddings + Groq LPUs. Sub-5ms repeated response serving with Cache-Augmented Generation (CAG).
            </p>
            <div className="flex items-center gap-2 text-xs font-semibold text-violet-400">
              <span>Covers AISC Exp 9, 10, 11, 12</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Card 2 */}
          <Link href="/analytics" className="glass-card p-6 group hover:border-cyan-500/50 hover:shadow-cyan-600/20 transition-all">
            <div className="w-12 h-12 rounded-xl bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-4 group-hover:scale-110 transition-transform">
              <BarChart3 className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2 group-hover:text-cyan-300 transition-colors">
              Statistical Analytics & EDA
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed mb-4">
              Live exploratory data analysis: latency distributions, A/B Welch t-test (RAG vs CAG), Pearson correlation regression, and PCA clustering.
            </p>
            <div className="flex items-center gap-2 text-xs font-semibold text-cyan-400">
              <span>Covers Stats Exp 1, 4, 5, 8, 9, 12</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Card 3 */}
          <Link href="/admin" className="glass-card p-6 group hover:border-emerald-500/50 hover:shadow-emerald-600/20 transition-all">
            <div className="w-12 h-12 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-4 group-hover:scale-110 transition-transform">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2 group-hover:text-emerald-300 transition-colors">
              Integrity & Checksum Vault
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed mb-4">
              Document ingestion verifying transmission integrity via CRC-32, SHA-256, and Internet Checksum RFC 1071 with automatic semantic chunking.
            </p>
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400">
              <span>Covers CN Exp 5 & 9</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>
        </div>
      </div>

      {/* Curriculum Coverage Badges */}
      <div className="max-w-6xl mx-auto px-6 py-8 w-full border-t border-white/5">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4 text-center">
          Comprehensive Laboratory Curriculum Coverage
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {subjects.map((sub) => (
            <div key={sub.code} className="p-3 rounded-lg bg-slate-900/50 border border-white/5">
              <div className="flex items-center justify-between mb-1">
                <span className="font-extrabold text-sm text-cyan-300">{sub.code}</span>
                <span className="text-[10px] text-slate-400 font-medium">Mapped</span>
              </div>
              <p className="text-xs font-semibold text-slate-200 truncate">{sub.name}</p>
              <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">{sub.exps}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <footer className="glass border-t border-white/10 px-6 py-4 text-center text-xs text-slate-400">
        CampusMind © 2026 — Antigravity Engineering Lab • Fast Groq Cloud LPU Architecture
      </footer>
    </div>
  );
}
