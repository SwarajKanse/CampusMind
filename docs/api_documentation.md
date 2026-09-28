# 📖 CampusMind — API Specification & Documentation

CampusMind exposes high-performance asynchronous REST endpoints and WebSocket channels engineered with FastAPI and integrated with Groq Cloud LPUs.

---

## 1. Health & Networking Diagnostics (CN Experiments 1, 2, 10)

### `GET /api/health/ping`
- **Description**: Analogous to ICMP PING. Verifies basic server reachability and timestamp.
- **Subject Experiment**: CN Exp 2.
- **Response**:
```json
{
  "status": "ok",
  "message": "pong",
  "timestamp": 1790618315.48
}
```

### `GET /api/health/services`
- **Description**: Pings connected dependent microservices including Groq API reachability, network latency, and Redis connection.
- **Response**:
```json
{
  "groq_api": {
    "status": "reachable",
    "latency_ms": 353.12,
    "authenticated": true
  },
  "redis": {
    "status": "up",
    "latency_ms": 1.2
  },
  "api": {
    "status": "up",
    "hostname": "Inspiron-14"
  }
}
```

### `GET /api/health/dns-lookup/{hostname}`
- **Description**: Resolves domain names to IP addresses (IPv4 & IPv6).
- **Subject Experiment**: CN Exp 10 (DNS Resolution).
- **Example**: `GET /api/health/dns-lookup/google.com`
- **Response**:
```json
{
  "hostname": "google.com",
  "ip": "142.250.146.113",
  "addresses": ["142.250.146.113", "142.250.146.102", "2404:6800:4009:802::200e"]
}
```

---

## 2. Wireless & Interface Telemetry (WMC Experiments 4, 5, 7, 13)

### `GET /api/network/info`
- **Description**: Monitors local network interfaces, MAC addresses, IPv4/IPv6 socket families, and client request IP.
- **Subject Experiment**: WMC Exp 4, 5, 7.
- **Response**:
```json
{
  "client_ip": "127.0.0.1",
  "server_interfaces": {
    "WiFi": [
      { "family": "2", "address": "10.194.55.229" },
      { "family": "-1", "address": "04-CF-4B-D2-60-95" }
    ]
  },
  "timestamp": 1790618316.0
}
```

---

## 3. Document Ingestion & Checksum Verification (CN Exp 5 & 9)

### `POST /api/documents/upload`
- **Description**: Uploads PDF or TXT files, performs integrity verification via 3 checksum algorithms, extracts text, chunks, and creates vector embeddings in ChromaDB.
- **Content-Type**: `multipart/form-data`
- **Form Fields**: `file` (Binary)
- **Response**:
```json
{
  "id": 1,
  "filename": "Sem_V_Syllabus.pdf",
  "chunks": 29,
  "sha256": "548ab38f8db5ae133fdd2542060d35493e0528f6974c92402bdcf20c8edf0873",
  "crc32": "0x92cbfe85",
  "internet_checksum": "0x5ba",
  "status": "embedded"
}
```

### `GET /api/documents/list`
- **Description**: Lists all active documents in the knowledge base.

### `DELETE /api/documents/{id}`
- **Description**: Deletes a document by ID.

---

## 4. Intelligent Chat & Cache Retrieval (AISC Exp 7, 9, 10, 11, 12, 13, 14, 15)

### `POST /api/chat/query`
- **Description**: Full pipeline query execution. Checks CAG cache first; on miss, retrieves top-k chunks from ChromaDB, determines query intent with a Multi-Class Perceptron, generates context-grounded response via Groq Cloud LPUs, computes Fuzzy quality scores (Mamdani, Sugeno, ANFIS), and caches results.
- **Request Body**:
```json
{
  "query": "What is RAG pipeline?",
  "use_cache": true
}
```
- **Response**:
```json
{
  "answer": "Retrieval-Augmented Generation (RAG) is an AI architecture that enhances LLM generation by retrieving relevant document chunks from a vector database...",
  "sources": ["Sem_V_Syllabus.pdf"],
  "confidence": 0.88,
  "response_time_ms": 348.2,
  "cached": false,
  "intent": {
    "intent": "academic",
    "confidence": 0.94
  },
  "fuzzy_scores": {
    "mamdani": 0.82,
    "sugeno": 0.85,
    "neurofuzzy": 0.84,
    "combined": 0.837
  }
}
```

### `GET /api/chat/cache-stats`
- **Description**: Returns CAG Cache hit count, miss count, and hit rate (AISC Exp 12).

### `WebSocket /api/chat/ws`
- **Description**: Real-time token-by-token streaming socket (CN Exp 8 Socket Programming).

---

## 5. Statistical Analytics (Stats Experiments 1, 4, 5, 8, 9, 10, 12)

- `GET /api/analytics/query-stats` (EDA descriptive metrics)
- `GET /api/analytics/response-times` (Histograms / Central Limit Theorem)
- `GET /api/analytics/ab-test` (Welch's two-sample t-test)
- `GET /api/analytics/regression` (Linear regression & Pearson correlation)
- `GET /api/analytics/embeddings-pca` (2D PCA projection of queries)
