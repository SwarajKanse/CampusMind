"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { MessageSquare, BarChart3, UploadCloud, Activity, Zap, Cpu } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();
  const [latency, setLatency] = useState<number | null>(null);
  const [groqOnline, setGroqOnline] = useState<boolean>(true);

  useEffect(() => {
    const checkPing = async () => {
      try {
        const start = performance.now();
        const res = await fetch("http://localhost:8000/api/health/ping");
        if (res.ok) {
          setLatency(Math.round(performance.now() - start));
        }
      } catch {
        setLatency(null);
      }
    };

    checkPing();
    const interval = setInterval(checkPing, 5000);
    return () => clearInterval(interval);
  }, []);

  const navLinks = [
    { name: "Academic Chat", href: "/chat", icon: MessageSquare },
    { name: "Analytics Dashboard", href: "/analytics", icon: BarChart3 },
    { name: "Document Vault", href: "/admin", icon: UploadCloud },
  ];

  return (
    <header className="sticky top-0 z-50 glass border-b border-white/10 px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-violet-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-violet-600/30 group-hover:scale-105 transition-transform">
            <Cpu className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-violet-400 via-cyan-300 to-white bg-clip-text text-transparent">
                CampusMind
              </span>
              <span className="text-[10px] uppercase tracking-wider font-semibold px-1.5 py-0.5 rounded bg-violet-500/20 text-violet-300 border border-violet-500/30">
                Groq LPU
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">Unified Engineering Microproject</p>
          </div>
        </Link>

        {/* Nav Links */}
        <nav className="flex items-center gap-1 sm:gap-2">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? "bg-violet-600/25 text-violet-300 border border-violet-500/40 shadow-sm shadow-violet-600/20"
                    : "text-slate-300 hover:text-white hover:bg-white/5"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
                <span>{link.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Network & Engine Telemetry (WMC & CN Exp) */}
        <div className="hidden md:flex items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-900/60 border border-white/10">
            <span
              className={`w-2 h-2 rounded-full ${
                latency !== null ? "bg-emerald-400 animate-pulse" : "bg-rose-400"
              }`}
            />
            <span className="text-slate-300">
              {latency !== null ? `${latency} ms` : "Offline"}
            </span>
            <Activity className="w-3.5 h-3.5 text-slate-400 ml-0.5" />
          </div>

          <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-full bg-cyan-950/40 border border-cyan-500/30 text-cyan-300">
            <Zap className="w-3.5 h-3.5 text-cyan-400" />
            <span>Qwen 27B</span>
          </div>
        </div>
      </div>
    </header>
  );
}
