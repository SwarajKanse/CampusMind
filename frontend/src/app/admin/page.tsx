"use client";

import { useState, useEffect } from "react";
import { UploadCloud, FileText, CheckCircle2, ShieldAlert, Trash2, RefreshCw, Network, Search, Hash, Globe, Cpu } from "lucide-react";

interface DocItem {
  id: number;
  filename: string;
  chunks: number;
  size: number;
  status: string;
  uploaded: string;
}

export default function AdminPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [documents, setDocuments] = useState<DocItem[]>([]);
  const [loadingDocs, setLoadingDocs] = useState(false);

  // Network diagnostics state
  const [dnsHost, setDnsHost] = useState("api.groq.com");
  const [dnsResult, setDnsResult] = useState<any>(null);
  const [resolvingDns, setResolvingDns] = useState(false);
  const [netInfo, setNetInfo] = useState<any>(null);

  const fetchDocs = async () => {
    setLoadingDocs(true);
    try {
      const res = await fetch("http://localhost:8000/api/documents/list");
      if (res.ok) setDocuments(await res.json());
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingDocs(false);
    }
  };

  const fetchNetInfo = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/network/info");
      if (res.ok) setNetInfo(await res.json());
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchDocs();
    fetchNetInfo();
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setUploadResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setUploadResult(data);
      setFile(null);
      fetchDocs();
    } catch (err: any) {
      alert(`Upload error: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this document and its chunk vectors?")) return;
    try {
      const res = await fetch(`http://localhost:8000/api/documents/${id}`, { method: "DELETE" });
      if (res.ok) fetchDocs();
    } catch (e) {
      console.error(e);
    }
  };

  const handleDnsLookup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!dnsHost.trim()) return;
    setResolvingDns(true);
    try {
      const res = await fetch(`http://localhost:8000/api/health/dns-lookup/${dnsHost.trim()}`);
      if (res.ok) setDnsResult(await res.json());
    } catch (e) {
      console.error(e);
    } finally {
      setResolvingDns(false);
    }
  };

  return (
    <div className="flex-1 max-w-7xl mx-auto w-full px-6 py-8 overflow-y-auto">
      {/* Header */}
      <div className="mb-8">
        <span className="text-xs uppercase tracking-wider font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
          CN Exp 5 & 10 | WMC Exp 4, 5, 7
        </span>
        <h1 className="text-3xl font-extrabold text-white mt-1">Document Vault & Network Telemetry</h1>
        <p className="text-sm text-slate-400">
          Upload academic course materials with RFC 1071 checksum verification, and test host socket DNS resolution.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Upload Card */}
        <div className="lg:col-span-2 glass-card p-6">
          <h2 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
            <UploadCloud className="w-5 h-5 text-emerald-400" />
            <span>Upload Document (PDF / TXT)</span>
          </h2>
          <p className="text-xs text-slate-300 mb-4">
            Files are verified for transmission integrity using multiple checksum algorithms (CN Exp 5) and chunked into ChromaDB vector store.
          </p>

          <form onSubmit={handleUpload} className="space-y-4">
            <div className="border-2 border-dashed border-white/10 hover:border-violet-500/50 rounded-xl p-8 text-center bg-slate-900/40 transition-colors">
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer block">
                <FileText className="w-10 h-10 mx-auto text-violet-400 mb-2 opacity-75" />
                <span className="text-sm font-semibold text-slate-200 block">
                  {file ? file.name : "Click to select a syllabus PDF or notes file"}
                </span>
                <span className="text-xs text-slate-400 mt-1 block">
                  Supported formats: .pdf, .txt (max 25MB)
                </span>
              </label>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400">
                {file ? `${(file.size / 1024).toFixed(1)} KB selected` : "No file chosen"}
              </span>
              <button
                type="submit"
                disabled={!file || uploading}
                className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-sm disabled:opacity-50 transition-all shadow-md shadow-emerald-600/20"
              >
                {uploading ? "Computing Checksums..." : "Upload & Vectorize"}
              </button>
            </div>
          </form>

          {/* Upload Result Telemetry (CN Exp 5) */}
          {uploadResult && (
            <div className="mt-6 p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-xs space-y-2">
              <div className="flex items-center gap-2 text-emerald-400 font-bold">
                <CheckCircle2 className="w-4 h-4" />
                <span>Document Processed Successfully!</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-slate-300 font-mono text-[11px] pt-2 border-t border-white/10">
                <div><span className="text-slate-400">SHA-256:</span> {uploadResult.sha256?.substring(0, 24)}...</div>
                <div><span className="text-slate-400">CRC-32:</span> {uploadResult.crc32}</div>
                <div><span className="text-slate-400">Internet Checksum:</span> {uploadResult.internet_checksum}</div>
                <div><span className="text-slate-400">Chunks Created:</span> {uploadResult.chunks}</div>
              </div>
            </div>
          )}
        </div>

        {/* DNS Resolver (CN Exp 10) */}
        <div className="glass-card p-6 flex flex-col justify-between">
          <div>
            <h2 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
              <Globe className="w-5 h-5 text-cyan-400" />
              <span>DNS Lookup (CN Exp 10)</span>
            </h2>
            <p className="text-xs text-slate-300 mb-4">
              Query socket resolution using standard DNS transport mechanisms.
            </p>

            <form onSubmit={handleDnsLookup} className="space-y-3">
              <input
                type="text"
                value={dnsHost}
                onChange={(e) => setDnsHost(e.target.value)}
                placeholder="Hostname (e.g. google.com)"
                className="w-full glass-input px-3 py-2 text-xs"
              />
              <button
                type="submit"
                disabled={resolvingDns}
                className="w-full py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs transition-colors"
              >
                {resolvingDns ? "Resolving..." : "Resolve Host IP"}
              </button>
            </form>

            {dnsResult && (
              <div className="mt-4 p-3 rounded-lg bg-slate-900/60 border border-white/5 text-xs space-y-1">
                <p className="font-semibold text-cyan-300">{dnsResult.hostname}</p>
                <p className="text-slate-300 font-mono">Primary IP: {dnsResult.ip}</p>
                {dnsResult.addresses && (
                  <div className="mt-1 text-[10px] text-slate-400 font-mono">
                    All IPs: {dnsResult.addresses.join(", ")}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Network interface telemetry */}
          {netInfo && (
            <div className="mt-6 pt-4 border-t border-white/10 text-xs">
              <div className="flex items-center gap-1.5 text-slate-400 mb-1">
                <Network className="w-3.5 h-3.5 text-cyan-400" />
                <span className="font-semibold">Local Interfaces (WMC Exp 4)</span>
              </div>
              <p className="text-[11px] text-slate-400">
                Interfaces monitored: {Object.keys(netInfo.server_interfaces || {}).length} active adapters
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Document Inventory Table */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-violet-400" />
            <span>Vault Inventory</span>
          </h2>
          <button
            onClick={fetchDocs}
            disabled={loadingDocs}
            className="p-1.5 rounded-lg glass hover:bg-white/10 text-slate-400 hover:text-white transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loadingDocs ? "animate-spin" : ""}`} />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="border-b border-white/10 text-slate-400 uppercase font-semibold text-[10px]">
              <tr>
                <th className="py-2.5 px-3">ID</th>
                <th className="py-2.5 px-3">Filename</th>
                <th className="py-2.5 px-3">Chunks</th>
                <th className="py-2.5 px-3">Size</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {documents.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-400">
                    No documents found in vault. Upload one above!
                  </td>
                </tr>
              ) : (
                documents.map((doc) => (
                  <tr key={doc.id} className="hover:bg-white/5 transition-colors">
                    <td className="py-3 px-3 text-slate-400 font-mono">#{doc.id}</td>
                    <td className="py-3 px-3 font-semibold text-slate-200">{doc.filename}</td>
                    <td className="py-3 px-3 text-slate-300 font-mono">{doc.chunks}</td>
                    <td className="py-3 px-3 text-slate-400">{Math.round(doc.size / 1024)} KB</td>
                    <td className="py-3 px-3">
                      <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-semibold">
                        {doc.status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right">
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="p-1 rounded hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition-colors"
                        title="Delete document"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
