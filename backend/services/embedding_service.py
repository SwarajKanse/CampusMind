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
            from sentence_transformers import SentenceTransformer
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
