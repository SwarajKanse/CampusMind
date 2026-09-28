import type { Metadata } from "next";
import Navbar from "@/components/Navbar";
import "./globals.css";

export const metadata: Metadata = {
  title: "CampusMind — AI-Powered Academic Assistant",
  description: "Unified Engineering Microproject: Academic RAG Chatbot with Groq LPU, CAG Cache, and Statistical Analytics",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full antialiased">
      <body className="min-h-full flex flex-col bg-[#0a0a1a] text-slate-100 selection:bg-violet-600 selection:text-white">
        <Navbar />
        <main className="flex-1 flex flex-col">{children}</main>
      </body>
    </html>
  );
}
