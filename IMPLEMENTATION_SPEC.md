# 🏗️ CampusMind — Deep Implementation Specification

> **Purpose**: This document is designed to be handed off to Gemini 3.8 Flash for mechanical implementation. Every decision is pre-made. Every file is specified. The implementing model should NOT improvise — follow this document exactly.

---

## 1. Tech Stack (Fixed — Do Not Change)

| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| **Frontend** | Next.js (App Router) | 15.x | SSR + API routes in one project |
| **Styling** | Tailwind CSS | 4.x | Fast, utility-first (user requested framework) |
| **LLM Runtime** | Groq Cloud API | Latest | Ultra-fast LPU inference (no local GPU required) |
| **LLM Model** | `llama-3.3-70b-versatile` / `llama-3.1-8b-instant` | Latest | High quality, 500+ tok/s, generous free tier |
| **Embedding Model** | `all-MiniLM-L6-v2` via sentence-transformers | Latest | Lightweight, fast embeddings |
| **Vector DB** | ChromaDB | 0.5+ | Simple, file-based, Python-native |
| **Cache** | Redis | 7.x | Fast KV store for CAG layer |
| **Database** | SQLite | 3.x | Simple, no server needed (micro project) |
| **Monitoring** | Prometheus + Grafana | Latest | Metrics collection + dashboards |
| **CI/CD** | GitHub Actions | N/A | Free, integrated with GitHub |
| **Containerization** | Docker + Docker Compose | Latest | Multi-service orchestration |
| **ML Tracking** | MLflow | 2.x | Experiment tracking |
| **Workflow** | Apache Airflow | 2.x | DAG-based document ingestion |
| **IaC** | Terraform | 1.x | Infrastructure as Code |
| **Config Mgmt** | Ansible | 2.x | Server provisioning playbooks |
| **Orchestration** | Kubernetes | 1.x | Container orchestration manifests |

---

## 2. Project Folder Structure

```
CampusMind/
├── frontend/                          # Next.js app
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx             # Root layout with fonts, metadata
│   │   │   ├── page.tsx               # Landing page
│   │   │   ├── globals.css            # Tailwind imports + custom styles
│   │   │   ├── chat/
│   │   │   │   └── page.tsx           # Chat interface
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx           # Stats analytics dashboard
│   │   │   └── admin/
│   │   │       └── page.tsx           # Document upload & management
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── ChatWindow.tsx         # Main chat component
│   │   │   ├── ChatMessage.tsx        # Individual message bubble
│   │   │   ├── ChatInput.tsx          # Input box with send button
│   │   │   ├── DocumentUpload.tsx     # Drag-drop file upload
│   │   │   ├── AnalyticsCharts.tsx    # Charts for stats experiments
│   │   │   ├── NetworkStatus.tsx      # Network quality indicator (WMC)
│   │   │   └── Sidebar.tsx            # Navigation sidebar
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts        # WebSocket hook for real-time chat
│   │   │   └── useNetworkInfo.ts      # Network info detection (WMC)
│   │   └── lib/
│   │       ├── api.ts                 # API client functions
│   │       └── types.ts               # TypeScript interfaces
│   └── Dockerfile
│
├── backend/                           # FastAPI app
│   ├── requirements.txt
│   ├── main.py                        # FastAPI entry point
│   ├── config.py                      # App configuration
│   ├── database.py                    # SQLite setup
│   ├── models.py                      # SQLAlchemy models
│   ├── routers/
│   │   ├── chat.py                    # Chat endpoints + WebSocket
│   │   ├── documents.py               # Document upload/management
│   │   ├── analytics.py               # Analytics data endpoints
│   │   ├── health.py                  # Health check endpoints (CN)
│   │   └── network.py                 # Network diagnostic endpoints (WMC/CN)
│   ├── services/
│   │   ├── rag_service.py             # RAG pipeline (AISC Exp 11)
│   │   ├── cag_service.py             # Cache-Augmented Gen (AISC Exp 12)
│   │   ├── embedding_service.py       # Embedding generation
│   │   ├── llm_service.py             # LLM interaction via Groq Cloud API
│   │   ├── intent_classifier.py       # Query intent classification (AISC Exp 7,8)
│   │   ├── fuzzy_service.py           # Fuzzy logic scoring (AISC Exp 13,14)
│   │   ├── neurofuzzy_service.py      # Neuro-fuzzy system (AISC Exp 15)
│   │   ├── search_service.py          # BFS/DFS/A* document search (AISC Exp 3,4)
│   │   ├── stats_service.py           # Statistical analysis (Stats Exp 1-14)
│   │   ├── checksum_service.py        # Checksum validation (CN Exp 5)
│   │   └── document_processor.py      # PDF/text parsing and chunking
│   ├── ml/
│   │   ├── perceptron.py              # Perceptron implementation (AISC Exp 7)
│   │   ├── intent_model.py            # Intent classification model
│   │   ├── clustering.py              # Query clustering (Stats Exp 12)
│   │   ├── regression.py              # Response quality regression (Stats Exp 8,9)
│   │   ├── classification.py          # Multi-model classification (Stats Exp 10,11)
│   │   └── pca_viz.py                 # PCA visualization (Stats Exp 12)
│   ├── fuzzy/
│   │   ├── membership_functions.py    # Fuzzy membership definitions
│   │   ├── mamdani_fis.py             # Mamdani FIS implementation
│   │   ├── sugeno_fis.py              # Sugeno FIS implementation
│   │   └── neurofuzzy.py              # ANFIS-style hybrid system
│   ├── network/
│   │   ├── socket_server.py           # WebSocket server (CN Exp 8)
│   │   ├── health_checker.py          # Service health ping (CN Exp 2)
│   │   └── dns_resolver.py            # DNS lookup utility (CN Exp 10)
│   ├── Dockerfile
│   └── tests/
│       ├── test_rag.py
│       ├── test_cag.py
│       ├── test_fuzzy.py
│       └── test_stats.py
│
├── stats_notebooks/                   # Jupyter notebooks for Stats experiments
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_sampling.ipynb
│   ├── 04_clt_simulation.ipynb
│   ├── 05_hypothesis_testing.ipynb
│   ├── 06_bootstrap.ipynb
│   ├── 07_mle.ipynb
│   ├── 08_linear_regression.ipynb
│   ├── 09_regularization.ipynb
│   ├── 10_classification.ipynb
│   ├── 11_trees_forest.ipynb
│   └── 12_pca_clustering.ipynb
│
├── devops/                            # All DevOps configs (ASD&D)
│   ├── docker-compose.yml             # Multi-service compose
│   ├── docker-compose.monitoring.yml  # Prometheus + Grafana
│   ├── Jenkinsfile                    # Jenkins pipeline
│   ├── ansible/
│   │   ├── inventory.ini
│   │   ├── playbook.yml               # Server provisioning
│   │   └── roles/
│   │       └── app/
│   │           └── tasks/
│   │               └── main.yml
│   ├── kubernetes/
│   │   ├── namespace.yml
│   │   ├── deployment.yml
│   │   ├── service.yml
│   │   ├── ingress.yml
│   │   └── configmap.yml
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── provider.tf
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── dashboards/
│   │       └── campusmind.json
│   ├── airflow/
│   │   └── dags/
│   │       └── document_ingestion.py
│   └── mlflow/
│       └── mlflow_config.py
│
├── .github/
│   └── workflows/
│       ├── ci.yml                     # CI: lint + test + build
│       └── cd.yml                     # CD: deploy on merge to main
│
├── docs/
│   ├── peas_formulation.md            # PEAS model (AISC Exp 1)
│   ├── network_architecture.md        # Network topology docs (CN Exp 1)
│   ├── wireless_analysis.md           # Wireless concepts (WMC Exp 1,15)
│   ├── api_documentation.md           # API reference
│   └── user_guide.md                  # User guide
│
├── data/
│   ├── sample_documents/              # Sample academic PDFs for testing
│   └── query_logs/                    # Logged queries for stats analysis
│
├── .gitignore
├── README.md
└── Makefile                           # Common commands
```

---

## 3. Backend Implementation Details

### 3.1 `backend/main.py` — FastAPI Entry Point

```python
"""
CampusMind Backend API Server.
Provides RAG-based chatbot, analytics, and network endpoints.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
from database import create_tables
from routers import chat, documents, analytics, health, network

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create DB tables, load models
    create_tables()
    yield
    # Shutdown: cleanup

app = FastAPI(
    title="CampusMind API",
    description="AI-Powered Academic RAG Chatbot",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics (ASD&D Exp 11)
Instrumentator().instrument(app).expose(app)

# Register routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
```

### 3.2 `backend/config.py` — Configuration

```python
"""Application configuration. All settings in one place."""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "CampusMind"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./campusmind.db"

    # Groq Cloud API (ultra-fast LPU inference — no local GPU needed)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION: str = "academic_docs"

    # Redis (CAG)
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hour

    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3.3 `backend/database.py` — SQLite Database

```python
"""SQLite database setup using SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
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

### 3.4 `backend/models.py` — Database Models

```python
"""SQLAlchemy models for CampusMind."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_hash = Column(String(64), nullable=False)  # SHA256 checksum (CN Exp 5)
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
    source = Column(String(10), default="rag")  # "rag" or "cag"
    intent = Column(String(50))
    confidence_score = Column(Float)
    fuzzy_quality_score = Column(Float)
    user_rating = Column(Integer)  # 1-5 stars
    timestamp = Column(DateTime, server_default=func.now())
    cached = Column(Boolean, default=False)

class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"
    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(100))
    metric_value = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())
```

### 3.5 `backend/routers/chat.py` — Chat Endpoints + WebSocket

```python
"""
Chat router: REST endpoint + WebSocket for real-time streaming.
Covers: AISC Exp 9,10,11,12 | CN Exp 8 | Stats Exp logging
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import QueryLog
from services.rag_service import RAGService
from services.cag_service import CAGService
from services.intent_classifier import IntentClassifier
from services.fuzzy_service import FuzzyQualityScorer
import time
import json

router = APIRouter()
rag_service = RAGService()
cag_service = CAGService()
intent_classifier = IntentClassifier()
fuzzy_scorer = FuzzyQualityScorer()

class ChatRequest(BaseModel):
    query: str
    use_cache: bool = True

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
    fuzzy_quality: float
    response_time_ms: float
    cached: bool
    intent: str

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint. Tries CAG first, falls back to RAG.
    Logs everything for Stats experiments.
    """
    start = time.time()

    # Step 1: Classify intent (AISC Exp 7,8)
    intent = intent_classifier.classify(request.query)

    # Step 2: Try CAG cache first (AISC Exp 12)
    cached_response = None
    if request.use_cache:
        cached_response = await cag_service.get_cached(request.query)

    if cached_response:
        elapsed = (time.time() - start) * 1000
        quality = fuzzy_scorer.score(
            confidence=cached_response["confidence"],
            response_length=len(cached_response["answer"]),
            source_count=len(cached_response["sources"])
        )
        # Log for Stats
        log = QueryLog(
            query_text=request.query,
            response_text=cached_response["answer"],
            response_time_ms=elapsed,
            source="cag",
            intent=intent,
            confidence_score=cached_response["confidence"],
            fuzzy_quality_score=quality,
            cached=True
        )
        db.add(log)
        db.commit()
        return ChatResponse(
            answer=cached_response["answer"],
            sources=cached_response["sources"],
            confidence=cached_response["confidence"],
            fuzzy_quality=quality,
            response_time_ms=elapsed,
            cached=True,
            intent=intent
        )

    # Step 3: RAG pipeline (AISC Exp 11)
    rag_result = await rag_service.query(request.query)
    elapsed = (time.time() - start) * 1000

    # Step 4: Fuzzy quality scoring (AISC Exp 13,14)
    quality = fuzzy_scorer.score(
        confidence=rag_result["confidence"],
        response_length=len(rag_result["answer"]),
        source_count=len(rag_result["sources"])
    )

    # Step 5: Cache result (AISC Exp 12)
    await cag_service.cache_response(request.query, rag_result)

    # Step 6: Log for Stats
    log = QueryLog(
        query_text=request.query,
        response_text=rag_result["answer"],
        response_time_ms=elapsed,
        source="rag",
        intent=intent,
        confidence_score=rag_result["confidence"],
        fuzzy_quality_score=quality,
        cached=False
    )
    db.add(log)
    db.commit()

    return ChatResponse(
        answer=rag_result["answer"],
        sources=rag_result["sources"],
        confidence=rag_result["confidence"],
        fuzzy_quality=quality,
        response_time_ms=elapsed,
        cached=False,
        intent=intent
    )


@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat streaming.
    Covers CN Exp 8 (Socket Programming).
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            query = message.get("query", "")

            # Stream response chunks
            async for chunk in rag_service.stream_query(query):
                await websocket.send_json({
                    "type": "chunk",
                    "content": chunk
                })

            await websocket.send_json({
                "type": "done",
                "content": ""
            })
    except WebSocketDisconnect:
        pass
```

### 3.6 `backend/services/rag_service.py` — RAG Pipeline (AISC Exp 11)

```python
"""
RAG (Retrieval-Augmented Generation) Service.
AISC Exp 11: Design and Implementation of a RAG Framework for Contextual QA.
"""
import chromadb
from sentence_transformers import SentenceTransformer
from config import settings
from services.llm_service import LLMService
from services.search_service import SearchService

class RAGService:
    def __init__(self):
        self.embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
        self.llm = LLMService()
        self.search = SearchService()

    async def query(self, query_text: str, top_k: int = 5) -> dict:
        """
        Full RAG pipeline:
        1. Embed query
        2. Retrieve relevant chunks from ChromaDB
        3. Optionally refine with graph search (AISC Exp 3,4)
        4. Generate answer using LLM
        """
        # Step 1: Embed query
        query_embedding = self.embedder.encode(query_text).tolist()

        # Step 2: Retrieve from vector DB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        documents = results["documents"][0] if results["documents"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        distances = results["distances"][0] if results["distances"] else []

        # Step 3: Graph-based refinement using A* search (AISC Exp 4)
        refined_docs = self.search.a_star_refine(query_text, documents, distances)

        # Step 4: Build context for LLM
        context = "\n\n---\n\n".join(refined_docs[:5])

        # Step 5: Generate answer
        prompt = f"""You are CampusMind, an academic assistant chatbot.
Answer the question based ONLY on the provided context.
If the context doesn't contain the answer, say "I don't have enough information to answer this question."

Context:
{context}

Question: {query_text}

Answer:"""

        answer = await self.llm.generate(prompt)

        # Calculate confidence from distances
        if distances:
            avg_similarity = 1 - (sum(distances) / len(distances))
            confidence = min(max(avg_similarity, 0.0), 1.0)
        else:
            confidence = 0.0

        sources = [m.get("source", "unknown") for m in metadatas[:5]]

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }

    async def stream_query(self, query_text: str, top_k: int = 5):
        """Streaming version for WebSocket."""
        query_embedding = self.embedder.encode(query_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas"]
        )
        documents = results["documents"][0] if results["documents"] else []
        context = "\n\n---\n\n".join(documents[:5])

        prompt = f"""You are CampusMind, an academic assistant chatbot.
Answer based on the context provided.

Context:
{context}

Question: {query_text}

Answer:"""

        async for chunk in self.llm.stream_generate(prompt):
            yield chunk

    def add_documents(self, chunks: list[dict]):
        """Add document chunks to vector DB."""
        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.encode(texts).tolist()
        ids = [f"chunk_{c['doc_id']}_{c['chunk_idx']}" for c in chunks]
        metadatas = [{"source": c["source"], "chunk_idx": c["chunk_idx"]} for c in chunks]

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
```

### 3.7 `backend/services/cag_service.py` — CAG (AISC Exp 12)

```python
"""
CAG (Cache-Augmented Generation) Service.
AISC Exp 12: Cache layer that stores previous RAG responses
for instant retrieval of repeated/similar queries.
"""
import redis.asyncio as redis
import json
import hashlib
from config import settings

class CAGService:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

    def _hash_query(self, query: str) -> str:
        """Normalize and hash query for cache key."""
        normalized = query.strip().lower()
        return f"cag:{hashlib.md5(normalized.encode()).hexdigest()}"

    async def get_cached(self, query: str) -> dict | None:
        """Try to get cached response."""
        key = self._hash_query(query)
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    async def cache_response(self, query: str, response: dict):
        """Cache a RAG response."""
        key = self._hash_query(query)
        await self.redis.setex(
            key,
            settings.CACHE_TTL,
            json.dumps(response)
        )

    async def invalidate(self, query: str):
        """Remove a cached entry."""
        key = self._hash_query(query)
        await self.redis.delete(key)

    async def get_cache_stats(self) -> dict:
        """Get cache hit/miss statistics for analytics."""
        info = await self.redis.info("stats")
        return {
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
            "hit_rate": info.get("keyspace_hits", 0) /
                max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1)
        }
```

### 3.8 `backend/services/llm_service.py` — Groq Cloud LLM Interaction

```python
"""
LLM Service: Interact with Groq Cloud API for ultra-fast LPU inference.
AISC Exp 9: Generative AI exploration
AISC Exp 10: Small/Micro Language Models
"""
from groq import AsyncGroq
from config import settings

class LLMService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        """Generate complete response from LLM."""
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
        """Stream response token by token for WebSocket."""
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

### 3.9 `backend/services/search_service.py` — BFS/DFS/A* (AISC Exp 3,4)

```python
"""
Search Service: Graph-based document search.
AISC Exp 3: BFS/DFS uninformed search
AISC Exp 4: A* informed search
Documents form a graph where edges = similarity between chunks.
"""
import heapq
from collections import deque

class SearchService:
    def bfs_search(self, start_doc: str, all_docs: list[str], adjacency: dict) -> list[str]:
        """
        BFS traversal of document chunk graph.
        AISC Exp 3: Uninformed search.
        """
        visited = set()
        queue = deque([start_doc])
        result = []

        while queue:
            doc = queue.popleft()
            if doc not in visited:
                visited.add(doc)
                result.append(doc)
                for neighbor in adjacency.get(doc, []):
                    if neighbor not in visited:
                        queue.append(neighbor)

        return result

    def dfs_search(self, start_doc: str, all_docs: list[str], adjacency: dict) -> list[str]:
        """
        DFS traversal of document chunk graph.
        AISC Exp 3: Uninformed search.
        """
        visited = set()
        stack = [start_doc]
        result = []

        while stack:
            doc = stack.pop()
            if doc not in visited:
                visited.add(doc)
                result.append(doc)
                for neighbor in reversed(adjacency.get(doc, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return result

    def a_star_refine(self, query: str, documents: list[str], distances: list[float]) -> list[str]:
        """
        A* search: Use cosine distance as heuristic to rank documents.
        AISC Exp 4: Informed search.

        g(n) = position index (cost to reach)
        h(n) = cosine distance from query (heuristic)
        f(n) = g(n) + h(n)
        """
        if not documents:
            return []

        # Build priority queue with f(n) = g(n) + h(n)
        heap = []
        for i, (doc, dist) in enumerate(zip(documents, distances)):
            g = i * 0.1  # Small cost per position
            h = dist      # Cosine distance as heuristic
            f = g + h
            heapq.heappush(heap, (f, i, doc))

        # Extract in order of best f(n)
        result = []
        while heap:
            f_val, idx, doc = heapq.heappop(heap)
            result.append(doc)

        return result
```

### 3.10 `backend/services/intent_classifier.py` — Perceptron Classifier (AISC Exp 7,8)

```python
"""
Intent Classifier using Perceptron.
AISC Exp 7: Train perceptron for classification.
AISC Exp 8: Supervised/Unsupervised learning.
Classifies queries into: academic, general, feedback, greeting
"""
import numpy as np
from sentence_transformers import SentenceTransformer
from config import settings

class PerceptronClassifier:
    """Simple multi-class perceptron. AISC Exp 7."""

    def __init__(self, input_dim: int, num_classes: int):
        self.weights = np.random.randn(num_classes, input_dim) * 0.01
        self.bias = np.zeros(num_classes)

    def predict(self, x: np.ndarray) -> int:
        scores = self.weights @ x + self.bias
        return int(np.argmax(scores))

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
        self.embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.perceptron = PerceptronClassifier(
            input_dim=384,  # MiniLM embedding dim
            num_classes=len(self.INTENTS)
        )
        self._train_default()

    def _train_default(self):
        """Train on seed examples."""
        training_data = {
            "academic": [
                "What is binary search tree?",
                "Explain neural networks",
                "What are the types of sorting algorithms?",
                "Define polymorphism in OOP",
                "How does TCP work?",
            ],
            "general": [
                "What time is the exam?",
                "Where is the library?",
                "Who is the HOD?",
                "What are the holidays this month?",
            ],
            "feedback": [
                "This answer was helpful",
                "That was wrong",
                "Rate the response",
                "Good answer",
            ],
            "greeting": [
                "Hello",
                "Hi there",
                "Good morning",
                "Hey",
            ],
        }

        texts, labels = [], []
        for intent, examples in training_data.items():
            for ex in examples:
                texts.append(ex)
                labels.append(self.INTENTS.index(intent))

        X = self.embedder.encode(texts)
        y = np.array(labels)
        self.perceptron.train(X, y, epochs=200, lr=0.01)

    def classify(self, query: str) -> str:
        embedding = self.embedder.encode(query)
        idx = self.perceptron.predict(embedding)
        return self.INTENTS[idx]
```

### 3.11 `backend/fuzzy/mamdani_fis.py` — Fuzzy Inference (AISC Exp 13,14)

```python
"""
Mamdani Fuzzy Inference System for response quality scoring.
AISC Exp 13: Fuzzy Logic Controller
AISC Exp 14: Mamdani/Sugeno FIS

Inputs: confidence (0-1), response_length (0-2000), source_count (0-10)
Output: quality_score (0-1)
"""
import numpy as np

class MembershipFunction:
    """Triangular and trapezoidal membership functions."""

    @staticmethod
    def triangular(x: float, a: float, b: float, c: float) -> float:
        """Triangular MF: f(x; a, b, c)"""
        if x <= a or x >= c:
            return 0.0
        elif x <= b:
            return (x - a) / (b - a) if b != a else 1.0
        else:
            return (c - x) / (c - b) if c != b else 1.0

    @staticmethod
    def trapezoidal(x: float, a: float, b: float, c: float, d: float) -> float:
        """Trapezoidal MF: f(x; a, b, c, d)"""
        if x <= a or x >= d:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 1.0
        elif b < x <= c:
            return 1.0
        else:
            return (d - x) / (d - c) if d != c else 1.0


class MamdaniFIS:
    """
    Mamdani FIS with rules:
    Rule 1: IF confidence IS high AND sources IS many THEN quality IS excellent
    Rule 2: IF confidence IS medium AND sources IS some THEN quality IS good
    Rule 3: IF confidence IS low OR sources IS few THEN quality IS poor
    Rule 4: IF response_length IS short THEN quality IS poor
    Rule 5: IF confidence IS high AND response_length IS long THEN quality IS excellent
    """
    MF = MembershipFunction

    def fuzzify_confidence(self, conf: float) -> dict:
        return {
            "low": self.MF.trapezoidal(conf, 0, 0, 0.3, 0.5),
            "medium": self.MF.triangular(conf, 0.3, 0.5, 0.7),
            "high": self.MF.trapezoidal(conf, 0.5, 0.7, 1.0, 1.0),
        }

    def fuzzify_length(self, length: float) -> dict:
        return {
            "short": self.MF.trapezoidal(length, 0, 0, 50, 150),
            "medium": self.MF.triangular(length, 100, 500, 1000),
            "long": self.MF.trapezoidal(length, 800, 1200, 2000, 2000),
        }

    def fuzzify_sources(self, count: float) -> dict:
        return {
            "few": self.MF.trapezoidal(count, 0, 0, 1, 2),
            "some": self.MF.triangular(count, 1, 3, 5),
            "many": self.MF.trapezoidal(count, 3, 5, 10, 10),
        }

    def evaluate_rules(self, conf: dict, length: dict, sources: dict) -> dict:
        """Apply fuzzy rules and return output fuzzy sets."""
        return {
            "excellent": max(
                min(conf["high"], sources["many"]),          # Rule 1
                min(conf["high"], length["long"]),            # Rule 5
            ),
            "good": min(conf["medium"], sources["some"]),     # Rule 2
            "poor": max(
                max(conf["low"], sources["few"]),             # Rule 3
                length["short"],                              # Rule 4
            ),
        }

    def defuzzify(self, output: dict) -> float:
        """Centroid defuzzification."""
        # Output universe: 0 to 1
        x = np.linspace(0, 1, 100)
        aggregated = np.zeros_like(x)

        # Output MFs
        for i, xi in enumerate(x):
            poor = min(output["poor"], self.MF.trapezoidal(xi, 0, 0, 0.2, 0.4))
            good = min(output["good"], self.MF.triangular(xi, 0.3, 0.5, 0.7))
            excellent = min(output["excellent"], self.MF.trapezoidal(xi, 0.6, 0.8, 1.0, 1.0))
            aggregated[i] = max(poor, good, excellent)

        # Centroid
        if np.sum(aggregated) == 0:
            return 0.5
        return float(np.sum(x * aggregated) / np.sum(aggregated))

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        conf = self.fuzzify_confidence(confidence)
        length = self.fuzzify_length(float(response_length))
        sources = self.fuzzify_sources(float(source_count))
        output = self.evaluate_rules(conf, length, sources)
        return self.defuzzify(output)
```

### 3.12 `backend/fuzzy/neurofuzzy.py` — ANFIS Hybrid (AISC Exp 15)

```python
"""
Hybrid Neuro-Fuzzy System (ANFIS-style).
AISC Exp 15: Developing a Hybrid Neuro-Fuzzy System.

Combines neural network learning with fuzzy inference.
The neural network learns optimal membership function parameters.
"""
import numpy as np

class ANFISLayer:
    """Simplified ANFIS architecture."""

    def __init__(self, n_inputs: int = 3, n_rules: int = 4):
        self.n_inputs = n_inputs
        self.n_rules = n_rules

        # Layer 1: Membership function parameters (learnable)
        # Each rule has Gaussian MF params (mean, sigma) for each input
        self.means = np.random.randn(n_rules, n_inputs) * 0.5 + 0.5
        self.sigmas = np.abs(np.random.randn(n_rules, n_inputs) * 0.2) + 0.1

        # Layer 4: Consequent parameters (learnable)
        # Each rule: y_i = p_i * x1 + q_i * x2 + r_i * x3 + s_i
        self.consequent = np.random.randn(n_rules, n_inputs + 1) * 0.1

        self.lr = 0.01

    def gaussian_mf(self, x: float, mean: float, sigma: float) -> float:
        return np.exp(-0.5 * ((x - mean) / max(sigma, 1e-6)) ** 2)

    def forward(self, x: np.ndarray) -> float:
        """Forward pass through ANFIS layers."""
        # Layer 1: Fuzzification (Gaussian MFs)
        mu = np.zeros((self.n_rules, self.n_inputs))
        for i in range(self.n_rules):
            for j in range(self.n_inputs):
                mu[i, j] = self.gaussian_mf(x[j], self.means[i, j], self.sigmas[i, j])

        # Layer 2: Rule firing strengths (product)
        w = np.prod(mu, axis=1)

        # Layer 3: Normalized firing strengths
        w_sum = np.sum(w) + 1e-10
        w_norm = w / w_sum

        # Layer 4: Consequent output per rule
        x_aug = np.append(x, 1.0)  # Add bias term
        rule_outputs = self.consequent @ x_aug

        # Layer 5: Weighted sum
        output = np.sum(w_norm * rule_outputs)
        return float(np.clip(output, 0, 1))

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100):
        """Train using gradient descent."""
        for epoch in range(epochs):
            total_loss = 0
            for xi, yi in zip(X, y):
                pred = self.forward(xi)
                error = yi - pred
                total_loss += error ** 2

                # Update consequent parameters (simplified gradient)
                x_aug = np.append(xi, 1.0)
                for r in range(self.n_rules):
                    self.consequent[r] += self.lr * error * x_aug * 0.25

            if epoch % 20 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss / len(X):.4f}")


class NeuroFuzzyQualityScorer:
    """Uses ANFIS for adaptive quality scoring."""

    def __init__(self):
        self.anfis = ANFISLayer(n_inputs=3, n_rules=4)
        self._pretrain()

    def _pretrain(self):
        """Pre-train on synthetic quality data."""
        # Generate training data: [confidence, norm_length, norm_sources] -> quality
        X = np.random.rand(200, 3)
        # Quality heuristic: high confidence + moderate length + many sources = good
        y = 0.5 * X[:, 0] + 0.2 * np.clip(X[:, 1], 0.2, 0.8) + 0.3 * X[:, 2]
        y = np.clip(y + np.random.randn(200) * 0.05, 0, 1)
        self.anfis.train(X, y, epochs=100)

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        """Score response quality using neuro-fuzzy system."""
        norm_length = min(response_length / 2000.0, 1.0)
        norm_sources = min(source_count / 10.0, 1.0)
        x = np.array([confidence, norm_length, norm_sources])
        return self.anfis.forward(x)
```

### 3.13 `backend/services/fuzzy_service.py` — Fuzzy Quality Scorer Wrapper

```python
"""Wrapper that combines Mamdani FIS with Neuro-Fuzzy for quality scoring."""
from fuzzy.mamdani_fis import MamdaniFIS
from fuzzy.neurofuzzy import NeuroFuzzyQualityScorer

class FuzzyQualityScorer:
    def __init__(self):
        self.mamdani = MamdaniFIS()
        self.neurofuzzy = NeuroFuzzyQualityScorer()

    def score(self, confidence: float, response_length: int, source_count: int) -> float:
        """Combined score: average of Mamdani and Neuro-Fuzzy."""
        mamdani_score = self.mamdani.score(confidence, response_length, source_count)
        nf_score = self.neurofuzzy.score(confidence, response_length, source_count)
        return (mamdani_score + nf_score) / 2.0
```

### 3.14 `backend/services/checksum_service.py` — Checksum (CN Exp 5)

```python
"""
Checksum validation for document uploads.
CN Exp 5: CRC/Hamming/Checksum implementation.
"""
import hashlib
import struct

class ChecksumService:
    @staticmethod
    def sha256(data: bytes) -> str:
        """SHA-256 hash for file integrity verification."""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def crc32(data: bytes) -> int:
        """CRC-32 checksum. CN Exp 5."""
        import binascii
        return binascii.crc32(data) & 0xFFFFFFFF

    @staticmethod
    def internet_checksum(data: bytes) -> int:
        """
        Internet checksum (RFC 1071) as used in TCP/UDP.
        CN Exp 5: Checksum implementation.
        """
        if len(data) % 2 == 1:
            data += b'\x00'

        total = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            total += word

        # Add carry
        while total >> 16:
            total = (total & 0xFFFF) + (total >> 16)

        return ~total & 0xFFFF

    @staticmethod
    def verify_integrity(data: bytes, expected_hash: str) -> bool:
        """Verify file hasn't been corrupted during upload."""
        actual = hashlib.sha256(data).hexdigest()
        return actual == expected_hash
```

### 3.15 `backend/routers/documents.py` — Document Management

```python
"""
Document upload and management router.
Covers: CN Exp 5 (checksum), CN Exp 9 (file transfer)
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Document
from services.checksum_service import ChecksumService
from services.document_processor import DocumentProcessor
from services.rag_service import RAGService

router = APIRouter()
checksum_svc = ChecksumService()
doc_processor = DocumentProcessor()
rag_service = RAGService()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload academic document (PDF/TXT), compute checksum, chunk, embed."""
    content = await file.read()

    # CN Exp 5: Compute checksums
    file_hash = checksum_svc.sha256(content)
    crc = checksum_svc.crc32(content)
    internet_cksum = checksum_svc.internet_checksum(content)

    # Check for duplicates
    existing = db.query(Document).filter(Document.file_hash == file_hash).first()
    if existing:
        raise HTTPException(status_code=409, detail="Document already exists")

    # Process and chunk document
    chunks = doc_processor.process(content, file.filename)

    # Store in DB
    doc = Document(
        filename=file.filename,
        file_hash=file_hash,
        chunk_count=len(chunks),
        file_size=len(content),
        status="processed"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Add to vector DB
    chunk_dicts = [
        {"text": c, "doc_id": doc.id, "chunk_idx": i, "source": file.filename}
        for i, c in enumerate(chunks)
    ]
    rag_service.add_documents(chunk_dicts)

    return {
        "id": doc.id,
        "filename": file.filename,
        "chunks": len(chunks),
        "sha256": file_hash,
        "crc32": crc,
        "internet_checksum": internet_cksum,
        "status": "processed"
    }

@router.get("/list")
async def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return [{"id": d.id, "filename": d.filename, "chunks": d.chunk_count,
             "size": d.file_size, "status": d.status, "uploaded": str(d.uploaded_at)}
            for d in docs]

@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": f"Document {doc_id} deleted"}
```

### 3.16 `backend/services/document_processor.py` — Document Chunking

```python
"""Document parsing and chunking service."""
import io
from config import settings

class DocumentProcessor:
    def process(self, content: bytes, filename: str) -> list[str]:
        """Parse document and split into chunks."""
        if filename.endswith(".pdf"):
            text = self._extract_pdf(content)
        elif filename.endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")
        elif filename.endswith(".md"):
            text = content.decode("utf-8", errors="ignore")
        else:
            text = content.decode("utf-8", errors="ignore")

        return self._chunk_text(text)

    def _extract_pdf(self, content: bytes) -> str:
        """Extract text from PDF."""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except ImportError:
            # Fallback: try pdfplumber
            import pdfplumber
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)

    def _chunk_text(self, text: str) -> list[str]:
        """Split text into overlapping chunks."""
        chunk_size = settings.CHUNK_SIZE
        overlap = settings.CHUNK_OVERLAP
        chunks = []

        words = text.split()
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
            i += chunk_size - overlap

        return chunks
```

### 3.17 `backend/routers/analytics.py` — Stats Analytics Endpoints

```python
"""
Analytics router: provides data for Stats experiments.
Covers Stats Exp 1-12.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import QueryLog
import numpy as np

router = APIRouter()

@router.get("/query-stats")
async def get_query_stats(db: Session = Depends(get_db)):
    """
    Stats Exp 1: EDA — descriptive stats on query data.
    Returns mean, median, std, min, max of response times.
    """
    logs = db.query(QueryLog).all()
    if not logs:
        return {"message": "No data yet"}

    response_times = [l.response_time_ms for l in logs if l.response_time_ms]
    confidences = [l.confidence_score for l in logs if l.confidence_score]

    return {
        "total_queries": len(logs),
        "response_time": {
            "mean": float(np.mean(response_times)) if response_times else 0,
            "median": float(np.median(response_times)) if response_times else 0,
            "std": float(np.std(response_times)) if response_times else 0,
            "min": float(np.min(response_times)) if response_times else 0,
            "max": float(np.max(response_times)) if response_times else 0,
        },
        "confidence": {
            "mean": float(np.mean(confidences)) if confidences else 0,
            "std": float(np.std(confidences)) if confidences else 0,
        },
        "cache_rate": sum(1 for l in logs if l.cached) / max(len(logs), 1),
        "intent_distribution": _count_intents(logs),
    }

def _count_intents(logs):
    counts = {}
    for log in logs:
        intent = log.intent or "unknown"
        counts[intent] = counts.get(intent, 0) + 1
    return counts

@router.get("/response-times")
async def get_response_times(db: Session = Depends(get_db)):
    """Raw response times for histogram/CLT visualization. Stats Exp 1,4."""
    logs = db.query(QueryLog).all()
    return {
        "rag_times": [l.response_time_ms for l in logs if l.source == "rag" and l.response_time_ms],
        "cag_times": [l.response_time_ms for l in logs if l.source == "cag" and l.response_time_ms],
    }

@router.get("/ab-test")
async def ab_test_data(db: Session = Depends(get_db)):
    """
    Stats Exp 5: A/B test data — RAG vs CAG quality comparison.
    Returns data suitable for t-test.
    """
    logs = db.query(QueryLog).all()
    rag_scores = [l.fuzzy_quality_score for l in logs if l.source == "rag" and l.fuzzy_quality_score]
    cag_scores = [l.fuzzy_quality_score for l in logs if l.source == "cag" and l.fuzzy_quality_score]

    return {
        "rag_quality_scores": rag_scores,
        "cag_quality_scores": cag_scores,
        "rag_count": len(rag_scores),
        "cag_count": len(cag_scores),
    }

@router.get("/embeddings-pca")
async def embeddings_pca(db: Session = Depends(get_db)):
    """
    Stats Exp 12: PCA + clustering data.
    Returns 2D PCA projection of query embeddings.
    """
    from sentence_transformers import SentenceTransformer
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans

    logs = db.query(QueryLog).limit(200).all()
    queries = [l.query_text for l in logs if l.query_text]

    if len(queries) < 5:
        return {"message": "Need more queries for PCA"}

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(queries)

    pca = PCA(n_components=2)
    projected = pca.fit_transform(embeddings)

    kmeans = KMeans(n_clusters=min(4, len(queries)), random_state=42)
    clusters = kmeans.fit_predict(embeddings)

    return {
        "points": [{"x": float(p[0]), "y": float(p[1]), "cluster": int(c), "query": q}
                   for p, c, q in zip(projected, clusters, queries)],
        "explained_variance": pca.explained_variance_ratio_.tolist(),
    }
```

### 3.18 `backend/routers/health.py` — Health Check (CN Exp 2)

```python
"""
Health check endpoints.
CN Exp 1,2: Study networking, simulate LAN + PING.
"""
from fastapi import APIRouter
import httpx
import time
import socket

router = APIRouter()

@router.get("/ping")
async def ping():
    """Basic health check — like PING in networking."""
    return {"status": "ok", "message": "pong", "timestamp": time.time()}

@router.get("/services")
async def check_services():
    """
    Check health of all microservices.
    CN Exp 2: Simulate connectivity testing using PING.
    """
    # Check Groq API
    try:
        headers = {}
        if settings.GROQ_API_KEY:
            headers["Authorization"] = f"Bearer {settings.GROQ_API_KEY}"
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("https://api.groq.com/openai/v1/models", headers=headers)
            results["groq_api"] = {
                "status": "reachable",
                "latency_ms": round(resp.elapsed.total_seconds() * 1000, 2),
                "authenticated": resp.status_code == 200,
            }
    except Exception as e:
        results["groq_api"] = {"status": "unreachable", "error": str(e)}

    # Check Redis
    try:
        import redis
        r = redis.Redis(host="localhost", port=6379, socket_timeout=2)
        start = time.time()
        r.ping()
        results["redis"] = {"status": "up", "latency_ms": (time.time() - start) * 1000}
    except Exception as e:
        results["redis"] = {"status": "down", "error": str(e)}

    # Self check
    results["api"] = {"status": "up", "hostname": socket.gethostname()}

    return results

@router.get("/dns-lookup/{hostname}")
async def dns_lookup(hostname: str):
    """
    CN Exp 10: DNS resolution.
    Resolve hostname to IP address.
    """
    try:
        ip = socket.gethostbyname(hostname)
        full_info = socket.getaddrinfo(hostname, None)
        return {
            "hostname": hostname,
            "ip": ip,
            "addresses": list(set(addr[4][0] for addr in full_info)),
            "family": "IPv4" if full_info[0][0] == socket.AF_INET else "IPv6"
        }
    except socket.gaierror as e:
        return {"hostname": hostname, "error": str(e)}
```

### 3.19 `backend/routers/network.py` — Network Diagnostics (WMC + CN)

```python
"""
Network diagnostics endpoints.
WMC Exp 4,5,7,13: Wi-Fi scanning, signal strength, throughput
CN Exp 6: Protocol analysis info
"""
from fastapi import APIRouter, Request
import time
import psutil

router = APIRouter()

@router.get("/info")
async def network_info(request: Request):
    """
    WMC Exp 4,13: Network information.
    Returns client IP, network interfaces, etc.
    """
    interfaces = {}
    for name, addrs in psutil.net_if_addrs().items():
        interfaces[name] = [
            {"family": str(addr.family), "address": addr.address}
            for addr in addrs
        ]

    return {
        "client_ip": request.client.host if request.client else "unknown",
        "server_interfaces": interfaces,
        "timestamp": time.time(),
    }

@router.get("/throughput-test")
async def throughput_test():
    """
    WMC Exp 7: Throughput measurement.
    Returns a payload to measure download speed.
    """
    # Generate 1MB of data
    start = time.time()
    payload = "x" * (1024 * 1024)
    elapsed = time.time() - start

    return {
        "payload_size_bytes": len(payload),
        "generation_time_ms": elapsed * 1000,
        "payload": payload[:100] + "... (truncated)",
        "full_size_kb": len(payload) / 1024,
    }

@router.get("/latency")
async def measure_latency():
    """
    WMC Exp 7: Latency measurement.
    Client can use the timestamp to calculate RTT.
    """
    return {
        "server_timestamp": time.time(),
        "message": "Use (receive_time - server_timestamp) for one-way latency"
    }
```

---

## 4. Frontend Implementation Details

### 4.1 Initialize Next.js Project

```bash
# Run from CampusMind/ root
npx -y create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --no-import-alias
```

### 4.2 Key Frontend Components

The frontend should have these pages:

1. **`/` (Landing Page)**: Hero section with project name, description, buttons to Chat and Analytics
2. **`/chat` (Chat Page)**: Full-screen chat interface with WebSocket streaming
3. **`/analytics` (Analytics Dashboard)**: Charts showing Stats experiment data
4. **`/admin` (Admin Page)**: Document upload, system health, cache stats

### 4.3 `src/hooks/useWebSocket.ts` — WebSocket Hook (CN Exp 8)

```typescript
import { useState, useEffect, useCallback, useRef } from 'react';

interface WSMessage {
  type: 'chunk' | 'done';
  content: string;
}

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [streamingText, setStreamingText] = useState('');
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);
    ws.onmessage = (event) => {
      const msg: WSMessage = JSON.parse(event.data);
      if (msg.type === 'chunk') {
        setStreamingText(prev => prev + msg.content);
      } else if (msg.type === 'done') {
        // Signal completion
      }
    };

    return () => ws.close();
  }, [url]);

  const sendQuery = useCallback((query: string) => {
    setStreamingText('');
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ query }));
    }
  }, []);

  return { isConnected, streamingText, sendQuery };
}
```

### 4.4 `src/hooks/useNetworkInfo.ts` — Network Detection (WMC Exp 4,13)

```typescript
/**
 * WMC Exp 4, 13: Detect network type, signal quality.
 * Uses Navigator.connection API.
 */
export function useNetworkInfo() {
  const getNetworkInfo = () => {
    const conn = (navigator as any).connection ||
                 (navigator as any).mozConnection ||
                 (navigator as any).webkitConnection;
    if (conn) {
      return {
        type: conn.effectiveType || 'unknown', // '4g', '3g', '2g', 'slow-2g'
        downlink: conn.downlink || 0,           // Mbps
        rtt: conn.rtt || 0,                     // ms
        saveData: conn.saveData || false,
      };
    }
    return { type: 'unknown', downlink: 0, rtt: 0, saveData: false };
  };

  return getNetworkInfo();
}
```

### 4.5 Frontend Design Requirements

> [!IMPORTANT]
> The UI must be premium and modern. Use these design tokens:

- **Color palette**: Dark theme with purple/blue accents
  - Background: `#0a0a1a` (deep navy)
  - Surface: `#12122a` (slightly lighter)
  - Primary: `#7c3aed` (violet-600)
  - Accent: `#06b6d4` (cyan-500)
  - Text: `#e2e8f0` (slate-200)
  - Muted: `#64748b` (slate-500)
- **Font**: Inter from Google Fonts
- **Border radius**: 12px for cards, 8px for inputs
- **Animations**: Smooth 200ms transitions, fade-in for messages
- **Chat bubbles**: User = right-aligned violet, Bot = left-aligned dark surface
- **Glassmorphism**: On cards with `backdrop-filter: blur(12px)` and `bg-opacity-60`

---

## 5. DevOps Configuration Files

### 5.1 `devops/docker-compose.yml` (ASD&D Exp 5,6)

```yaml
version: '3.8'
services:
  frontend:
    build: ../frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

  backend:
    build: ../backend
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GROQ_MODEL=${GROQ_MODEL:-llama-3.3-70b-versatile}
    volumes:
      - chroma_data:/app/chroma_db
      - sqlite_data:/app/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  chroma_data:
  sqlite_data:
  redis_data:
```

### 5.2 `.github/workflows/ci.yml` (ASD&D Exp 3)

```yaml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install backend deps
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest flake8

      - name: Lint
        run: cd backend && flake8 . --max-line-length=120

      - name: Test
        run: cd backend && pytest tests/ -v

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install frontend deps
        run: cd frontend && npm ci

      - name: Lint frontend
        run: cd frontend && npm run lint

      - name: Build frontend
        run: cd frontend && npm run build

  docker-build:
    runs-on: ubuntu-latest
    needs: lint-and-test
    steps:
      - uses: actions/checkout@v4
      - name: Build backend image
        run: docker build -t campusmind-backend ./backend
      - name: Build frontend image
        run: docker build -t campusmind-frontend ./frontend
```

### 5.3 `.github/workflows/cd.yml` (ASD&D Exp 8)

```yaml
name: CD Pipeline
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and push Docker images
        run: |
          docker build -t campusmind-backend ./backend
          docker build -t campusmind-frontend ./frontend

      - name: Deploy with Docker Compose
        run: |
          cd devops
          docker-compose up -d --build
```

### 5.4 `devops/kubernetes/deployment.yml` (ASD&D Exp 7)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: campusmind-backend
  namespace: campusmind
spec:
  replicas: 2
  selector:
    matchLabels:
      app: campusmind-backend
  template:
    metadata:
      labels:
        app: campusmind-backend
    spec:
      containers:
        - name: backend
          image: campusmind-backend:latest
          ports:
            - containerPort: 8000
          env:
            - name: REDIS_URL
              value: "redis://redis-service:6379/0"
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: campusmind-frontend
  namespace: campusmind
spec:
  replicas: 2
  selector:
    matchLabels:
      app: campusmind-frontend
  template:
    metadata:
      labels:
        app: campusmind-frontend
    spec:
      containers:
        - name: frontend
          image: campusmind-frontend:latest
          ports:
            - containerPort: 3000
```

### 5.5 `devops/kubernetes/service.yml` (ASD&D Exp 7)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: campusmind-backend-svc
  namespace: campusmind
spec:
  selector:
    app: campusmind-backend
  ports:
    - port: 8000
      targetPort: 8000
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: campusmind-frontend-svc
  namespace: campusmind
spec:
  selector:
    app: campusmind-frontend
  ports:
    - port: 80
      targetPort: 3000
  type: LoadBalancer
```

### 5.6 `devops/terraform/main.tf` (ASD&D Exp 9)

```hcl
# Terraform config for cloud infrastructure provisioning

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# EC2 Instance for CampusMind
resource "aws_instance" "campusmind_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.campusmind_sg.id]

  tags = {
    Name = "CampusMind-Server"
    Project = "CampusMind"
  }

  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io docker-compose
    systemctl start docker
    systemctl enable docker
  EOF
}

resource "aws_security_group" "campusmind_sg" {
  name = "campusmind-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 5.7 `devops/ansible/playbook.yml` (ASD&D Exp 4)

```yaml
---
- name: Provision CampusMind Server
  hosts: campusmind_servers
  become: yes

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes

    - name: Install Docker
      apt:
        name:
          - docker.io
          - docker-compose
        state: present

    - name: Start Docker service
      service:
        name: docker
        state: started
        enabled: yes

    - name: Clone CampusMind repo
      git:
        repo: "https://github.com/yourusername/CampusMind.git"
        dest: /opt/campusmind
        version: main

    - name: Run Docker Compose
      shell: |
        cd /opt/campusmind/devops
        docker-compose up -d --build
```

### 5.8 `devops/prometheus/prometheus.yml` (ASD&D Exp 11)

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'campusmind-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

### 5.9 `devops/airflow/dags/document_ingestion.py` (ASD&D Exp 13)

```python
"""
Airflow DAG for automated document ingestion pipeline.
ASD&D Exp 13: Designing, scheduling, and monitoring workflows.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import os

default_args = {
    'owner': 'campusmind',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'document_ingestion',
    default_args=default_args,
    description='Ingest new academic documents into CampusMind',
    schedule_interval=timedelta(hours=6),
    catchup=False,
)

def scan_for_new_docs(**kwargs):
    """Scan document directory for new files."""
    doc_dir = "/data/incoming_documents"
    new_files = []
    if os.path.exists(doc_dir):
        for f in os.listdir(doc_dir):
            if f.endswith(('.pdf', '.txt', '.md')):
                new_files.append(os.path.join(doc_dir, f))
    kwargs['ti'].xcom_push(key='new_files', value=new_files)
    return new_files

def upload_documents(**kwargs):
    """Upload each new document to CampusMind API."""
    new_files = kwargs['ti'].xcom_pull(key='new_files', task_ids='scan_docs')
    api_url = "http://backend:8000/api/documents/upload"

    for filepath in new_files:
        with open(filepath, 'rb') as f:
            response = requests.post(api_url, files={'file': f})
            if response.status_code == 200:
                print(f"Uploaded: {filepath}")
                os.rename(filepath, filepath + ".processed")
            else:
                print(f"Failed: {filepath} — {response.text}")

def log_results(**kwargs):
    """Log ingestion results."""
    new_files = kwargs['ti'].xcom_pull(key='new_files', task_ids='scan_docs')
    print(f"Processed {len(new_files)} documents")

scan_task = PythonOperator(task_id='scan_docs', python_callable=scan_for_new_docs, dag=dag)
upload_task = PythonOperator(task_id='upload_docs', python_callable=upload_documents, dag=dag)
log_task = PythonOperator(task_id='log_results', python_callable=log_results, dag=dag)

scan_task >> upload_task >> log_task
```

### 5.10 `devops/mlflow/mlflow_config.py` (ASD&D Exp 12)

```python
"""
MLflow configuration for tracking embedding model experiments.
ASD&D Exp 12: ML lifecycle with model development & deployment.
"""
import mlflow
from config import settings

def setup_mlflow():
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment("campusmind-embeddings")

def log_embedding_experiment(model_name: str, metrics: dict, params: dict):
    """Log an embedding model experiment."""
    with mlflow.start_run(run_name=f"embedding-{model_name}"):
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.set_tag("model_type", "embedding")
        mlflow.set_tag("project", "CampusMind")

def log_rag_experiment(retrieval_metrics: dict, generation_metrics: dict):
    """Log RAG pipeline experiment."""
    with mlflow.start_run(run_name="rag-pipeline"):
        mlflow.log_metrics({
            "retrieval_precision": retrieval_metrics.get("precision", 0),
            "retrieval_recall": retrieval_metrics.get("recall", 0),
            "generation_bleu": generation_metrics.get("bleu", 0),
            "avg_response_time": generation_metrics.get("avg_time", 0),
        })
```

---

## 6. `backend/requirements.txt`

```
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic-settings==2.7.1
sqlalchemy==2.0.36
sentence-transformers==3.3.1
chromadb==0.5.23
redis[hiredis]==5.2.1
httpx==0.28.1
python-multipart==0.0.18
PyMuPDF==1.25.1
numpy==2.2.1
scipy==1.15.0
scikit-learn==1.6.1
prometheus-fastapi-instrumentator==7.0.2
mlflow==2.19.0
psutil==6.1.1
websockets==14.1
pytest==8.3.4
flake8==7.1.1
```

---

## 7. PEAS Formulation Document (AISC Exp 1)

Save as `docs/peas_formulation.md`:

| Component | Description |
|-----------|-------------|
| **Performance** | Response accuracy, relevance, response time, user satisfaction rating, cache hit rate |
| **Environment** | Academic setting (university), course materials (PDFs, notes), student queries, Wi-Fi network |
| **Actuators** | Text responses, source citations, confidence scores, quality ratings |
| **Sensors** | Text queries (NL input), document uploads, user feedback (ratings), network status |

---

## 8. Build & Run Instructions

### Step-by-step (for implementing model):

```bash
# 1. Create project structure
mkdir -p CampusMind/{frontend,backend,devops,docs,data,stats_notebooks}
cd CampusMind

# 2. Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Configure Groq API key in .env
# Get your free key at https://console.groq.com/keys
# Add GROQ_API_KEY=your_key_here to .env (see .env.example)

# 4. Start Redis
docker run -d --name redis -p 6379:6379 redis:7-alpine

# 5. Run backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 6. Set up frontend
cd frontend
npx -y create-next-app@latest . --typescript --tailwind --eslint --app --src-dir
npm install
npm run dev

# 7. Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001
```

---

## 9. What the Implementing Model Should Do (Execution Order)

> [!IMPORTANT]
> Follow this exact order. Do NOT skip steps or improvise.

1. **Create the folder structure** exactly as specified in Section 2
2. **Backend first**: Create all Python files in `backend/` — start with `config.py`, `database.py`, `models.py`, then services, then routers, then `main.py`
3. **Create `requirements.txt`** as specified
4. **Frontend**: Initialize Next.js with the specified command, then create all components and pages
5. **DevOps configs**: Create all YAML/HCL files in `devops/`
6. **GitHub Actions**: Create `.github/workflows/` files
7. **Documentation**: Create files in `docs/`
8. **Test**: Run backend with `uvicorn` and frontend with `npm run dev`

> [!CAUTION]
> Do NOT change the tech stack. Do NOT substitute libraries. Do NOT skip the fuzzy/neuro-fuzzy implementations. These cover critical AISC experiments.
