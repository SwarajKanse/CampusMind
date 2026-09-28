"""Database models for CampusMind."""
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
    status = Column(String(50), default="processing")


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
