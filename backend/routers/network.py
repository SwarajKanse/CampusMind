"""
Network diagnostics endpoints.
Covers WMC Experiments 4,5,7,13 and CN Experiment 6.
"""
from fastapi import APIRouter, Request
import time
import psutil

router = APIRouter()


@router.get("/info")
async def network_info(request: Request):
    """
    WMC Exp 4,13: Network information.
    Returns client IP, server network interfaces, etc.
    """
    interfaces = {}
    for name, addrs in psutil.net_if_addrs().items():
        interfaces[name] = [
            {"family": str(a.family), "address": a.address}
            for a in addrs
        ]

    return {
        "client_ip": request.client.host if request.client else "unknown",
        "server_interfaces": interfaces,
        "timestamp": time.time(),
    }


@router.get("/throughput-test")
async def throughput_test():
    """
    WMC Exp 7: Throughput and latency measurement.
    Returns metadata for client-side throughput calculation.
    """
    start = time.time()
    payload_size = 1024 * 1024  # 1MB conceptual
    elapsed = time.time() - start

    return {
        "payload_size_bytes": payload_size,
        "server_generation_ms": round(elapsed * 1000, 3),
        "server_timestamp": time.time(),
    }


@router.get("/latency")
async def measure_latency():
    """
    WMC Exp 7: Latency measurement.
    Client uses (receive_time - server_timestamp) for one-way latency.
    """
    return {"server_timestamp": time.time()}
