# 🎓 CampusMind — Phase-Wise Implementation Plan

> **Deadline**: Complete by **October 5, 2026** (7 days from now)
> **Executor**: Antigravity + Gemini 3.8 Flash (high-speed model)
> **Human role**: Only logins where required, nothing else

---

## 💻 Your Laptop Specs & Impact

| Spec | Value | Impact |
|------|-------|--------|
| **CPU** | Intel i5-1235U (10 cores, 12 threads) | ✅ Adequate for development |
| **RAM** | 16 GB | ⚠️ Tight — no local LLM possible |
| **GPU** | Intel Iris Xe (integrated, 2GB shared) | ❌ **No CUDA, no local inference** |
| **Disk** | 512GB NVMe (137GB free on D:) | ✅ Enough for project |
| **OS** | Windows 11 | ✅ Fine |

### ❌ What CANNOT Run Locally
- **Ollama with any model** — needs minimum 8GB VRAM (you have 0 dedicated VRAM)
- **Any local LLM** — even tiny 1B models will crawl on CPU-only with 16GB RAM (system uses ~6GB, leaves ~10GB, model needs 4-8GB + inference overhead = will swap to disk = unusable)
- **Heavy Docker stacks** — 5+ containers simultaneously will eat RAM

### ✅ Revised Strategy
| Original Plan | New Plan |
|---------------|----------|
| Ollama + Mistral 7B locally | **Groq Cloud API (free tier, LPU acceleration)** |
| sentence-transformers locally | **Keep** — runs fine on CPU (model is only ~90MB) |
| Redis in Docker | **Keep** — lightweight (~50MB RAM) |
| ChromaDB | **Keep** — file-based, very lightweight |
| Full Docker Compose (5 services) | Run backend + frontend natively in dev; Docker for final demo only |
| Prometheus + Grafana in Docker | Lightweight — keep but run only during demo |

### Free LLM API Options:

| Provider | Free Tier | Speed | Best For |
|----------|-----------|-------|----------|
| **Groq API (Selected)** | 30 RPM, 14.4K requests/day | Extremely fast (500+ tok/s) | Best inference speed & high rate limits |
| **Google Gemini API** | 15 RPM, 1M tokens/day | Fast | Fallback option |
| **Together AI** | $5 free credit | Fast | Alternative open-source models |
| **HuggingFace Inference API** | Rate-limited free | Slow | Backup option |

> **Recommendation**: Use **Groq API** — ultra-fast LPU inference (LLaMA 3.3 70B & LLaMA 3.1 8B), generous limits (30 req/min, 14,400 req/day), much less restrictive than Gemini, and OpenAI-compatible SDK. Get your free key at [Groq Console](https://console.groq.com/keys).

---

## 📅 Phase Schedule

| Phase | Days | What Gets Built | Subject Coverage |
|-------|------|-----------------|------------------|
| **Phase 1** | Day 1 (Sep 29) | Project setup, backend skeleton, DB, document upload | ASD&D (Git), CN (checksum) |
| **Phase 2** | Day 2 (Sep 30) | RAG pipeline, CAG cache, Groq LLM integration | AISC (Exp 9-12) |
| **Phase 3** | Day 3-4 (Oct 1-2) | AI/ML layer: search, perceptron, fuzzy, neuro-fuzzy | AISC (Exp 1,3,4,7,8,13-15) |
| **Phase 4** | Day 5 (Oct 3) | Frontend: chat UI, analytics dashboard, admin | Stats (Exp 1-12), WMC, CN |
| **Phase 5** | Day 6 (Oct 4) | DevOps: Docker, CI/CD, K8s, Terraform, Ansible, monitoring | ASD&D (Exp 1-14) |
| **Phase 6** | Day 7 (Oct 5) | Documentation, testing, Jupyter notebooks, final polish | All subjects |

---

## 🔧 Prerequisites (Human does this ONCE before Phase 1)

You need to do these manual steps (Flash can't do logins):

### 1. Get Groq API Key
1. Go to https://console.groq.com/keys
2. Sign up / Log in and click "Create API Key"
3. Copy the key (starts with `gsk_...`)
4. Create file `d:\Engineering\Projects\CampusMind\.env` (or copy `.env.example`):
```
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2. Ensure Python is available
Your system already has Python 3.14. ✅

### 3. Ensure Node.js is available
Flash will check and install if needed.

That's it. Everything else is automated.

---

---

# PHASE 1: Project Setup & Backend Skeleton
**Day 1 (Sep 29) | ~3-4 hours of Flash execution**

## What gets built
- Git repository initialized
- Complete folder structure
- Python virtual environment
- FastAPI backend with database models
- Document upload with checksum validation
- Health check endpoints

## Prompt for Flash — Phase 1

> Copy-paste this ENTIRE block as the prompt to Flash:

---

```
READ THIS ENTIRE PROMPT BEFORE STARTING. Do not improvise. Follow exactly.

## PROJECT: CampusMind — Phase 1: Project Setup & Backend Skeleton

### System Info
- OS: Windows 11
- Python: 3.14 (already installed, use `python` command)
- Working directory: d:\Engineering\Projects\CampusMind
- The .env file has GROQ_API_KEY (see .env.example)

### STEP 1: Create folder structure
Run these commands:

```powershell
cd d:\Engineering\Projects\CampusMind
mkdir -p backend/routers, backend/services, backend/ml, backend/fuzzy, backend/network, backend/tests
mkdir -p frontend, devops/ansible/roles/app/tasks, devops/kubernetes, devops/terraform
mkdir -p devops/prometheus, devops/grafana/dashboards, devops/airflow/dags, devops/mlflow
mkdir -p .github/workflows, docs, data/sample_documents, data/query_logs, stats_notebooks
```

### STEP 2: Initialize Git
```powershell
cd d:\Engineering\Projects\CampusMind
git init
```

Create `.gitignore`:
```
__pycache__/
*.pyc
.env
venv/
node_modules/
.next/
chroma_db/
*.db
*.sqlite3
.pytest_cache/
dist/
build/
mlruns/
```

### STEP 3: Create Python virtual environment
```powershell
cd d:\Engineering\Projects\CampusMind\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### STEP 4: Create requirements.txt
File: `backend/requirements.txt`
```
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic-settings==2.7.1
sqlalchemy==2.0.36
sentence-transformers==3.3.1
chromadb==0.5.23
redis==5.2.1
httpx==0.28.1
python-multipart==0.0.18
PyMuPDF==1.25.1
numpy==2.2.1
scipy==1.15.0
scikit-learn==1.6.1
prometheus-fastapi-instrumentator==7.0.2
psutil==6.1.1
websockets==14.1
pytest==8.3.4
python-dotenv==1.0.1
google-generativeai==0.8.5
```

Install:
```powershell
pip install -r requirements.txt
```

### STEP 5: Create backend/config.py
```python
"""Application configuration. All settings in one place."""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class Settings(BaseSettings):
    APP_NAME: str = "CampusMind"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./campusmind.db"

    # Groq Cloud API (ultra-fast LPU inference — no local GPU needed)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Embeddings (runs on CPU — only ~90MB model)
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # ChromaDB (file-based, no server needed)
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION: str = "academic_docs"

    # Redis (for CAG cache)
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600

    class Config:
        env_file = "../.env"

settings = Settings()
```

### STEP 6: Create backend/database.py
```python
"""SQLite database setup."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### STEP 7: Create backend/models.py
```python
"""Database models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_hash = Column(String(64), nullable=False)
    chunk_count = Column(Integer, default=0)
    uploaded_at = Column(DateTime, server_default=func.now())
    file_size = Column(Integer)
    status = Column(String(20), default="processing")

class QueryLog(Base):
    __tablename__ = "query_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_text = Column(Text, nullable=False)
    response_text = Column(Text)
    response_time_ms = Column(Float)
    source = Column(String(10), default="rag")
    intent = Column(String(50))
    confidence_score = Column(Float)
    fuzzy_quality_score = Column(Float)
    user_rating = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())
    cached = Column(Boolean, default=False)
```

### STEP 8: Create backend/services/checksum_service.py
```python
"""
Checksum validation for document uploads.
Covers CN Experiment 5: Error detection (CRC, Checksum).
"""
import hashlib
import binascii

class ChecksumService:
    @staticmethod
    def sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def crc32(data: bytes) -> int:
        return binascii.crc32(data) & 0xFFFFFFFF

    @staticmethod
    def internet_checksum(data: bytes) -> int:
        """Internet checksum as used in TCP/UDP (RFC 1071)."""
        if len(data) % 2 == 1:
            data += b'\x00'
        total = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            total += word
        while total >> 16:
            total = (total & 0xFFFF) + (total >> 16)
        return ~total & 0xFFFF

    @staticmethod
    def verify_integrity(data: bytes, expected_hash: str) -> bool:
        return hashlib.sha256(data).hexdigest() == expected_hash
```

### STEP 9: Create backend/services/document_processor.py
```python
"""Document parsing and text chunking."""
import io
from config import settings

class DocumentProcessor:
    def process(self, content: bytes, filename: str) -> list[str]:
        if filename.lower().endswith(".pdf"):
            text = self._extract_pdf(content)
        else:
            text = content.decode("utf-8", errors="ignore")
        return self._chunk_text(text)

    def _extract_pdf(self, content: bytes) -> str:
        import fitz
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def _chunk_text(self, text: str) -> list[str]:
        words = text.split()
        chunks = []
        chunk_size = settings.CHUNK_SIZE
        overlap = settings.CHUNK_OVERLAP
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
            i += chunk_size - overlap
        return chunks
```

### STEP 10: Create backend/routers/health.py
```python
"""
Health check endpoints.
Covers CN Experiment 1 (networking study) and CN Experiment 2 (PING).
"""
from fastapi import APIRouter
import time
import socket
import httpx

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "ok", "message": "pong", "timestamp": time.time()}

@router.get("/services")
async def check_services():
    results = {}
    # Check Groq API
    try:
        headers = {}
        if settings.GROQ_API_KEY:
            headers["Authorization"] = f"Bearer {settings.GROQ_API_KEY}"
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("https://api.groq.com/openai/v1/models", headers=headers)
            results["groq_api"] = {"status": "reachable", "latency_ms": resp.elapsed.total_seconds() * 1000}
    except Exception as e:
        results["groq_api"] = {"status": "unreachable", "error": str(e)}

    # Check Redis
    try:
        import redis as r
        rc = r.Redis(host="localhost", port=6379, socket_timeout=2)
        start = time.time()
        rc.ping()
        results["redis"] = {"status": "up", "latency_ms": (time.time() - start) * 1000}
    except Exception as e:
        results["redis"] = {"status": "down", "error": str(e)}

    results["api"] = {"status": "up", "hostname": socket.gethostname()}
    return results

@router.get("/dns-lookup/{hostname}")
async def dns_lookup(hostname: str):
    """CN Experiment 10: DNS resolution."""
    try:
        ip = socket.gethostbyname(hostname)
        full_info = socket.getaddrinfo(hostname, None)
        return {
            "hostname": hostname,
            "ip": ip,
            "addresses": list(set(addr[4][0] for addr in full_info)),
        }
    except socket.gaierror as e:
        return {"hostname": hostname, "error": str(e)}
```

### STEP 11: Create backend/routers/network.py
```python
"""
Network diagnostics. Covers WMC Experiments 4,5,7,13 and CN Experiment 6.
"""
from fastapi import APIRouter, Request
import time
import psutil

router = APIRouter()

@router.get("/info")
async def network_info(request: Request):
    interfaces = {}
    for name, addrs in psutil.net_if_addrs().items():
        interfaces[name] = [{"family": str(a.family), "address": a.address} for a in addrs]
    return {
        "client_ip": request.client.host if request.client else "unknown",
        "server_interfaces": interfaces,
        "timestamp": time.time(),
    }

@router.get("/throughput-test")
async def throughput_test():
    """WMC Exp 7: Generate payload for throughput measurement."""
    start = time.time()
    payload_size = 1024 * 1024  # 1MB
    elapsed = time.time() - start
    return {
        "payload_size_bytes": payload_size,
        "server_generation_ms": elapsed * 1000,
        "server_timestamp": time.time(),
    }

@router.get("/latency")
async def measure_latency():
    return {"server_timestamp": time.time()}
```

### STEP 12: Create backend/routers/documents.py
```python
"""Document upload and management. Covers CN Exp 5 (checksum), CN Exp 9 (FTP/file transfer)."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Document
from services.checksum_service import ChecksumService
from services.document_processor import DocumentProcessor

router = APIRouter()
checksum_svc = ChecksumService()
doc_processor = DocumentProcessor()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    file_hash = checksum_svc.sha256(content)
    crc = checksum_svc.crc32(content)
    icksum = checksum_svc.internet_checksum(content)

    existing = db.query(Document).filter(Document.file_hash == file_hash).first()
    if existing:
        raise HTTPException(status_code=409, detail="Document already exists (duplicate hash)")

    chunks = doc_processor.process(content, file.filename)

    doc = Document(
        filename=file.filename,
        file_hash=file_hash,
        chunk_count=len(chunks),
        file_size=len(content),
        status="pending_embedding"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "id": doc.id,
        "filename": file.filename,
        "chunks": len(chunks),
        "sha256": file_hash,
        "crc32": hex(crc),
        "internet_checksum": hex(icksum),
        "status": doc.status,
    }

@router.get("/list")
async def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return [{"id": d.id, "filename": d.filename, "chunks": d.chunk_count,
             "size": d.file_size, "status": d.status} for d in docs]

@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(doc)
    db.commit()
    return {"message": f"Deleted document {doc_id}"}
```

### STEP 13: Create backend/main.py
```python
"""CampusMind Backend API Server."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables
from routers import health, network, documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="CampusMind API",
    description="AI-Powered Academic RAG Chatbot",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
```

### STEP 14: Create empty __init__.py files
Create empty `__init__.py` in these directories:
- backend/routers/__init__.py
- backend/services/__init__.py
- backend/ml/__init__.py
- backend/fuzzy/__init__.py
- backend/network/__init__.py

### STEP 15: Test the server
```powershell
cd d:\Engineering\Projects\CampusMind\backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

Then open browser: http://localhost:8000/docs
Verify all endpoints show up in Swagger UI.
Test the /api/health/ping endpoint — should return {"status": "ok"}.

### STEP 16: Git commit
```powershell
cd d:\Engineering\Projects\CampusMind
git add -A
git commit -m "Phase 1: Project setup, backend skeleton, document upload with checksum"
```

### SUCCESS CRITERIA for Phase 1:
- [ ] Server starts without errors on port 8000
- [ ] /api/health/ping returns {"status": "ok"}
- [ ] /api/documents/upload accepts a file and returns checksums
- [ ] /api/health/dns-lookup/google.com returns IP addresses
- [ ] SQLite database file is created
- [ ] Git repo has initial commit
```

---

# PHASE 2: RAG Pipeline, CAG Cache & LLM Integration
**Day 2 (Sep 30) | ~3-4 hours**

## What gets built
- Embedding service (sentence-transformers on CPU)
- ChromaDB vector database integration
- RAG pipeline (retrieve + generate)
- CAG cache layer with Redis
- LLM service using Groq API (LLaMA 3.3 70B / 3.1 8B)
- Chat endpoints (REST + WebSocket)

## Prompt for Flash — Phase 2

> Copy-paste this ENTIRE block as the prompt to Flash:

---

```
READ THIS ENTIRE PROMPT BEFORE STARTING. Do not improvise. Follow exactly.

## PROJECT: CampusMind — Phase 2: RAG + CAG + Groq LLM Integration

### Context
Phase 1 is complete. The backend skeleton is at d:\Engineering\Projects\CampusMind\backend.
The .env file has GROQ_API_KEY set.
The virtual environment is at backend/venv.

Always activate venv first:
```powershell
cd d:\Engineering\Projects\CampusMind\backend
.\venv\Scripts\Activate.ps1
```

### STEP 1: Install Redis locally (Docker)
```powershell
docker pull redis:7-alpine
docker run -d --name campusmind-redis -p 6379:6379 redis:7-alpine
```
If Docker is not installed, install Docker Desktop from https://www.docker.com/products/docker-desktop/
After install, the user will need to log in / accept terms. Then retry the commands.

### STEP 2: Create backend/services/embedding_service.py
```python
"""Embedding service using sentence-transformers. Runs on CPU (~90MB model)."""
from sentence_transformers import SentenceTransformer
from config import settings

class EmbeddingService:
    _instance = None
    _model = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer(settings.EMBEDDING_MODEL)
        return cls._model

    @classmethod
    def encode(cls, texts: list[str]) -> list[list[float]]:
        model = cls.get_model()
        embeddings = model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    @classmethod
    def encode_single(cls, text: str) -> list[float]:
        model = cls.get_model()
        return model.encode(text, show_progress_bar=False).tolist()
```

### STEP 3: Create backend/services/llm_service.py
```python
"""
LLM Service using Groq API (free tier).
Ultra-fast LPU inference, NO local GPU needed. Covers AISC Exp 9 (GenAI) and Exp 10 (small LMs).
"""
from groq import AsyncGroq
from config import settings

class LLMService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        """Generate complete response."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"Error generating response: {str(e)}"

    async def stream_generate(self, prompt: str):
        """Stream response for WebSocket."""
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.3,
                stream=True,
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"Error: {str(e)}"
```

### STEP 4: Create backend/services/rag_service.py
```python
"""
RAG (Retrieval-Augmented Generation) Service.
AISC Exp 11: RAG Framework for Contextual Question Answering.
"""
import chromadb
from config import settings
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService

class RAGService:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
        self.llm = LLMService()

    async def query(self, query_text: str, top_k: int = 5) -> dict:
        query_embedding = EmbeddingService.encode_single(query_text)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        documents = results["documents"][0] if results["documents"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        distances = results["distances"][0] if results["distances"] else []

        context = "\n\n---\n\n".join(documents[:5])

        prompt = f"""You are CampusMind, an intelligent academic assistant chatbot for university students.
Answer the question based ONLY on the provided context from academic documents.
If the context doesn't contain the answer, say "I don't have enough information from the uploaded documents to answer this question."
Be concise but thorough. Use bullet points for clarity when appropriate.

Context from academic documents:
{context if context else "No documents have been uploaded yet."}

Student's Question: {query_text}

Answer:"""

        answer = await self.llm.generate(prompt)

        confidence = 0.0
        if distances:
            avg_similarity = 1 - (sum(distances) / len(distances))
            confidence = min(max(avg_similarity, 0.0), 1.0)

        sources = [m.get("source", "unknown") for m in metadatas[:5]]

        return {"answer": answer, "sources": sources, "confidence": round(confidence, 3)}

    async def stream_query(self, query_text: str, top_k: int = 5):
        query_embedding = EmbeddingService.encode_single(query_text)
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k,
            include=["documents"]
        )
        documents = results["documents"][0] if results["documents"] else []
        context = "\n\n---\n\n".join(documents[:5])

        prompt = f"""You are CampusMind, an academic assistant. Answer based on context.

Context: {context if context else "No documents uploaded."}

Question: {query_text}

Answer:"""

        async for chunk in self.llm.stream_generate(prompt):
            yield chunk

    def add_documents(self, chunks: list[dict]):
        texts = [c["text"] for c in chunks]
        embeddings = EmbeddingService.encode(texts)
        ids = [f"chunk_{c['doc_id']}_{c['chunk_idx']}" for c in chunks]
        metadatas = [{"source": c["source"], "chunk_idx": c["chunk_idx"]} for c in chunks]
        self.collection.add(
            documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas
        )
```

### STEP 5: Create backend/services/cag_service.py
```python
"""
CAG (Cache-Augmented Generation) Service.
AISC Exp 12: Cache layer for instant retrieval of repeated queries.
"""
import redis
import json
import hashlib
from config import settings

class CAGService:
    def __init__(self):
        try:
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.redis_client.ping()
            self.available = True
        except Exception:
            self.available = False

    def _hash_query(self, query: str) -> str:
        normalized = query.strip().lower()
        return f"cag:{hashlib.md5(normalized.encode()).hexdigest()}"

    def get_cached(self, query: str) -> dict | None:
        if not self.available:
            return None
        try:
            key = self._hash_query(query)
            cached = self.redis_client.get(key)
            return json.loads(cached) if cached else None
        except Exception:
            return None

    def cache_response(self, query: str, response: dict):
        if not self.available:
            return
        try:
            key = self._hash_query(query)
            self.redis_client.setex(key, settings.CACHE_TTL, json.dumps(response))
        except Exception:
            pass

    def get_cache_stats(self) -> dict:
        if not self.available:
            return {"available": False}
        try:
            info = self.redis_client.info("stats")
            hits = info.get("keyspace_hits", 0)
            misses = info.get("keyspace_misses", 0)
            return {
                "available": True,
                "hits": hits, "misses": misses,
                "hit_rate": round(hits / max(hits + misses, 1), 3)
            }
        except Exception:
            return {"available": False}
```

### STEP 6: Create backend/routers/chat.py
```python
"""
Chat router: REST + WebSocket for real-time streaming.
Covers: AISC Exp 9,10,11,12 | CN Exp 8 (Socket Programming)
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import QueryLog
from services.rag_service import RAGService
from services.cag_service import CAGService
import time
import json

router = APIRouter()

# Initialize services (singletons)
rag_service = None
cag_service = None

def get_rag():
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service

def get_cag():
    global cag_service
    if cag_service is None:
        cag_service = CAGService()
    return cag_service

class ChatRequest(BaseModel):
    query: str
    use_cache: bool = True

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
    response_time_ms: float
    cached: bool

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest, db: Session = Depends(get_db)):
    start = time.time()
    cag = get_cag()
    rag = get_rag()

    # Try cache first (AISC Exp 12: CAG)
    if request.use_cache:
        cached = cag.get_cached(request.query)
        if cached:
            elapsed = (time.time() - start) * 1000
            log = QueryLog(
                query_text=request.query, response_text=cached["answer"],
                response_time_ms=elapsed, source="cag",
                confidence_score=cached["confidence"], cached=True
            )
            db.add(log); db.commit()
            return ChatResponse(
                answer=cached["answer"], sources=cached["sources"],
                confidence=cached["confidence"],
                response_time_ms=round(elapsed, 2), cached=True
            )

    # RAG pipeline (AISC Exp 11)
    result = await rag.query(request.query)
    elapsed = (time.time() - start) * 1000

    # Cache the result (AISC Exp 12)
    cag.cache_response(request.query, result)

    # Log for stats analytics
    log = QueryLog(
        query_text=request.query, response_text=result["answer"],
        response_time_ms=elapsed, source="rag",
        confidence_score=result["confidence"], cached=False
    )
    db.add(log); db.commit()

    return ChatResponse(
        answer=result["answer"], sources=result["sources"],
        confidence=result["confidence"],
        response_time_ms=round(elapsed, 2), cached=False
    )

@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """WebSocket for real-time streaming. CN Exp 8: Socket Programming."""
    await websocket.accept()
    rag = get_rag()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            query = msg.get("query", "")
            async for chunk in rag.stream_query(query):
                await websocket.send_json({"type": "chunk", "content": chunk})
            await websocket.send_json({"type": "done", "content": ""})
    except WebSocketDisconnect:
        pass
```

### STEP 7: Update backend/routers/documents.py
Add RAG integration to the upload endpoint. After creating the Document record, also embed and store in ChromaDB:

Add this import at the top:
```python
from services.rag_service import RAGService
```

In the upload_document function, after `db.refresh(doc)`, add:
```python
    # Embed and store in vector DB
    try:
        rag = RAGService()
        chunk_dicts = [
            {"text": c, "doc_id": doc.id, "chunk_idx": i, "source": file.filename}
            for i, c in enumerate(chunks)
        ]
        rag.add_documents(chunk_dicts)
        doc.status = "embedded"
        db.commit()
    except Exception as e:
        doc.status = f"embedding_failed: {str(e)[:100]}"
        db.commit()
```

### STEP 8: Update backend/main.py
Add the chat router import and registration:
```python
from routers import health, network, documents, chat

# Add this line after other router includes:
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
```

### STEP 9: Test the full pipeline
1. Start Redis: `docker start campusmind-redis`
2. Start backend: `cd backend && .\venv\Scripts\Activate.ps1 && uvicorn main:app --reload --port 8000`
3. Open http://localhost:8000/docs
4. Upload a PDF via /api/documents/upload (use one of the syllabus PDFs in the project root)
5. Ask a question via /api/chat/query with body: {"query": "What is RAG?"}
6. Verify the response contains an answer, sources, and confidence score

### STEP 10: Git commit
```powershell
cd d:\Engineering\Projects\CampusMind
git add -A
git commit -m "Phase 2: RAG pipeline, CAG cache, Groq LLM integration, WebSocket chat"
```

### SUCCESS CRITERIA for Phase 2:
- [ ] Documents can be uploaded and embedded in ChromaDB
- [ ] /api/chat/query returns AI-generated answers with sources
- [ ] Second identical query is served from cache (cached: true)
- [ ] WebSocket endpoint /api/chat/ws accepts connections
- [ ] Redis is running and cache stats show hits
```

---

# PHASE 3: AI/ML Layer — Search, Perceptron, Fuzzy, Neuro-Fuzzy
**Day 3-4 (Oct 1-2) | ~4-5 hours**

## What gets built
- BFS/DFS/A* search algorithms for document graph
- Perceptron-based intent classifier
- Mamdani & Sugeno Fuzzy Inference Systems
- ANFIS Neuro-Fuzzy hybrid system
- Integration into chat pipeline

## Prompt for Flash — Phase 3

> Copy-paste this ENTIRE block as the prompt to Flash:

---

```
READ THIS ENTIRE PROMPT BEFORE STARTING.

## PROJECT: CampusMind — Phase 3: AI/ML Layer (Search, Perceptron, Fuzzy, Neuro-Fuzzy)

### Context
Phases 1-2 complete. Backend at d:\Engineering\Projects\CampusMind\backend.
RAG + CAG working. Now add the AI/ML components for AISC experiments.

Activate venv: cd d:\Engineering\Projects\CampusMind\backend && .\venv\Scripts\Activate.ps1

### STEP 1: Create backend/services/search_service.py
```python
"""
Graph-based document search using BFS, DFS, and A*.
AISC Exp 3: Uninformed search (BFS, DFS)
AISC Exp 4: Informed search (A*)
"""
import heapq
from collections import deque
import numpy as np

class SearchService:
    def build_adjacency(self, documents: list[str], embeddings: list[list[float]], threshold: float = 0.7) -> dict:
        """Build document chunk graph based on embedding similarity."""
        adjacency = {i: [] for i in range(len(documents))}
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]) + 1e-10
                )
                if sim >= threshold:
                    adjacency[i].append(j)
                    adjacency[j].append(i)
        return adjacency

    def bfs_search(self, start: int, adjacency: dict, max_nodes: int = 10) -> list[int]:
        """BFS traversal of document graph. AISC Exp 3."""
        visited = set()
        queue = deque([start])
        result = []
        while queue and len(result) < max_nodes:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in adjacency.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
        return result

    def dfs_search(self, start: int, adjacency: dict, max_nodes: int = 10) -> list[int]:
        """DFS traversal of document graph. AISC Exp 3."""
        visited = set()
        stack = [start]
        result = []
        while stack and len(result) < max_nodes:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in reversed(adjacency.get(node, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return result

    def a_star_search(self, query_embedding: list[float], doc_embeddings: list[list[float]],
                      documents: list[str], top_k: int = 5) -> list[dict]:
        """
        A* search: rank documents by f(n) = g(n) + h(n).
        g(n) = exploration cost (order discovered)
        h(n) = cosine distance to query (heuristic)
        AISC Exp 4.
        """
        heap = []
        query_vec = np.array(query_embedding)
        for i, emb in enumerate(doc_embeddings):
            emb_vec = np.array(emb)
            cosine_dist = 1 - np.dot(query_vec, emb_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(emb_vec) + 1e-10
            )
            g = i * 0.05
            h = cosine_dist
            f = g + h
            heapq.heappush(heap, (f, i))

        results = []
        while heap and len(results) < top_k:
            f_val, idx = heapq.heappop(heap)
            results.append({
                "index": idx,
                "document": documents[idx],
                "f_score": round(f_val, 4),
                "relevance": round(1 - f_val, 4),
            })
        return results
```

### STEP 2: Create backend/services/intent_classifier.py
```python
"""
Intent Classifier using Perceptron.
AISC Exp 7: Perceptron for AND/OR/XOR → extended to intent classification.
AISC Exp 8: Supervised/Unsupervised NN learning.
"""
import numpy as np
from services.embedding_service import EmbeddingService

class Perceptron:
    """Multi-class Perceptron classifier. AISC Exp 7."""

    def __init__(self, input_dim: int, num_classes: int):
        self.weights = np.random.randn(num_classes, input_dim) * 0.01
        self.bias = np.zeros(num_classes)

    def predict(self, x: np.ndarray) -> int:
        scores = self.weights @ x + self.bias
        return int(np.argmax(scores))

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        scores = self.weights @ x + self.bias
        exp_scores = np.exp(scores - np.max(scores))
        return exp_scores / exp_scores.sum()

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, lr: float = 0.01):
        for _ in range(epochs):
            for xi, yi in zip(X, y):
                pred = self.predict(xi)
                if pred != yi:
                    self.weights[yi] += lr * xi
                    self.bias[yi] += lr
                    self.weights[pred] -= lr * xi
                    self.bias[pred] -= lr


class IntentClassifier:
    INTENTS = ["academic", "general", "feedback", "greeting"]

    def __init__(self):
        self.perceptron = Perceptron(input_dim=384, num_classes=len(self.INTENTS))
        self._train_default()

    def _train_default(self):
        training_data = {
            "academic": [
                "What is binary search tree?", "Explain neural networks",
                "Define polymorphism in OOP", "How does TCP work?",
                "What are sorting algorithms?", "Explain OSI model",
                "What is machine learning?", "Define encapsulation",
                "How does HTTP work?", "What is a database index?",
            ],
            "general": [
                "What time is the exam?", "Where is the library?",
                "Who is the HOD?", "What are the holidays?",
                "When is the submission deadline?", "Where is room 301?",
            ],
            "feedback": [
                "This answer was helpful", "That was wrong",
                "Good answer", "Not useful", "Thanks for helping",
                "Could be better", "Great response",
            ],
            "greeting": [
                "Hello", "Hi there", "Good morning", "Hey",
                "Hi", "Good evening", "What's up",
            ],
        }

        texts, labels = [], []
        for intent, examples in training_data.items():
            for ex in examples:
                texts.append(ex)
                labels.append(self.INTENTS.index(intent))

        X = np.array(EmbeddingService.encode(texts))
        y = np.array(labels)
        self.perceptron.train(X, y, epochs=300, lr=0.01)

    def classify(self, query: str) -> dict:
        embedding = np.array(EmbeddingService.encode_single(query))
        idx = self.perceptron.predict(embedding)
        proba = self.perceptron.predict_proba(embedding)
        return {
            "intent": self.INTENTS[idx],
            "confidence": round(float(proba[idx]), 3),
            "all_scores": {self.INTENTS[i]: round(float(p), 3) for i, p in enumerate(proba)},
        }
```

### STEP 3: Create backend/fuzzy/membership_functions.py
```python
"""Fuzzy membership functions. AISC Exp 13: Fuzzy Logic Controller."""
import numpy as np

class MembershipFunction:
    @staticmethod
    def triangular(x: float, a: float, b: float, c: float) -> float:
        if x <= a or x >= c: return 0.0
        elif x <= b: return (x - a) / (b - a) if b != a else 1.0
        else: return (c - x) / (c - b) if c != b else 1.0

    @staticmethod
    def trapezoidal(x: float, a: float, b: float, c: float, d: float) -> float:
        if x <= a or x >= d: return 0.0
        elif a < x <= b: return (x - a) / (b - a) if b != a else 1.0
        elif b < x <= c: return 1.0
        else: return (d - x) / (d - c) if d != c else 1.0

    @staticmethod
    def gaussian(x: float, mean: float, sigma: float) -> float:
        return float(np.exp(-0.5 * ((x - mean) / max(sigma, 1e-6)) ** 2))
```

### STEP 4: Create backend/fuzzy/mamdani_fis.py
```python
"""
Mamdani Fuzzy Inference System for response quality scoring.
AISC Exp 13: Fuzzy Logic Controller
AISC Exp 14: Mamdani FIS implementation

Inputs: confidence (0-1), response_length (0-2000), source_count (0-10)
Output: quality_score (0-1)
"""
import numpy as np
from fuzzy.membership_functions import MembershipFunction as MF

class MamdaniFIS:
    def fuzzify_confidence(self, val: float) -> dict:
        return {
            "low": MF.trapezoidal(val, 0, 0, 0.3, 0.5),
            "medium": MF.triangular(val, 0.3, 0.5, 0.7),
            "high": MF.trapezoidal(val, 0.5, 0.7, 1.0, 1.0),
        }

    def fuzzify_length(self, val: float) -> dict:
        return {
            "short": MF.trapezoidal(val, 0, 0, 50, 200),
            "medium": MF.triangular(val, 100, 500, 1000),
            "long": MF.trapezoidal(val, 800, 1200, 2000, 2000),
        }

    def fuzzify_sources(self, val: float) -> dict:
        return {
            "few": MF.trapezoidal(val, 0, 0, 1, 2),
            "some": MF.triangular(val, 1, 3, 5),
            "many": MF.trapezoidal(val, 3, 5, 10, 10),
        }

    def evaluate_rules(self, conf: dict, length: dict, sources: dict) -> dict:
        return {
            "excellent": max(min(conf["high"], sources["many"]),
                           min(conf["high"], length["long"])),
            "good": min(conf["medium"], sources["some"]),
            "poor": max(max(conf["low"], sources["few"]), length["short"]),
        }

    def defuzzify(self, output: dict) -> float:
        x = np.linspace(0, 1, 100)
        aggregated = np.zeros_like(x)
        for i, xi in enumerate(x):
            poor = min(output["poor"], MF.trapezoidal(xi, 0, 0, 0.2, 0.4))
            good = min(output["good"], MF.triangular(xi, 0.3, 0.5, 0.7))
            excellent = min(output["excellent"], MF.trapezoidal(xi, 0.6, 0.8, 1.0, 1.0))
            aggregated[i] = max(poor, good, excellent)
        total = np.sum(aggregated)
        if total == 0: return 0.5
        return float(np.sum(x * aggregated) / total)

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        conf = self.fuzzify_confidence(confidence)
        length = self.fuzzify_length(float(response_length))
        sources = self.fuzzify_sources(float(source_count))
        output = self.evaluate_rules(conf, length, sources)
        return round(self.defuzzify(output), 3)
```

### STEP 5: Create backend/fuzzy/sugeno_fis.py
```python
"""
Sugeno Fuzzy Inference System. AISC Exp 14.
Unlike Mamdani (output is fuzzy set), Sugeno output is a linear function.
"""
from fuzzy.membership_functions import MembershipFunction as MF

class SugenoFIS:
    def fuzzify_confidence(self, val: float) -> dict:
        return {
            "low": MF.trapezoidal(val, 0, 0, 0.3, 0.5),
            "medium": MF.triangular(val, 0.3, 0.5, 0.7),
            "high": MF.trapezoidal(val, 0.5, 0.7, 1.0, 1.0),
        }

    def fuzzify_sources(self, val: float) -> dict:
        return {
            "few": MF.trapezoidal(val, 0, 0, 1, 3),
            "many": MF.trapezoidal(val, 2, 4, 10, 10),
        }

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        conf = self.fuzzify_confidence(confidence)
        src = self.fuzzify_sources(float(source_count))
        norm_len = min(response_length / 2000.0, 1.0)

        # Sugeno: output = linear function of inputs
        # Rule 1: IF conf IS high AND sources IS many THEN z1 = 0.5*conf + 0.3*norm_len + 0.2*src_norm
        z1 = 0.5 * confidence + 0.3 * norm_len + 0.2 * min(source_count / 10, 1)
        w1 = min(conf["high"], src["many"])

        # Rule 2: IF conf IS medium THEN z2 = 0.4*conf + 0.3*norm_len + 0.1
        z2 = 0.4 * confidence + 0.3 * norm_len + 0.1
        w2 = conf["medium"]

        # Rule 3: IF conf IS low OR sources IS few THEN z3 = 0.2*conf + 0.1
        z3 = 0.2 * confidence + 0.1
        w3 = max(conf["low"], src["few"])

        total_w = w1 + w2 + w3
        if total_w == 0: return 0.5
        return round(float((w1 * z1 + w2 * z2 + w3 * z3) / total_w), 3)
```

### STEP 6: Create backend/fuzzy/neurofuzzy.py
```python
"""
ANFIS-style Hybrid Neuro-Fuzzy System. AISC Exp 15.
Combines neural network learning with fuzzy inference.
"""
import numpy as np

class ANFISLayer:
    def __init__(self, n_inputs: int = 3, n_rules: int = 4):
        self.n_inputs = n_inputs
        self.n_rules = n_rules
        self.means = np.random.randn(n_rules, n_inputs) * 0.3 + 0.5
        self.sigmas = np.abs(np.random.randn(n_rules, n_inputs) * 0.2) + 0.15
        self.consequent = np.random.randn(n_rules, n_inputs + 1) * 0.1
        self.lr = 0.01

    def gaussian_mf(self, x, mean, sigma):
        return np.exp(-0.5 * ((x - mean) / max(sigma, 1e-6)) ** 2)

    def forward(self, x: np.ndarray) -> float:
        mu = np.zeros((self.n_rules, self.n_inputs))
        for i in range(self.n_rules):
            for j in range(self.n_inputs):
                mu[i, j] = self.gaussian_mf(x[j], self.means[i, j], self.sigmas[i, j])
        w = np.prod(mu, axis=1)
        w_sum = np.sum(w) + 1e-10
        w_norm = w / w_sum
        x_aug = np.append(x, 1.0)
        rule_outputs = self.consequent @ x_aug
        output = np.sum(w_norm * rule_outputs)
        return float(np.clip(output, 0, 1))

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100):
        for epoch in range(epochs):
            for xi, yi in zip(X, y):
                pred = self.forward(xi)
                error = yi - pred
                x_aug = np.append(xi, 1.0)
                for r in range(self.n_rules):
                    self.consequent[r] += self.lr * error * x_aug * 0.25


class NeuroFuzzyScorer:
    def __init__(self):
        self.anfis = ANFISLayer(n_inputs=3, n_rules=4)
        self._pretrain()

    def _pretrain(self):
        np.random.seed(42)
        X = np.random.rand(300, 3)
        y = 0.5 * X[:, 0] + 0.2 * np.clip(X[:, 1], 0.2, 0.8) + 0.3 * X[:, 2]
        y = np.clip(y + np.random.randn(300) * 0.03, 0, 1)
        self.anfis.train(X, y, epochs=150)

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        x = np.array([confidence, min(response_length / 2000, 1), min(source_count / 10, 1)])
        return round(self.anfis.forward(x), 3)
```

### STEP 7: Create backend/services/fuzzy_service.py
```python
"""Wrapper combining Mamdani + Sugeno + NeuroFuzzy. AISC Exp 13,14,15."""
from fuzzy.mamdani_fis import MamdaniFIS
from fuzzy.sugeno_fis import SugenoFIS
from fuzzy.neurofuzzy import NeuroFuzzyScorer

class FuzzyQualityScorer:
    def __init__(self):
        self.mamdani = MamdaniFIS()
        self.sugeno = SugenoFIS()
        self.neurofuzzy = NeuroFuzzyScorer()

    def score(self, confidence: float, response_length: int, source_count: int) -> dict:
        m = self.mamdani.score(confidence, response_length, source_count)
        s = self.sugeno.score(confidence, response_length, source_count)
        nf = self.neurofuzzy.score(confidence, response_length, source_count)
        combined = round((m + s + nf) / 3, 3)
        return {
            "mamdani": m, "sugeno": s, "neurofuzzy": nf,
            "combined": combined,
        }
```

### STEP 8: Update backend/routers/chat.py
Add intent classification and fuzzy scoring to the chat pipeline.

Add these imports at the top:
```python
from services.intent_classifier import IntentClassifier
from services.fuzzy_service import FuzzyQualityScorer
```

Add singletons:
```python
intent_classifier = None
fuzzy_scorer = None

def get_intent():
    global intent_classifier
    if intent_classifier is None:
        intent_classifier = IntentClassifier()
    return intent_classifier

def get_fuzzy():
    global fuzzy_scorer
    if fuzzy_scorer is None:
        fuzzy_scorer = FuzzyQualityScorer()
    return fuzzy_scorer
```

Update ChatResponse model to include new fields:
```python
class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
    response_time_ms: float
    cached: bool
    intent: dict = {}
    fuzzy_scores: dict = {}
```

In chat_query function, add after getting the RAG result:
```python
    # Classify intent (AISC Exp 7,8)
    intent_result = get_intent().classify(request.query)

    # Fuzzy quality scoring (AISC Exp 13,14,15)
    fuzzy_result = get_fuzzy().score(
        confidence=result["confidence"],
        response_length=len(result["answer"]),
        source_count=len(result["sources"])
    )
```

And include in the response and log:
```python
    log.intent = intent_result["intent"]
    log.fuzzy_quality_score = fuzzy_result["combined"]
```

Return with intent and fuzzy_scores in ChatResponse.

### STEP 9: Create PEAS formulation document
File: docs/peas_formulation.md
```markdown
# PEAS Formulation — CampusMind (AISC Experiment 1)

## Problem Statement
Design an intelligent academic chatbot for university students that answers questions from uploaded course materials.

## PEAS Model

| Component | Description |
|-----------|-------------|
| **Performance** | Response accuracy, relevance (confidence score), response time, user satisfaction, cache hit rate, fuzzy quality score |
| **Environment** | University academic setting, uploaded PDFs/notes, diverse student queries, Wi-Fi/mobile network, varying network quality |
| **Actuators** | Generated text responses, source citations, confidence scores, quality ratings, network diagnostics |
| **Sensors** | Natural language queries, document uploads, user feedback ratings, network status, query intent |

## Agent Type
- **Type**: Goal-based agent with learning capability
- **Architecture**: RAG (Retrieval-Augmented Generation) with cache augmentation
- **Learning**: Perceptron-based intent classifier improves with more data
- **Reasoning**: Fuzzy inference for quality assessment
```

### STEP 10: Git commit
```powershell
cd d:\Engineering\Projects\CampusMind
git add -A
git commit -m "Phase 3: Search algorithms, Perceptron intent classifier, Fuzzy (Mamdani+Sugeno), Neuro-Fuzzy ANFIS"
```

### SUCCESS CRITERIA for Phase 3:
- [ ] /api/chat/query now returns intent classification and fuzzy scores
- [ ] Fuzzy scores show mamdani, sugeno, neurofuzzy, combined values
- [ ] Intent correctly classifies "Hello" as greeting, "What is TCP?" as academic
- [ ] docs/peas_formulation.md exists
- [ ] No import errors when starting the server
```

---

# PHASE 4: Frontend — Chat UI, Analytics Dashboard, Admin
**Day 5 (Oct 3) | ~4-5 hours**

## What gets built
- Next.js app with dark theme premium UI
- Real-time chat interface with WebSocket streaming
- Analytics dashboard with charts (Stats experiments)
- Admin panel for document upload
- Network status indicator (WMC experiments)

## Prompt for Flash — Phase 4

> Copy-paste this ENTIRE block as the prompt to Flash:

---

```
READ THIS ENTIRE PROMPT BEFORE STARTING.

## PROJECT: CampusMind — Phase 4: Frontend (Next.js)

### Context
Backend is running at http://localhost:8000. All APIs work.
Now build the frontend at d:\Engineering\Projects\CampusMind\frontend.

### STEP 1: Initialize Next.js
```powershell
cd d:\Engineering\Projects\CampusMind
npx -y create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --no-import-alias --yes
cd frontend
npm install recharts lucide-react
```

### STEP 2: Design Requirements (MANDATORY)

The UI MUST be premium dark-theme. Use these exact design tokens:
- Background: #0a0a1a (deep navy)
- Surface/Cards: #12122a with glassmorphism (backdrop-blur-xl, bg-opacity-60, border border-white/10)
- Primary: #7c3aed (violet)
- Accent: #06b6d4 (cyan)
- Success: #22c55e
- Warning: #f59e0b
- Error: #ef4444
- Text primary: #e2e8f0
- Text muted: #94a3b8
- Font: Inter from Google Fonts
- Border radius: 12px cards, 8px inputs, 24px buttons
- Subtle gradient backgrounds: from-violet-600/10 to-cyan-600/10
- Chat bubbles: User = violet right-aligned, Bot = surface left-aligned
- Smooth transitions: transition-all duration-200
- Hover effects on all interactive elements
- Loading skeletons/spinners during API calls

### STEP 3: Create these pages

#### Page 1: Landing Page (src/app/page.tsx)
- Hero section with "CampusMind" title, gradient text
- Subtitle: "AI-Powered Academic Assistant"
- 3 feature cards: Chat, Analytics, Admin
- Each card links to its page
- Animated gradient background

#### Page 2: Chat Page (src/app/chat/page.tsx)
- Full-height chat window
- Left sidebar showing uploaded documents
- Chat messages area (scrollable)
- Input bar at bottom with send button
- Each bot response shows: answer, sources, confidence, intent, fuzzy scores
- Network status indicator in top-right (uses Navigator.connection API)
- Real-time streaming via WebSocket when available, fallback to REST

#### Page 3: Analytics Dashboard (src/app/analytics/page.tsx)
- Top stats cards: Total Queries, Avg Response Time, Cache Hit Rate, Avg Confidence
- Charts (using recharts):
  - Bar chart: Response time distribution (histogram) — Stats Exp 1
  - Line chart: Response times over time
  - Pie chart: Intent distribution — Stats Exp 10
  - Scatter plot: Confidence vs Response Time
  - Bar chart: RAG vs CAG comparison — Stats Exp 5
- All data fetched from /api/analytics/* endpoints

#### Page 4: Admin Page (src/app/admin/page.tsx)
- Document upload: drag-drop zone
- Shows SHA256, CRC32, Internet Checksum after upload (CN Exp 5)
- Document list with delete option
- Service health status (from /api/health/services)
- Cache statistics (hits, misses, hit rate)
- Network diagnostics panel (from /api/network/info)

### STEP 4: Create components

Create each component in src/components/:
- Navbar.tsx — top navigation bar with logo and links
- ChatWindow.tsx — main chat area
- ChatMessage.tsx — individual message bubble (user/bot styling)
- ChatInput.tsx — text input with send button, loading state
- DocumentUpload.tsx — drag-drop file upload component
- AnalyticsCharts.tsx — all the recharts charts
- NetworkStatus.tsx — shows connection type (4G/WiFi), signal indicator
- Sidebar.tsx — document list sidebar for chat page
- StatCard.tsx — glassmorphism stat card for analytics

### STEP 5: Create hooks

src/hooks/useWebSocket.ts:
- Connect to ws://localhost:8000/api/chat/ws
- Handle streaming messages
- Reconnection logic
- Export: isConnected, streamingText, sendQuery, resetStream

src/hooks/useNetworkInfo.ts:
- Uses Navigator.connection API
- Returns: type (4g/3g/wifi), downlink, rtt
- Updates on change

### STEP 6: API client
src/lib/api.ts:
```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function sendChatQuery(query: string) {
  const res = await fetch(`${API_BASE}/api/chat/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, use_cache: true }),
  });
  return res.json();
}

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/api/documents/upload`, {
    method: 'POST',
    body: formData,
  });
  return res.json();
}

export async function getDocuments() {
  const res = await fetch(`${API_BASE}/api/documents/list`);
  return res.json();
}

export async function getQueryStats() {
  const res = await fetch(`${API_BASE}/api/analytics/query-stats`);
  return res.json();
}

export async function getResponseTimes() {
  const res = await fetch(`${API_BASE}/api/analytics/response-times`);
  return res.json();
}

export async function getHealthStatus() {
  const res = await fetch(`${API_BASE}/api/health/services`);
  return res.json();
}

export async function getNetworkInfo() {
  const res = await fetch(`${API_BASE}/api/network/info`);
  return res.json();
}
```

### STEP 7: Create analytics endpoint in backend
Before building frontend charts, create the missing analytics router.

File: backend/routers/analytics.py
```python
"""Analytics data endpoints for Stats experiments."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import QueryLog
import numpy as np

router = APIRouter()

@router.get("/query-stats")
async def get_query_stats(db: Session = Depends(get_db)):
    logs = db.query(QueryLog).all()
    if not logs:
        return {"total_queries": 0, "response_time": {}, "confidence": {}, "cache_rate": 0, "intent_distribution": {}}

    times = [l.response_time_ms for l in logs if l.response_time_ms]
    confs = [l.confidence_score for l in logs if l.confidence_score is not None]

    return {
        "total_queries": len(logs),
        "response_time": {
            "mean": round(float(np.mean(times)), 2) if times else 0,
            "median": round(float(np.median(times)), 2) if times else 0,
            "std": round(float(np.std(times)), 2) if times else 0,
            "min": round(float(np.min(times)), 2) if times else 0,
            "max": round(float(np.max(times)), 2) if times else 0,
        },
        "confidence": {
            "mean": round(float(np.mean(confs)), 3) if confs else 0,
        },
        "cache_rate": round(sum(1 for l in logs if l.cached) / max(len(logs), 1), 3),
        "intent_distribution": _count_intents(logs),
    }

def _count_intents(logs):
    counts = {}
    for l in logs:
        intent = l.intent or "unknown"
        counts[intent] = counts.get(intent, 0) + 1
    return counts

@router.get("/response-times")
async def get_response_times(db: Session = Depends(get_db)):
    logs = db.query(QueryLog).all()
    return {
        "rag_times": [l.response_time_ms for l in logs if l.source == "rag" and l.response_time_ms],
        "cag_times": [l.response_time_ms for l in logs if l.source == "cag" and l.response_time_ms],
        "all_times": [{"time": l.response_time_ms, "source": l.source, "cached": l.cached} for l in logs if l.response_time_ms],
    }

@router.get("/ab-test")
async def ab_test_data(db: Session = Depends(get_db)):
    logs = db.query(QueryLog).all()
    return {
        "rag_scores": [l.fuzzy_quality_score for l in logs if l.source == "rag" and l.fuzzy_quality_score],
        "cag_scores": [l.fuzzy_quality_score for l in logs if l.source == "cag" and l.fuzzy_quality_score],
    }
```

Register it in main.py:
```python
from routers import health, network, documents, chat, analytics
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
```

### STEP 8: Test frontend
```powershell
cd d:\Engineering\Projects\CampusMind\frontend
npm run dev
```
Open http://localhost:3000 and verify all pages render.

### STEP 9: Git commit
```powershell
cd d:\Engineering\Projects\CampusMind
git add -A
git commit -m "Phase 4: Frontend — chat UI, analytics dashboard, admin panel, network status"
```

### SUCCESS CRITERIA:
- [ ] Landing page renders with 3 feature cards
- [ ] Chat page can send queries and display responses
- [ ] Analytics page shows charts (even if empty initially)
- [ ] Admin page can upload documents and shows checksums
- [ ] Network status indicator shows connection type
- [ ] Dark theme with glassmorphism looks premium
```

---

# PHASE 5: DevOps — Docker, CI/CD, K8s, Terraform, Ansible, Monitoring
**Day 6 (Oct 4) | ~3-4 hours**

## What gets built
- Docker + Docker Compose setup
- GitHub Actions CI/CD
- Kubernetes manifests
- Terraform config
- Ansible playbook
- Prometheus + Grafana monitoring
- MLflow + Airflow configs

## Prompt for Flash — Phase 5

> I won't repeat all the DevOps configs here — they are **already fully specified** in the [IMPLEMENTATION_SPEC.md](file:///d:/Engineering/Projects/CampusMind/IMPLEMENTATION_SPEC.md) Sections 5.1 through 5.10. Tell Flash:

```
Read d:\Engineering\Projects\CampusMind\IMPLEMENTATION_SPEC.md sections 5.1 through 5.10.
Create ALL DevOps config files exactly as specified:
- devops/docker-compose.yml
- devops/docker-compose.monitoring.yml (Prometheus + Grafana)
- .github/workflows/ci.yml
- .github/workflows/cd.yml
- devops/kubernetes/ (namespace, deployment, service, ingress, configmap)
- devops/terraform/ (main.tf, variables.tf, outputs.tf, provider.tf)
- devops/ansible/ (inventory.ini, playbook.yml, roles)
- devops/prometheus/prometheus.yml
- devops/airflow/dags/document_ingestion.py
- devops/mlflow/mlflow_config.py
- backend/Dockerfile
- frontend/Dockerfile
- Jenkinsfile

Also add prometheus-fastapi-instrumentator to main.py:
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

Test: docker-compose -f devops/docker-compose.yml build
Git commit: "Phase 5: DevOps — Docker, CI/CD, K8s, Terraform, Ansible, monitoring"
```

---

# PHASE 6: Documentation, Jupyter Notebooks, Final Polish
**Day 7 (Oct 5) | ~3-4 hours**

## What gets built
- Jupyter notebooks for all Stats experiments
- API documentation
- README.md
- Final testing and bug fixes

## Prompt for Flash — Phase 6

```
## CampusMind — Phase 6: Final Documentation & Notebooks

### STEP 1: Create Jupyter notebooks in stats_notebooks/
Create 12 notebooks, each importing data from the CampusMind API.
Each notebook should:
- Have a clear title matching the Stats experiment
- Import necessary libraries (pandas, numpy, matplotlib, seaborn, scipy, sklearn)
- Fetch data from the API OR use synthetic data that mirrors the chatbot's output
- Include code + output + markdown explanations

Notebooks to create:
01_eda.ipynb — EDA on query logs (descriptive stats, histograms, correlation matrix)
02_preprocessing.ipynb — Data cleaning on document corpus
03_sampling.ipynb — Stratified/cluster sampling of test queries
04_clt_simulation.ipynb — CLT demonstration with response time samples
05_hypothesis_testing.ipynb — t-test comparing RAG vs CAG quality
06_bootstrap.ipynb — Bootstrap CI on accuracy metrics
07_mle.ipynb — MLE for response time distribution (Normal) and user satisfaction (Bernoulli)
08_linear_regression.ipynb — Predict response quality from features
09_regularization.ipynb — Ridge/Lasso/ElasticNet comparison
10_classification.ipynb — Intent classification with Logistic, KNN, Naive Bayes
11_trees_forest.ipynb — Decision tree + Random Forest for intent classification
12_pca_clustering.ipynb — PCA on query embeddings + K-means clustering

### STEP 2: Create README.md
Comprehensive README with:
- Project description
- Architecture diagram (Mermaid)
- Tech stack table
- Setup instructions (step by step)
- API documentation (list all endpoints)
- Screenshots section (placeholder paths)
- Subject-wise experiment mapping table
- Team members section

### STEP 3: Create docs/api_documentation.md
Full API reference with every endpoint, request/response format, examples.

### STEP 4: Create docs/network_architecture.md
Network topology of the deployed system — CN Exp 1 documentation.

### STEP 5: Create docs/wireless_analysis.md
WMC experiment documentation — EM spectrum, Wi-Fi analysis, throughput testing.

### STEP 6: Final testing
- Start backend and frontend
- Upload a syllabus PDF
- Ask 10 diverse questions
- Verify analytics dashboard shows data
- Check health endpoints
- Take screenshots of working app

### STEP 7: Git commit
git add -A
git commit -m "Phase 6: Jupyter notebooks, documentation, final polish"
```

---

## 📋 Quick Reference: What to Tell Flash Each Day

| Day | Date | Command to Flash |
|-----|------|------------------|
| 1 | Sep 29 | "Execute Phase 1 from PROJECT_PLAN.md" |
| 2 | Sep 30 | "Execute Phase 2 from PROJECT_PLAN.md" |
| 3-4 | Oct 1-2 | "Execute Phase 3 from PROJECT_PLAN.md" |
| 5 | Oct 3 | "Execute Phase 4 from PROJECT_PLAN.md" |
| 6 | Oct 4 | "Execute Phase 5 from PROJECT_PLAN.md" |
| 7 | Oct 5 | "Execute Phase 6 from PROJECT_PLAN.md" |

> [!TIP]
> When starting each phase, first tell Flash: "Read the Phase X section from `d:\Engineering\Projects\CampusMind\PROJECT_PLAN.md` and execute it step by step."

> [!WARNING]
> If Flash encounters errors, tell it: "Fix the error and continue. Do not redesign or change the architecture."
