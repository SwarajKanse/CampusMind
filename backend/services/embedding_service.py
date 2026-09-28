"""
Embedding service using sentence-transformers (all-MiniLM-L6-v2).
Runs on CPU — lightweight model (~90MB), fast inferences.
"""
from config import settings


class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                cls._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            except Exception:
                return None
        return cls._model

    @classmethod
    def encode(cls, texts: list[str]) -> list[list[float]]:
        model = cls.get_model()
        if model is None:
            import numpy as np
            return np.zeros((len(texts), 384)).tolist()
        embeddings = model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    @classmethod
    def encode_single(cls, text: str) -> list[float]:
        model = cls.get_model()
        if model is None:
            import numpy as np
            return np.zeros(384).tolist()
        return model.encode(text, show_progress_bar=False).tolist()
