"""
Health check endpoints.
Covers CN Experiment 1 (networking commands study) and CN Experiment 2 (PING connectivity).
"""
from fastapi import APIRouter
import time
import socket
import httpx

from config import settings

router = APIRouter()


@router.get("/ping")
async def ping():
    """Basic health check — analogous to PING in networking. CN Exp 2."""
    return {"status": "ok", "message": "pong", "timestamp": time.time()}


@router.get("/services")
async def check_services():
    """
    Check health of all dependent services.
    CN Exp 2: Simulate connectivity testing using PING-like health checks.
    """
    results = {}

    # Check Groq API reachability
    try:
        headers = {}
        if settings.GROQ_API_KEY:
            headers["Authorization"] = f"Bearer {settings.GROQ_API_KEY}"
        async with httpx.AsyncClient(timeout=5.0) as client:
            start = time.time()
            resp = await client.get("https://api.groq.com/openai/v1/models", headers=headers)
            latency = (time.time() - start) * 1000
            # 200 = authenticated ok, 401 = reached Groq but key not set yet
            if resp.status_code in [200, 401]:
                results["groq_api"] = {
                    "status": "reachable",
                    "latency_ms": round(latency, 2),
                    "authenticated": resp.status_code == 200,
                }
            else:
                results["groq_api"] = {
                    "status": f"http_{resp.status_code}",
                    "latency_ms": round(latency, 2),
                }
    except Exception as e:
        results["groq_api"] = {"status": "unreachable", "error": str(e)}

    # Check Redis
    try:
        import redis as r
        rc = r.Redis(host="localhost", port=6379, socket_timeout=2)
        start = time.time()
        rc.ping()
        latency = (time.time() - start) * 1000
        results["redis"] = {"status": "up", "latency_ms": round(latency, 2)}
    except Exception as e:
        results["redis"] = {"status": "down", "error": str(e)}

    # Self check
    results["api"] = {"status": "up", "hostname": socket.gethostname()}

    return results


@router.get("/dns-lookup/{hostname}")
async def dns_lookup(hostname: str):
    """
    CN Experiment 10: DNS resolution.
    Resolve a hostname to its IP address(es).
    """
    try:
        ip = socket.gethostbyname(hostname)
        full_info = socket.getaddrinfo(hostname, None)
        return {
            "hostname": hostname,
            "ip": ip,
            "addresses": list(set(addr[4][0] for addr in full_info)),
        }
    except socket.gaierror as e:
        return {"hostname": hostname, "error": str(e)}
