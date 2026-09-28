"""
Chat router: REST + WebSocket for real-time streaming.
Covers:
- AISC Exp 7, 8: Perceptron intent classification
- AISC Exp 9, 10: Generative AI & Micro Language Models
- AISC Exp 11: RAG pipeline
- AISC Exp 12: Cache-Augmented Generation (CAG)
- AISC Exp 13, 14, 15: Fuzzy Logic & Neuro-Fuzzy response scoring
- CN Exp 8: WebSocket socket programming
"""
import time
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import QueryLog
from services.rag_service import RAGService
from services.cag_service import CAGService

router = APIRouter()

# Singletons
_rag_service = None
_cag_service = None
_intent_classifier = None
_fuzzy_scorer = None


def get_rag():
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service


def get_cag():
    global _cag_service
    if _cag_service is None:
        _cag_service = CAGService()
    return _cag_service


def get_intent():
    global _intent_classifier
    if _intent_classifier is None:
        from services.intent_classifier import IntentClassifier
        _intent_classifier = IntentClassifier()
    return _intent_classifier


def get_fuzzy():
    global _fuzzy_scorer
    if _fuzzy_scorer is None:
        from services.fuzzy_service import FuzzyQualityScorer
        _fuzzy_scorer = FuzzyQualityScorer()
    return _fuzzy_scorer


class ChatRequest(BaseModel):
    query: str
    use_cache: bool = True


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
    response_time_ms: float
    cached: bool
    intent: dict = {}
    fuzzy_scores: dict = {}


@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest, db: Session = Depends(get_db)):
    start = time.time()
    cag = get_cag()
    rag = get_rag()

    # Determine intent using Perceptron (AISC Exp 7, 8)
    intent_data = {"intent": "general", "confidence": 1.0}
    try:
        intent_svc = get_intent()
        intent_data = intent_svc.classify(request.query)
    except Exception:
        pass

    # 1. Try CAG Cache first (AISC Exp 12)
    if request.use_cache:
        cached = cag.get_cached(request.query)
        if cached:
            elapsed = (time.time() - start) * 1000
            fuzzy_scores = cached.get("fuzzy_scores", {})
            log = QueryLog(
                query_text=request.query,
                response_text=cached["answer"],
                response_time_ms=elapsed,
                source="cag",
                confidence_score=cached.get("confidence", 0.0),
                fuzzy_quality_score=fuzzy_scores.get("combined", 0.8),
                intent=intent_data.get("intent", "general"),
                cached=True,
            )
            db.add(log)
            db.commit()
            return ChatResponse(
                answer=cached["answer"],
                sources=cached.get("sources", []),
                confidence=cached.get("confidence", 0.0),
                response_time_ms=round(elapsed, 2),
                cached=True,
                intent=intent_data,
                fuzzy_scores=fuzzy_scores,
            )

    # 2. RAG Pipeline execution (AISC Exp 11)
    result = await rag.query(request.query)
    elapsed = (time.time() - start) * 1000

    # 3. Fuzzy quality scoring (AISC Exp 13, 14, 15)
    fuzzy_scores = {"mamdani": 0.8, "sugeno": 0.8, "neurofuzzy": 0.8, "combined": 0.8}
    try:
        fuzzy_svc = get_fuzzy()
        fuzzy_scores = fuzzy_svc.score(
            confidence=result["confidence"],
            response_length=len(result["answer"]),
            source_count=len(result["sources"]),
        )
    except Exception:
        pass

    cache_payload = {
        "answer": result["answer"],
        "sources": result["sources"],
        "confidence": result["confidence"],
        "fuzzy_scores": fuzzy_scores,
    }

    # 4. Cache the generated response in CAG layer
    cag.cache_response(request.query, cache_payload)

    # 5. Log query in database for statistical analysis
    log = QueryLog(
        query_text=request.query,
        response_text=result["answer"],
        response_time_ms=elapsed,
        source="rag",
        confidence_score=result["confidence"],
        fuzzy_quality_score=fuzzy_scores.get("combined"),
        intent=intent_data.get("intent"),
        cached=False,
    )
    db.add(log)
    db.commit()

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"],
        response_time_ms=round(elapsed, 2),
        cached=False,
        intent=intent_data,
        fuzzy_scores=fuzzy_scores,
    )


@router.get("/cache-stats")
async def cache_stats():
    """Returns real-time CAG cache statistics (hits, misses, hit rate)."""
    cag = get_cag()
    return cag.get_cache_stats()


@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time token streaming.
    CN Exp 8: Socket programming.
    """
    await websocket.accept()
    rag = get_rag()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            query = msg.get("query", "")
            if not query.strip():
                continue
            async for chunk in rag.stream_query(query):
                await websocket.send_json({"type": "chunk", "content": chunk})
            await websocket.send_json({"type": "done", "content": ""})
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"type": "error", "content": str(e)})
