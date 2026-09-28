"""
Analytics router: provides statistical analysis and metrics for Stats experiments.
Covers:
- Stats Exp 1: EDA — descriptive statistics on query response times and confidence scores
- Stats Exp 4: Sampling distributions / Central Limit Theorem data
- Stats Exp 5: A/B hypothesis test (two-sample t-test comparing RAG vs CAG)
- Stats Exp 8, 9: Linear regression & correlation
- Stats Exp 10: Intent distribution breakdown
- Stats Exp 12: Dimensionality reduction (PCA) & clustering
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import QueryLog
from services.stats_service import StatsService

router = APIRouter()


@router.get("/query-stats")
async def get_query_stats(db: Session = Depends(get_db)):
    """Stats Exp 1: EDA — descriptive statistics on response times and confidence."""
    logs = db.query(QueryLog).all()
    if not logs:
        return {
            "total_queries": 0,
            "response_time": {},
            "confidence": {},
            "cache_rate": 0.0,
            "intent_distribution": {},
        }

    response_times = [l.response_time_ms for l in logs if l.response_time_ms is not None]
    confidences = [l.confidence_score for l in logs if l.confidence_score is not None]

    rt_stats = StatsService.descriptive_stats(response_times)
    conf_stats = StatsService.descriptive_stats(confidences)

    intents = {}
    for log in logs:
        intent = log.intent or "unclassified"
        intents[intent] = intents.get(intent, 0) + 1

    cache_count = sum(1 for l in logs if l.cached)

    return {
        "total_queries": len(logs),
        "response_time": rt_stats,
        "confidence": conf_stats,
        "cache_rate": round(cache_count / max(len(logs), 1), 3),
        "intent_distribution": intents,
    }


@router.get("/response-times")
async def get_response_times(db: Session = Depends(get_db)):
    """Stats Exp 1, 4: Raw response times for histogram and CLT distribution analysis."""
    logs = db.query(QueryLog).all()
    rag_times = [l.response_time_ms for l in logs if l.source == "rag" and l.response_time_ms]
    cag_times = [l.response_time_ms for l in logs if l.source == "cag" and l.response_time_ms]

    return {
        "rag_times": rag_times,
        "cag_times": cag_times,
        "total_recorded": len(rag_times) + len(cag_times),
    }


@router.get("/ab-test")
async def ab_test(db: Session = Depends(get_db)):
    """Stats Exp 5: A/B Hypothesis Testing comparing RAG vs CAG performance."""
    logs = db.query(QueryLog).all()
    rag_times = [l.response_time_ms for l in logs if l.source == "rag" and l.response_time_ms]
    cag_times = [l.response_time_ms for l in logs if l.source == "cag" and l.response_time_ms]

    if len(rag_times) >= 2 and len(cag_times) >= 2:
        return StatsService.t_test_rag_vs_cag(rag_times, cag_times)
    return {
        "message": "Collecting more A/B test data. Need at least 2 RAG and 2 CAG query logs.",
        "rag_count": len(rag_times),
        "cag_count": len(cag_times),
    }


@router.get("/regression")
async def regression_analysis(db: Session = Depends(get_db)):
    """Stats Exp 8, 9: Linear regression predicting response time from query length."""
    logs = db.query(QueryLog).all()
    points = [(len(l.query_text or ""), l.response_time_ms) for l in logs if l.response_time_ms]
    if len(points) >= 2:
        x = [float(p[0]) for p in points]
        y = [float(p[1]) for p in points]
        return StatsService.linear_regression(x, y)
    return {"message": "Need at least 2 query logs for regression analysis."}


@router.get("/embeddings-pca")
async def embeddings_pca(db: Session = Depends(get_db)):
    """Stats Exp 12: 2D PCA projection and clustering of query embeddings."""
    try:
        from sklearn.decomposition import PCA
        from sklearn.cluster import KMeans
        from services.embedding_service import EmbeddingService

        logs = db.query(QueryLog).limit(100).all()
        queries = [l.query_text for l in logs if l.query_text]

        if len(queries) < 3:
            return {"message": "Need at least 3 queries to project PCA space."}

        embeddings = EmbeddingService.encode(queries)
        pca = PCA(n_components=2)
        projected = pca.fit_transform(embeddings)

        n_clusters = min(3, len(queries))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(embeddings)

        return {
            "points": [
                {"x": round(float(p[0]), 3), "y": round(float(p[1]), 3), "cluster": int(c), "query": q}
                for p, c, q in zip(projected, clusters, queries)
            ],
            "explained_variance": [round(float(v), 4) for v in pca.explained_variance_ratio_],
        }
    except Exception as e:
        return {"error": str(e)}
