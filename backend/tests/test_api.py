"""Unit & Integration Tests for CampusMind Backend."""
import pytest
from fastapi.testclient import TestClient
from main import app
from services.checksum_service import ChecksumService
from services.search_service import search_service
from services.fuzzy_service import FuzzyQualityScorer
from services.intent_classifier import intent_classifier
from services.stats_service import stats_service

client = TestClient(app)


def test_health_ping():
    """CN Exp 3: ICMP/PING equivalent endpoint."""
    response = client.get("/api/health/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "pong"


def test_checksum_algorithms():
    """CN Exp 5: Error detection algorithms (SHA-256, CRC-32, RFC 1071)."""
    data = b"Academic syllabus and curriculum data"
    sha = ChecksumService.sha256(data)
    crc = ChecksumService.crc32(data)
    chk = ChecksumService.internet_checksum(data)

    assert len(sha) == 64
    assert isinstance(crc, int)
    assert isinstance(chk, int)
    assert ChecksumService.verify_integrity(data, sha) is True


def test_search_algorithms():
    """AISC Exp 3 & 4: BFS, DFS, and A* on document graphs."""
    adjacency = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2, 4],
        4: [3]
    }
    # Test BFS
    bfs_result = search_service.bfs_search(0, adjacency, max_nodes=5)
    assert len(bfs_result) > 0
    assert bfs_result[0] == 0

    # Test DFS
    dfs_result = search_service.dfs_search(0, adjacency, max_nodes=5)
    assert len(dfs_result) > 0
    assert dfs_result[0] == 0

    # Test A*
    query_emb = [0.9, 0.1, 0.0]
    doc_embs = [[0.85, 0.15, 0.0], [0.1, 0.9, 0.0], [0.88, 0.12, 0.0]]
    docs = ["Doc A: Networks", "Doc B: Random", "Doc C: Subnets"]
    astar_result = search_service.a_star_search(query_emb, doc_embs, docs, top_k=2)
    assert len(astar_result) == 2
    assert "f_score" in astar_result[0]


def test_intent_classifier():
    """AISC Exp 3: Perceptron Intent Classification."""
    res = intent_classifier.classify("What is the syllabus for computer networks?")
    assert res["intent"] in ["academic", "general", "feedback", "greeting"]
    assert 0.0 <= res["confidence"] <= 1.0


def test_fuzzy_scoring():
    """AISC Exp 13-15: Mamdani, Sugeno & Neuro-Fuzzy Quality Scoring."""
    scorer = FuzzyQualityScorer()
    scores = scorer.score(confidence=0.88, response_length=150, source_count=3)
    assert "mamdani" in scores
    assert "sugeno" in scores
    assert "neurofuzzy" in scores
    assert "combined" in scores
    assert 0.0 <= scores["combined"] <= 1.0


def test_stats_analytics():
    """Stats Exp 1 & 5: Descriptive stats & Welch t-test."""
    eda = stats_service.descriptive_stats([120.0, 140.0, 135.0, 128.0, 150.0, 130.0])
    assert eda["count"] == 6
    assert eda["mean"] > 0

    ttest = stats_service.t_test_rag_vs_cag([120.0, 130.0, 140.0, 135.0, 125.0], [20.0, 25.0, 30.0, 22.0, 28.0])
    assert "t_statistic" in ttest
    assert ttest["is_statistically_significant"] is True
    assert ttest["speedup_factor"] > 1.0
