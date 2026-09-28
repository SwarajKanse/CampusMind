"""
Ingest textbook chapters aligned with syllabus experiments into CampusMind ChromaDB and SQLite.
Extracts high-relevance pages from official textbooks in D:\\Engineering\\Projects\\CampusMind\\books.
"""
import os
import sys
import hashlib
import binascii
import pymupdf

# Set UTF-8 encoding for Windows terminal
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure backend root is in sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from database import SessionLocal, create_tables
from models import Document
from services.checksum_service import ChecksumService
from services.rag_service import RAGService


BOOKS_DIR = os.path.join(os.path.dirname(backend_dir), "books")

BOOK_SPECS = [
    {
        "filename": "Artificial-Intelligence-A-Modern-Approach-4th-Edition-1.pdf",
        "display_name": "Russell & Norvig - AI: A Modern Approach (4th Ed)",
        "subject": "AISC",
        "topics": {
            "Intelligent Agents & PEAS Formulation": (105, 115),
            "Uninformed Search (BFS & DFS)": (168, 185),
            "Informed Search (A* Search & Heuristics)": (190, 215),
        }
    },
    {
        "filename": "computer-networks-tanenbaum-5th-edition.pdf",
        "display_name": "Tanenbaum - Computer Networks (5th Ed)",
        "subject": "CN",
        "topics": {
            "OSI & TCP/IP Reference Models": (48, 65),
            "Error Detection & CRC Polynomials": (230, 245),
            "Sliding Window Protocols": (246, 260),
            "TCP Three-Way Handshake & Connection Management": (538, 552),
            "Domain Name System (DNS)": (645, 660),
        }
    },
    {
        "filename": "_OceanofPDF.com_Principles_of_Soft_Computing_-_S_N_Sivanandam.pdf",
        "display_name": "Sivanandam - Principles of Soft Computing (2nd Ed)",
        "subject": "AISC",
        "topics": {
            "Perceptron Networks & Learning Rule": (33, 45),
            "Fuzzy Sets & Membership Functions": (120, 135),
            "Defuzzification Methods (Centroid/Bisector)": (165, 175),
            "Mamdani & Takagi-Sugeno Fuzzy Models": (180, 195),
            "Adaptive Neuro-Fuzzy Inference System (ANFIS)": (240, 255),
        }
    },
    {
        "filename": "Practical Statistics for Data Scientists.pdf",
        "display_name": "Bruce & Bruce - Practical Statistics for Data Scientists (2nd Ed)",
        "subject": "Stats",
        "topics": {
            "Exploratory Data Analysis & Boxplots": (35, 60),
            "Central Limit Theorem & Sampling Distributions": (110, 125),
            "Hypothesis Testing & Student's/Welch t-test": (150, 195),
            "Multiple Linear Regression & Cross-Validation": (230, 260),
            "K-Means Clustering & PCA": (445, 470),
        }
    },
    {
        "filename": "_OceanofPDF.com_Probability_and_Statistics_for_ML_-_Charu_C_Aggarwal.pdf",
        "display_name": "Charu Aggarwal - Probability & Statistics for ML",
        "subject": "Stats",
        "topics": {
            "Descriptive Statistics & Sampling Distributions": (230, 245),
            "Central Limit Theorem (CLT)": (254, 265),
            "Hypothesis Testing & Student's/Welch t-test": (340, 355),
            "Linear Regression & Ordinary Least Squares": (480, 495),
            "Principal Component Analysis (PCA) & K-Means": (615, 635),
        }
    },
    {
        "filename": "WirelessCommunicationsbyTheodoreS.Rappaportz-lib.org.pdf",
        "display_name": "Rappaport - Wireless Communications (2nd Ed)",
        "subject": "WMC",
        "topics": {
            "Cellular Concept & Frequency Reuse": (35, 52),
            "Channel Assignment & Handoff Strategies": (53, 68),
            "Wireless MAC Protocols & CSMA/CA": (425, 438),
        }
    },
    {
        "filename": "The.DevOps.Handbook_faghatketab.ir.pdf",
        "display_name": "Gene Kim - The DevOps Handbook (2nd Ed)",
        "subject": "ASD&D",
        "topics": {
            "Agile Principles & Value Stream Architecture": (35, 50),
            "Continuous Integration & Fast Feedback Loops": (145, 160),
            "Automated Testing & Deployment Pipelines": (161, 178),
            "Production Telemetry & Observability Systems": (195, 210),
        }
    },
    {
        "filename": "Data-Communications-and-Network-5e.pdf",
        "display_name": "Forouzan - Data Communications and Networking (5th Ed)",
        "subject": "CN",
        "topics": {
            "OSI Layers & Encapsulation Architecture": (28, 48),
            "CRC Cyclic Redundancy Check & Checksums": (285, 310),
        }
    },
]


def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return " ".join(lines)


def chunk_text(text: str, chunk_size: int = 350, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.strip()) > 50:
            chunks.append(chunk.strip())
        i += max(1, chunk_size - overlap)
    return chunks


def ingest_books():
    print("=" * 70)
    print("📖 CampusMind Multi-Subject Textbook Ingestion Engine")
    print("=" * 70)

    if not os.path.exists(BOOKS_DIR):
        print(f"❌ Books directory not found: {BOOKS_DIR}")
        return

    create_tables()
    db = SessionLocal()
    rag = RAGService()

    total_chunks_added = 0
    total_books_processed = 0

    for spec in BOOK_SPECS:
        pdf_path = os.path.join(BOOKS_DIR, spec["filename"])
        if not os.path.exists(pdf_path):
            print(f"⚠️ Book not found: {spec['filename']}. Skipping.")
            continue

        print(f"\n📘 Processing: {spec['display_name']} ({spec['subject']})")
        doc = pymupdf.open(pdf_path)
        total_pages = len(doc)
        print(f"   Total Pages in Book: {total_pages}")

        # Compute full book checksums for document metadata (CN Exp 5)
        with open(pdf_path, "rb") as f:
            file_bytes = f.read()
        sha256_hash = hashlib.sha256(file_bytes).hexdigest()
        crc32_hash = hex(binascii.crc32(file_bytes) & 0xFFFFFFFF)
        file_size = len(file_bytes)

        # Check if already registered in SQLite
        db_doc = db.query(Document).filter(Document.file_hash == sha256_hash).first()
        if db_doc and db_doc.status == "embedded" and db_doc.chunk_count > 0:
            print(f"   ⏭️ Already embedded {db_doc.chunk_count} chunks. Skipping.")
            continue

        if not db_doc:
            db_doc = Document(
                filename=spec["display_name"],
                file_hash=sha256_hash,
                chunk_count=0,
                file_size=file_size,
                status="processing",
            )
            db.add(db_doc)
            db.commit()
            db.refresh(db_doc)

        book_chunks = []
        for topic_name, (start_pg, end_pg) in spec["topics"].items():
            start_idx = max(0, start_pg - 1)
            end_idx = min(total_pages, end_pg)
            extracted_pages_text = []

            for pg in range(start_idx, end_idx):
                page_text = doc[pg].get_text()
                if len(page_text.strip()) > 100:
                    cleaned = clean_text(page_text)
                    extracted_pages_text.append(f"[Page {pg+1}] {cleaned}")

            combined_topic_text = "\n\n".join(extracted_pages_text)
            topic_chunks = chunk_text(combined_topic_text, chunk_size=300, overlap=40)

            for i, chunk in enumerate(topic_chunks):
                book_chunks.append({
                    "text": f"[{spec['display_name']} - Topic: {topic_name}]\n{chunk}",
                    "doc_id": db_doc.id,
                    "chunk_idx": len(book_chunks),
                    "source": f"{spec['display_name']} ({topic_name})",
                })

            print(f"   ✓ Topic: '{topic_name}' (Pgs {start_pg}-{end_pg}) -> {len(topic_chunks)} chunks")

        # Ingest chunks into ChromaDB
        if book_chunks:
            print(f"   ⚡ Embedding {len(book_chunks)} chunks into ChromaDB vector store...")
            rag.add_documents(book_chunks)
            db_doc.chunk_count = len(book_chunks)
            db_doc.status = "embedded"
            db.commit()
            total_chunks_added += len(book_chunks)
            total_books_processed += 1
            print(f"   ✅ Successfully indexed {len(book_chunks)} chunks for '{spec['display_name']}'")

    db.close()
    print("\n" + "=" * 70)
    print(f"🎉 Ingestion Complete! Processed {total_books_processed} new textbooks, {total_chunks_added} chunks added to vector store.")
    print("=" * 70)


if __name__ == "__main__":
    ingest_books()
