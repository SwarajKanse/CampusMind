# 🌐 Network Architecture & Topology — CampusMind (CN Exp 1)

## 📌 Topology Overview
CampusMind implements a distributed microservices network architecture featuring client edge connections, reverse proxy routing, internal service meshes, and cloud API gateways.

```mermaid
graph TD
    Client["Client Browser (Desktop/Mobile)"]
    WIFI["Wireless AP / 4G LTE Network"]
    
    subgraph "Campus Infrastructure"
        RP["Reverse Proxy / Nginx / Next.js Edge (Port 3000)"]
        API["FastAPI Backend Server (Port 8000)"]
        REDIS["Redis Cache Server (Port 6379)"]
        CHROMA["ChromaDB Vector Store (Local Filesystem)"]
        SQLITE["SQLite Database (campusmind.db)"]
        PROM["Prometheus Scraper (Port 9090)"]
        GRAF["Grafana Dashboard (Port 3001)"]
    end
    
    subgraph "Cloud LPUs & External Providers"
        GROQ["Groq Cloud Inference API (api.groq.com:443)"]
        DNS["Authoritative DNS Nameservers (Port 53)"]
    end

    Client -->|802.11 Wi-Fi / LTE| WIFI
    WIFI -->|HTTP/2 & WebSocket| RP
    RP -->|REST / JSON| API
    API -->|TCP Socket (AISC Exp 12)| REDIS
    API -->|Vector Similarity Queries| CHROMA
    API -->|SQL Queries (SQLAlchemy)| SQLITE
    API -->|HTTPS TLS 1.3 / LPU Inference| GROQ
    API -->|UDP Port 53 Resolution| DNS
    PROM -->|HTTP GET /metrics| API
    GRAF -->|PromQL Queries| PROM
```

---

## 📡 OSI Layer Mapping

| Layer | Protocol / Technology in CampusMind | Function |
|---|---|---|
| **Layer 7: Application** | HTTP/1.1, HTTP/2, WebSocket (WSS), REST, DNS | Chat querying, document upload, token streaming, DNS resolution. |
| **Layer 6: Presentation** | TLS 1.3, JSON serialization, UTF-8, CRC-32, SHA-256 | Data encryption, integrity checksum encoding, document parsing. |
| **Layer 5: Session** | WebSocket sessions, Redis connection pool | Stateful real-time chat streaming, persistent cache sessions. |
| **Layer 4: Transport** | TCP (FastAPI, Redis, HTTPS), UDP (DNS queries) | Reliable ordered packet transfer, low-latency datagram DNS lookups. |
| **Layer 3: Network** | IPv4, IPv6, ICMP | Host routing, interface addressing, ping connectivity checks. |
| **Layer 2: Data Link** | IEEE 802.11 (Wi-Fi), Ethernet IEEE 802.3, ARP | Frame encapsulation, MAC addressing (exposed in `/api/network/info`). |
| **Layer 1: Physical** | Radio frequency (2.4GHz / 5GHz / 6GHz), Twisted pair cat6 | Transmission medium telemetry. |
