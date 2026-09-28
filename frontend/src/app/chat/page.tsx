"use client";

import { useState, useEffect, useRef } from "react";
import { Send, Bot, User, Sparkles, Database, Clock, ShieldAlert, FileText, CheckCircle2, RefreshCw, Cpu, Layers, UploadCloud } from "lucide-react";

interface DocumentItem {
  id: number;
  filename: string;
  chunks: number;
  size: number;
  status: string;
}

interface Message {
  id: string;
  sender: "user" | "bot";
  text: string;
  sources?: string[];
  confidence?: number;
  cached?: boolean;
  responseTimeMs?: number;
  intent?: { intent: string; confidence: number };
  fuzzyScores?: { mamdani: number; sugeno: number; neurofuzzy: number; combined: number };
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      sender: "bot",
      text: "Hello! I am **CampusMind**, your AI academic assistant powered by **Groq Cloud LPUs** and **ChromaDB**. Ask me questions about your uploaded course materials, algorithms, or engineering concepts!",
      confidence: 1.0,
      cached: false,
    },
  ]);
  const [inputQuery, setInputQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [useCache, setUseCache] = useState(true);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [docLoading, setDocLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch document vault list
  const fetchDocuments = async () => {
    setDocLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/documents/list");
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      }
    } catch (e) {
      console.error("Failed to load documents", e);
    } finally {
      setDocLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (queryText?: string) => {
    const q = queryText || inputQuery;
    if (!q.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: "user",
      text: q.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery("");
    setLoading(true);

    try {
      const start = performance.now();
      const res = await fetch("http://localhost:8000/api/chat/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q.trim(), use_cache: useCache }),
      });

      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }

      const data = await res.json();
      const clientElapsed = Math.round(performance.now() - start);

      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: data.answer || "No response received.",
        sources: data.sources || [],
        confidence: data.confidence ?? 0.0,
        cached: data.cached ?? false,
        responseTimeMs: data.response_time_ms || clientElapsed,
        intent: data.intent,
        fuzzyScores: data.fuzzy_scores,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err: any) {
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: `⚠️ **Error communicating with CampusMind API**: ${err.message}. Make sure the FastAPI backend is running on port 8000.`,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const starterPrompts = [
    "What is RAG (Retrieval-Augmented Generation)?",
    "Explain the difference between TCP and UDP.",
    "How does the Central Limit Theorem work?",
    "Describe BFS vs DFS graph search.",
  ];

  return (
    <div className="flex-1 flex h-[calc(100vh-65px)] overflow-hidden">
      {/* Sidebar: Document Vault */}
      <aside className="w-72 hidden md:flex flex-col border-r border-white/10 glass">
        <div className="p-4 border-b border-white/10 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-cyan-400" />
            <h2 className="font-bold text-sm text-white">Document Vault</h2>
          </div>
          <button
            onClick={fetchDocuments}
            disabled={docLoading}
            className="p-1 rounded-md hover:bg-white/10 text-slate-400 hover:text-white transition-colors"
            title="Refresh documents"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${docLoading ? "animate-spin" : ""}`} />
          </button>
        </div>

        {/* Document list */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {documents.length === 0 ? (
            <div className="text-center py-8 text-xs text-slate-400 px-4">
              <UploadCloud className="w-8 h-8 mx-auto text-slate-400 mb-2 opacity-60" />
              <p>No documents uploaded yet.</p>
              <a href="/admin" className="text-violet-400 hover:underline mt-1 block font-semibold">
                Upload Syllabus or Notes →
              </a>
            </div>
          ) : (
            documents.map((doc) => (
              <div
                key={doc.id}
                className="p-3 rounded-lg bg-slate-900/60 border border-white/5 hover:border-violet-500/30 transition-all text-xs"
              >
                <div className="flex items-start gap-2">
                  <FileText className="w-4 h-4 text-violet-400 shrink-0 mt-0.5" />
                  <div className="min-w-0 flex-1">
                    <p className="font-semibold text-slate-200 truncate">{doc.filename}</p>
                    <div className="flex items-center gap-2 mt-1 text-[11px] text-slate-400">
                      <span>{doc.chunks} chunks</span>
                      <span>•</span>
                      <span>{Math.round(doc.size / 1024)} KB</span>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* CAG Cache Toggle */}
        <div className="p-4 border-t border-white/10 bg-slate-900/40">
          <label className="flex items-center justify-between cursor-pointer">
            <div className="flex items-center gap-2">
              <Database className="w-4 h-4 text-cyan-400" />
              <span className="text-xs font-semibold text-slate-200">CAG Cache</span>
            </div>
            <input
              type="checkbox"
              checked={useCache}
              onChange={(e) => setUseCache(e.target.checked)}
              className="accent-violet-500 w-4 h-4 rounded cursor-pointer"
            />
          </label>
          <p className="text-[11px] text-slate-400 mt-1">
            Instant sub-5ms cached inference for repeated queries (AISC Exp 12).
          </p>
        </div>
      </aside>

      {/* Main Chat Interface */}
      <div className="flex-1 flex flex-col bg-[#0a0a1a]">
        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 max-w-3xl ${
                msg.sender === "user" ? "ml-auto justify-end" : "mr-auto justify-start"
              }`}
            >
              {/* Bot Avatar */}
              {msg.sender === "bot" && (
                <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-violet-600 to-cyan-500 flex items-center justify-center shrink-0 shadow-md">
                  <Bot className="w-4 h-4 text-white" />
                </div>
              )}

              {/* Message Content Bubble */}
              <div
                className={`p-4 rounded-2xl text-sm leading-relaxed ${
                  msg.sender === "user"
                    ? "bg-violet-600 text-white rounded-tr-sm shadow-lg shadow-violet-600/20"
                    : "glass-card text-slate-200 rounded-tl-sm border border-white/10"
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.text}</div>

                {/* Bot Metadata / Telemetry Footnote */}
                {msg.sender === "bot" && (msg.sources || msg.responseTimeMs || msg.intent) && (
                  <div className="mt-3 pt-3 border-t border-white/10 flex flex-wrap items-center gap-2 text-[11px]">
                    {/* Cached badge */}
                    {msg.cached && (
                      <span className="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-medium border border-cyan-500/30 flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-cyan-400" />
                        CAG Cache Hit (AISC Exp 12)
                      </span>
                    )}

                    {/* Latency */}
                    {msg.responseTimeMs !== undefined && (
                      <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 flex items-center gap-1 border border-white/5">
                        <Clock className="w-3 h-3 text-slate-400" />
                        {msg.responseTimeMs} ms
                      </span>
                    )}

                    {/* Intent */}
                    {msg.intent?.intent && (
                      <span className="px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        Intent: {msg.intent.intent} ({Math.round(msg.intent.confidence * 100)}%)
                      </span>
                    )}

                    {/* Confidence */}
                    {msg.confidence !== undefined && (
                      <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                        Cosine Conf: {Math.round(msg.confidence * 100)}%
                      </span>
                    )}

                    {/* Fuzzy Quality Score */}
                    {msg.fuzzyScores?.combined !== undefined && (
                      <span className="px-2 py-0.5 rounded-full bg-violet-500/20 text-violet-300 border border-violet-500/30">
                        Fuzzy Score: {msg.fuzzyScores.combined}
                      </span>
                    )}

                    {/* Sources citations */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="w-full mt-1 flex flex-wrap items-center gap-1 text-[11px] text-slate-400">
                        <span className="font-semibold text-slate-400">Sources:</span>
                        {msg.sources.map((s, idx) => (
                          <span key={idx} className="px-1.5 py-0.5 rounded bg-slate-800/80 border border-white/5 text-slate-300 font-mono text-[10px]">
                            {s}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* User Avatar */}
              {msg.sender === "user" && (
                <div className="w-8 h-8 rounded-lg bg-slate-800 border border-white/10 flex items-center justify-center shrink-0">
                  <User className="w-4 h-4 text-slate-300" />
                </div>
              )}
            </div>
          ))}

          {/* Typing indicator */}
          {loading && (
            <div className="flex gap-3 max-w-3xl mr-auto items-center text-xs text-slate-400">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-violet-600 to-cyan-500 flex items-center justify-center shrink-0 animate-pulse">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="p-3 rounded-xl glass-card flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-violet-400 animate-bounce" />
                <div className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.2s]" />
                <div className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce [animation-delay:0.4s]" />
                <span className="text-slate-400 text-xs ml-1">Groq LPU reasoning...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick starter chips */}
        {messages.length <= 2 && (
          <div className="px-6 py-2 flex flex-wrap gap-2">
            {starterPrompts.map((p, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(p)}
                className="text-xs px-3 py-1.5 rounded-full glass hover:bg-white/10 text-slate-300 hover:text-white border border-white/10 transition-colors"
              >
                {p}
              </button>
            ))}
          </div>
        )}

        {/* Input Bar */}
        <div className="p-4 border-t border-white/10 glass">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="max-w-4xl mx-auto flex items-center gap-2"
          >
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              placeholder="Ask an academic question from uploaded course materials..."
              disabled={loading}
              className="flex-1 glass-input px-4 py-3 text-sm placeholder:text-slate-400"
            />
            <button
              type="submit"
              disabled={loading || !inputQuery.trim()}
              className="px-5 py-3 rounded-lg bg-gradient-to-r from-violet-600 to-cyan-600 hover:from-violet-500 hover:to-cyan-500 text-white font-semibold text-sm disabled:opacity-50 disabled:cursor-not-allowed shadow-md shadow-violet-600/20 transition-all flex items-center gap-1.5"
            >
              <Send className="w-4 h-4" />
              <span>Send</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
