"""
CAG (Cache-Augmented Generation) Service.
AISC Exp 12: Cache layer for instant retrieval of repeated queries.
Uses Redis when available, with an in-memory fallback for local development.
"""
import json
import hashlib
import time
from config import settings


class CAGService:
    def __init__(self):
        self._memory_cache = {}  # Fallback in-memory cache: {key: (data, expire_at)}
        self.available = False
        try:
            import redis
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.redis_client.ping()
            self.available = True
        except Exception:
            self.redis_client = None
            self.available = False

    def _hash_query(self, query: str) -> str:
        normalized = query.strip().lower()
        return f"cag:{hashlib.md5(normalized.encode()).hexdigest()}"

    def get_cached(self, query: str) -> dict | None:
        key = self._hash_query(query)
        if self.available and self.redis_client:
            try:
                cached = self.redis_client.get(key)
                if cached:
                    return json.loads(cached)
            except Exception:
                pass

        # In-memory fallback
        if key in self._memory_cache:
            data, expire_at = self._memory_cache[key]
            if time.time() < expire_at:
                return data
            else:
                del self._memory_cache[key]
        return None

    def cache_response(self, query: str, response: dict):
        key = self._hash_query(query)
        # Store in Redis if available
        if self.available and self.redis_client:
            try:
                self.redis_client.setex(key, settings.CACHE_TTL, json.dumps(response))
            except Exception:
                pass

        # Always also store in memory cache
        expire_at = time.time() + settings.CACHE_TTL
        self._memory_cache[key] = (response, expire_at)

    def get_cache_stats(self) -> dict:
        if self.available and self.redis_client:
            try:
                info = self.redis_client.info("stats")
                hits = info.get("keyspace_hits", 0)
                misses = info.get("keyspace_misses", 0)
                return {
                    "backend": "redis",
                    "available": True,
                    "hits": hits,
                    "misses": misses,
                    "hit_rate": round(hits / max(hits + misses, 1), 3),
                }
            except Exception:
                pass
        return {
            "backend": "memory",
            "available": True,
            "cached_entries": len(self._memory_cache),
        }
