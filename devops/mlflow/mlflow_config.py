"""
MLflow experiment tracking configuration.
ASD&D Exp 11: Machine Learning Experiment Tracking.
Logs model parameters, prompt latency, and fuzzy quality scores.
"""
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///./mlflow.db")
EXPERIMENT_NAME = "CampusMind_RAG_Evaluations"


def log_rag_run(query: str, latency_ms: float, confidence: float, fuzzy_score: float, model: str):
    """Logs evaluation parameters and metrics to MLflow if available."""
    try:
        import mlflow
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(EXPERIMENT_NAME)

        with mlflow.start_run(run_name="rag_evaluation"):
            mlflow.log_param("model", model)
            mlflow.log_param("query_char_length", len(query))
            mlflow.log_metric("latency_ms", latency_ms)
            mlflow.log_metric("cosine_confidence", confidence)
            mlflow.log_metric("fuzzy_quality_score", fuzzy_score)
    except Exception:
        # Graceful fallback when MLflow server is optional
        pass
