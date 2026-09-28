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
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

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
