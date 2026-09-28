"""
Comprehensive Seed Script for CampusMind.
Populates:
1. Academic textbooks and syllabus study guides across 5 subjects into SQLite and ChromaDB.
2. Historical query logs (RAG vs CAG) with realistic latency, confidence, and fuzzy scores for Stats experiments.
"""
import os
import sys
import time
import random

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from database import SessionLocal, create_tables
from models import Document, QueryLog
from services.checksum_service import ChecksumService
from services.document_processor import DocumentProcessor
from services.rag_service import RAGService
from services.cag_service import CAGService


DOCUMENTS = {
    "computer_networks_study_guide.txt": """
# Computer Networks Comprehensive Study Guide

## 1. Network Architectures: OSI vs TCP/IP Model
The Open Systems Interconnection (OSI) reference model consists of seven layers:
1. Physical Layer: Transmits raw bitstreams over physical media (cables, radio frequencies).
2. Data Link Layer: Node-to-node frame delivery, MAC addressing, error detection via CRC-32.
3. Network Layer: Logical addressing (IPv4, IPv6) and path determination (Dijkstra, Bellman-Ford).
4. Transport Layer: End-to-end process communication, flow control (Sliding Window), TCP and UDP.
5. Session Layer: Manages dialog control and token management.
6. Presentation Layer: Syntax and semantics translation, data encryption (TLS/SSL), compression.
7. Application Layer: High-level protocols (HTTP, DNS, WebSocket, SMTP, FTP).

In contrast, the TCP/IP model condenses these into 4 layers: Link, Internet, Transport, and Application.

## 2. Error Detection and Correction (CN Experiment 5)
Data transmission over noisy channels requires robust verification:
- Cyclic Redundancy Check (CRC-32): Polynomial division using generator polynomial 0xEDB88320. Capable of detecting all single-bit, double-bit, and odd numbers of errors.
- Internet Checksum (RFC 1071): 16-bit one's complement sum of 16-bit words used in IPv4, TCP, and UDP headers. Computationally efficient for routers.
- Parity Checks: Single-bit parity checks identify odd numbers of flipped bits.

## 3. Transport Layer & Flow Control
- TCP (Transmission Control Protocol): Connection-oriented, reliable stream transport using a 3-way handshake (SYN -> SYN-ACK -> ACK). Implements Sliding Window flow control and AIMD (Additive Increase Multiplicative Decrease) congestion control.
- UDP (User Datagram Protocol): Connectionless, lightweight datagram service suitable for low-latency streaming and DNS queries.

## 4. WebSockets & Real-Time Socket Programming (CN Experiment 8)
RFC 6455 defines the WebSocket protocol providing full-duplex communication over a single TCP connection. Initiated via an HTTP Upgrade request (GET with Upgrade: websocket header), allowing sub-millisecond bidirectional communication without HTTP polling overhead.

## 5. Domain Name System (DNS) Resolution (CN Experiment 10)
DNS translates human-readable hostnames to IP addresses. Resolution hierarchy:
1. Local recursive resolver checks cache.
2. Root nameservers (.): Direct to Top-Level Domain (TLD) nameservers (.com, .edu).
3. TLD nameservers: Direct to Authoritative nameservers for the domain.
4. Authoritative nameservers: Return resource records (A, AAAA, CNAME, MX).
""",

    "artificial_intelligence_and_soft_computing.txt": """
# Artificial Intelligence & Soft Computing Curriculum Guide

## 1. Intelligent Agents & PEAS Formulation (AISC Experiment 1)
An intelligent agent perceives its environment through sensors and acts upon it through actuators.
The PEAS formulation specifies:
- Performance Measure: Query accuracy, response latency, student satisfaction, cache hit ratio.
- Environment: University academic syllabus, document repositories, student queries, network conditions.
- Actuators: Text generation via Groq LPU, WebSocket streaming tokens, analytics dashboard visualizations.
- Sensors: HTTP REST requests, WebSocket frames, uploaded PDF/text file streams.

## 2. Uninformed & Informed Search Algorithms (AISC Experiments 3 & 4)
- Breadth-First Search (BFS): Explores nodes level-by-level using a FIFO queue. Complete and optimal for unweighted graphs. Time complexity O(b^d), space complexity O(b^d).
- Depth-First Search (DFS): Explores deepest unvisited nodes first using a LIFO stack. Space-efficient O(b*m), but not guaranteed to find optimal paths.
- A* Search Algorithm: Evaluates nodes using the evaluation function f(n) = g(n) + h(n), where g(n) is the exact cost from start to node n, and h(n) is the admissible heuristic estimate from n to goal. A* is optimal if h(n) is admissible (never overestimates true cost).

## 3. Neural Networks & Perceptrons (AISC Experiments 7 & 8)
A single-layer Perceptron computes a weighted sum of inputs followed by an activation step: y = f(w^T x + b).
The Perceptron Learning Rule updates weights iteratively: w <- w + eta * (y_true - y_pred) * x.
Multi-class classification uses Softmax normalization across class logit outputs: P(y=k|x) = exp(z_k) / sum(exp(z_j)).

## 4. Fuzzy Logic & Fuzzy Inference Systems (AISC Experiments 13 & 14)
Fuzzy sets allow partial membership with degrees in [0, 1] defined by membership functions (Triangular, Trapezoidal, Gaussian).
- Mamdani FIS: Rules are expressed as IF x IS A AND y IS B THEN z IS C. Uses Min operator for implication, Max operator for aggregation, and Centroid calculation for crisp defuzzification: z* = sum(z * mu(z)) / sum(mu(z)).
- Takagi-Sugeno FIS: Consequent parts are crisp mathematical functions of inputs: IF x IS A THEN z = p*x + q. Defuzzification is computed via weighted average: z* = sum(w_i * z_i) / sum(w_i).

## 5. Neuro-Fuzzy Systems (ANFIS) (AISC Experiment 15)
Adaptive Neuro-Fuzzy Inference System combines the transparent interpretability of fuzzy rules with the empirical learning capability of artificial neural networks. Features a 5-layer feedforward structure tuned via hybrid learning (least squares estimation for linear consequent parameters, backpropagation for nonlinear premise parameters).

## 6. Retrieval-Augmented Generation (RAG) & CAG (AISC Experiments 11 & 12)
RAG retrieves top-k semantically relevant chunks from vector databases (ChromaDB) using dense cosine similarity embeddings (all-MiniLM-L6-v2, 384 dimensions).
Cache-Augmented Generation (CAG) stores pre-computed answers in Redis / memory caches, achieving 25x-50x speedups (from ~500ms down to ~10ms) while drastically conserving battery and bandwidth on mobile devices.
""",

    "applied_statistics_handbook.txt": """
# Applied Statistics & Data Analysis Handbook

## 1. Exploratory Data Analysis & Descriptive Statistics (Stats Experiment 1)
- Measures of Central Tendency: Mean (arithmetic average), Median (50th percentile robust to outliers), Mode (most frequent value).
- Measures of Dispersion: Variance s^2 = sum((x_i - mean)^2) / (n - 1), Standard Deviation s = sqrt(s^2), Interquartile Range IQR = Q3 - Q1.
- Shape Metrics: Skewness measures distribution asymmetry (Fisher-Pearson coefficient g1 = m3 / s^3). Kurtosis measures tail heaviness relative to a normal distribution (g2 = m4 / s^4 - 3.0).

## 2. Central Limit Theorem (CLT) & Sampling Distributions (Stats Experiment 4)
The Central Limit Theorem states that given a population with arbitrary probability distribution, mean mu, and finite variance sigma^2, the sampling distribution of the sample mean X_bar computed from independent random samples of size n approaches a normal distribution N(mu, sigma^2 / n) as n increases (typically n >= 30).
Standard Error of the Mean: SE = sigma / sqrt(n).

## 3. Hypothesis Testing: Welch's Two-Sample t-Test (Stats Experiment 5)
When comparing two independent groups (such as RAG latency vs CAG latency) where population variances cannot be assumed equal (sigma_1^2 != sigma_2^2):
Welch's t-statistic is computed as:
t = (X_bar_1 - X_bar_2) / sqrt(s_1^2 / n_1 + s_2^2 / n_2).
Degrees of freedom (df) are calculated using the Welch-Satterthwaite equation.
The null hypothesis H0: mu_RAG = mu_CAG is rejected when p-value < alpha (0.05), indicating a statistically significant difference.

## 4. Linear Regression & Pearson Correlation (Stats Experiments 8 & 9)
Simple linear regression models the dependent variable y (latency) as a function of explanatory variable x (query length): y = m*x + c.
- Slope: m = sum((x_i - x_bar)(y_i - y_bar)) / sum((x_i - x_bar)^2).
- Intercept: c = y_bar - m*x_bar.
- Pearson correlation coefficient r ranges from -1.0 to +1.0. Coefficient of determination R^2 measures the proportion of variance in y predictable from x.

## 5. Principal Component Analysis & K-Means Clustering (Stats Experiment 12)
PCA reduces 384-dimensional query embedding spaces to 2D projections by computing the eigenvectors of the data covariance matrix corresponding to the largest eigenvalues.
K-Means iteratively partitions observations into k distinct clusters by minimizing within-cluster sum of squares (WCSS) distance to cluster centroids.
""",

    "wireless_and_mobile_computing_guide.txt": """
# Wireless & Mobile Computing (WMC) Technical Guide

## 1. Wireless Topologies & Cellular Architecture
Modern wireless networks span cellular standards (4G LTE, 5G NR) and IEEE 802.11 Wi-Fi.
Key cellular components:
- Base Stations (eNodeB / gNodeB) providing radio coverage cells.
- Frequency reuse clusters to maximize spectrum efficiency while mitigating co-channel interference.
- Handoff mechanisms: Hard handoff (break-before-make) and Soft handoff (make-before-break).

## 2. Medium Access Control in Wireless Networks
Due to signal attenuation, collisions cannot be detected during transmission (no CD). Hence, Wi-Fi utilizes CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance):
- Interframe Spaces (DIFS, SIFS).
- Exponential backoff timers.
- Hidden Terminal Problem: Solved using Request to Send (RTS) and Clear to Send (CTS) handshake control frames.
- Exposed Terminal Problem: Over-conservative carrier sensing preventing concurrent non-interfering transmissions.

## 3. Mobile Device Energy Conservation & Radio Resource Control
Mobile wireless modems consume significant energy transitioning through radio states:
- Active / Connected State: High power consumption (~1200mW - 2000mW).
- Tail State: Modem stays active for 10-15 seconds after packet transfer waiting for additional data (~800mW - 1000mW).
- Idle / Sleep State: Low power consumption (~10mW - 20mW).

## 4. Cache-Augmented Generation (CAG) as an Energy Optimization Strategy
By caching frequent academic query responses locally and in low-latency edge caches:
- Radio awake time is reduced by up to 92%.
- Elimination of costly server-side LLM inference round-trips prevents cellular tail-energy state triggers.
- Conserves mobile device battery life while reducing end-to-end user latency from 500ms to under 15ms.
""",

    "devops_and_agile_engineering.txt": """
# Agile Software Development & DevOps (ASD&D) Reference

## 1. Agile Framework & Continuous Delivery
Agile methodologies prioritize iterative delivery, customer collaboration, and rapid response to change.
- Scrum: Sprints (1-2 weeks), daily standups, sprint reviews, and retrospectives.
- Kanban: Continuous flow, visual work-in-progress (WIP) limits.

## 2. Git Version Control & Interval Commits (ASD&D Exp 1)
Trunk-based development with frequent atomic commits. Each commit encapsulates a coherent unit of work with standardized messages:
- feat: new feature
- fix: bug fix
- test: adding test coverage
- docs: documentation updates
- refactor: code restructure without behavioral change

## 3. Continuous Integration & Automated Testing (ASD&D Exp 2 & 3)
CI pipelines (GitHub Actions, Jenkins) automatically trigger on push and pull requests:
- Linting and static analysis (flake8, eslint).
- Unit and integration tests (pytest with coverage reporting).
- Build verification and artifact generation.

## 4. Containerization & Docker Multi-Stage Builds (ASD&D Exp 4 & 5)
Multi-stage Docker builds isolate the build toolchain (Node.js compilers, C++ build tools) from the lightweight runtime image:
- Builder stage: Installs build dependencies and compiles standalone assets.
- Runner stage: Copies only the compiled standalone binary and static assets onto a minimal base image (alpine, slim), cutting image sizes by 80%.

## 5. Kubernetes Container Orchestration (ASD&D Exp 7 & 8)
Kubernetes manages containerized workloads across clusters:
- Deployments: Declarative updates, rolling upgrades, replica set management.
- Services: ClusterIP, NodePort, LoadBalancer network abstractions.
- ConfigMaps & Secrets: Decoupled environment configuration and credential management.
- Horizontal Pod Autoscaler (HPA): Automatic scaling based on CPU and memory utilization thresholds.

## 6. Infrastructure as Code & Configuration Management (ASD&D Exp 9 & 10)
- Terraform: Declarative provisioning of cloud infrastructure (VPCs, subnets, instances, databases) maintaining state integrity.
- Ansible: Agentless configuration management and automation via SSH and YAML playbooks.

## 7. Site Reliability Engineering & Observability (ASD&D Exp 11 & 12)
- Prometheus: Time-series metric collection via pull-based scraping of /metrics endpoints.
- Grafana: Interactive dashboards visualizing latency percentiles (p50, p95, p99), error rates, throughput, and system resource saturation (RED & USE methods).
"""
}


SAMPLE_QUERIES = [
    # Academic queries (RAG and CAG)
    ("Explain the difference between OSI and TCP/IP models.", "academic", 620.5, 0.94, False),
    ("What is the role of CRC-32 in data link frames?", "academic", 410.2, 0.91, False),
    ("How does the A* search algorithm guarantee optimal paths?", "academic", 580.4, 0.96, False),
    ("Explain Mamdani Fuzzy Inference System defuzzification.", "academic", 530.1, 0.89, False),
    ("What is Central Limit Theorem and why is it important?", "academic", 495.8, 0.95, False),
    ("How is Welch t-test used in hypothesis testing?", "academic", 512.3, 0.93, False),
    ("What causes the Hidden Terminal Problem in CSMA/CA?", "academic", 470.9, 0.92, False),
    ("Explain how CAG caching saves mobile device battery.", "academic", 440.6, 0.94, False),
    ("What are the advantages of Docker multi-stage builds?", "academic", 490.2, 0.90, False),
    ("How does the TCP 3-way handshake work?", "academic", 420.7, 0.97, False),
    ("What is the difference between BFS and DFS?", "academic", 460.3, 0.93, False),
    ("Explain the Takagi-Sugeno fuzzy model.", "academic", 510.8, 0.88, False),
    ("How does PCA reduce data dimensionality?", "academic", 550.2, 0.91, False),
    ("What is the RFC 1071 Internet Checksum?", "academic", 390.4, 0.95, False),
    ("Explain ANFIS neuro-fuzzy architecture.", "academic", 610.9, 0.89, False),

    # Fast CAG Cached Queries (response times ~10-25ms)
    ("Explain the difference between OSI and TCP/IP models.", "academic", 12.4, 0.94, True),
    ("How does the TCP 3-way handshake work?", "academic", 8.9, 0.97, True),
    ("What is Central Limit Theorem and why is it important?", "academic", 14.2, 0.95, True),
    ("How does the A* search algorithm guarantee optimal paths?", "academic", 11.5, 0.96, True),
    ("What causes the Hidden Terminal Problem in CSMA/CA?", "academic", 9.8, 0.92, True),
    ("Explain how CAG caching saves mobile device battery.", "academic", 15.1, 0.94, True),
    ("What is the role of CRC-32 in data link frames?", "academic", 10.3, 0.91, True),
    ("What are the advantages of Docker multi-stage builds?", "academic", 13.7, 0.90, True),
    ("What is the difference between BFS and DFS?", "academic", 9.2, 0.93, True),
    ("How does PCA reduce data dimensionality?", "academic", 16.4, 0.91, True),

    # General queries
    ("What are the college library timings?", "general", 310.2, 0.85, False),
    ("When is the semester examination starting?", "general", 340.5, 0.87, False),
    ("Where is the computer engineering department located?", "general", 290.1, 0.82, False),
    ("What is the procedure for laboratory submission?", "general", 325.4, 0.88, False),
    ("What are the college library timings?", "general", 8.4, 0.85, True),
    ("When is the semester examination starting?", "general", 11.2, 0.87, True),

    # Feedback queries
    ("This explanation was very clear and helpful.", "feedback", 180.2, 0.92, False),
    ("Thanks, this helped me understand the topic.", "feedback", 150.1, 0.95, False),
    ("Can you provide more practical examples?", "feedback", 195.4, 0.86, False),
    ("Great summary of the concepts.", "feedback", 140.8, 0.96, False),

    # Greeting queries
    ("Hello CampusMind!", "greeting", 95.3, 0.99, False),
    ("Good morning, I need help with my studies.", "greeting", 110.2, 0.98, False),
    ("Hey there!", "greeting", 85.1, 0.99, False),
    ("Hi, can you assist me with exam preparation?", "greeting", 120.4, 0.97, False),
]


def seed():
    print("🚀 Starting CampusMind Academic Knowledge Base & Data Seeder...")
    create_tables()
    db = SessionLocal()
    rag = RAGService()
    cag = CAGService()
    processor = DocumentProcessor()

    # 1. Ingest Academic Documents
    print("\n📚 Step 1: Processing and indexing academic curriculum guides...")
    for filename, text_content in DOCUMENTS.items():
        content_bytes = text_content.encode("utf-8")
        file_hash = ChecksumService.sha256(content_bytes)

        # Check if already exists in DB
        existing = db.query(Document).filter(Document.file_hash == file_hash).first()
        if existing:
            print(f"  ⏭️  '{filename}' already indexed. Skipping.")
            continue

        chunks = processor.process(content_bytes, filename)
        doc = Document(
            filename=filename,
            file_hash=file_hash,
            chunk_count=len(chunks),
            file_size=len(content_bytes),
            status="embedded"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        chunk_dicts = [
            {"text": c, "doc_id": doc.id, "chunk_idx": i, "source": filename}
            for i, c in enumerate(chunks)
        ]
        rag.add_documents(chunk_dicts)
        print(f"  ✅ Indexed '{filename}': {len(chunks)} chunks, SHA-256: {file_hash[:12]}...")

    # 2. Ingest Historical Query Logs for Statistics Analytics
    print("\n📊 Step 2: Populating historical query logs for Stats analytics...")
    existing_logs_count = db.query(QueryLog).count()
    if existing_logs_count >= len(SAMPLE_QUERIES):
        print(f"  ⏭️  Found {existing_logs_count} existing query logs. Skipping log seeding.")
    else:
        for q_text, intent, latency, conf, cached in SAMPLE_QUERIES:
            source = "cag" if cached else "rag"
            fuzzy_quality = round(min(1.0, max(0.5, conf * 0.9 + (0.1 if cached else 0.05))), 3)
            log = QueryLog(
                query_text=q_text,
                response_text=f"Sample response for academic query: {q_text}",
                response_time_ms=latency,
                source=source,
                intent=intent,
                confidence_score=conf,
                fuzzy_quality_score=fuzzy_quality,
                cached=cached,
                user_rating=5 if conf > 0.9 else 4,
            )
            db.add(log)

            # Also seed into CAG cache
            if cached:
                cag.cache_response(q_text, {
                    "answer": f"Cached high-speed response for: {q_text}",
                    "sources": ["academic_knowledge_base"],
                    "confidence": conf,
                    "fuzzy_scores": {"combined": fuzzy_quality},
                })
        db.commit()
        print(f"  ✅ Seeded {len(SAMPLE_QUERIES)} query logs across RAG & CAG.")

    total_docs = db.query(Document).count()
    total_logs = db.query(QueryLog).count()
    db.close()

    print("\n✨ Database and Vector Store Seeding Complete!")
    print(f"   - Total Documents: {total_docs}")
    print(f"   - Total Query Logs: {total_logs}")
    print("   - ChromaDB Collection: 'academic_docs' fully ready.")


if __name__ == "__main__":
    seed()
