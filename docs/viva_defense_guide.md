# 🎓 CampusMind — Unified Academic Viva Voce & Defense Guide

> **Project**: CampusMind (AI-Powered Academic RAG Chatbot)  
> **Repository**: [https://github.com/SwarajKanse/CampusMind.git](https://github.com/SwarajKanse/CampusMind.git)  
> **Author**: Swaraj Kanse (2026)  
> **Target Audience**: External Examiners & Faculty across AISC, CN, Stats, WMC, and ASD&D.

---

## 📑 Quick Subject Navigation

1. [Artificial Intelligence & Soft Computing (AISC)](#1-artificial-intelligence--soft-computing-aisc)
2. [Computer Networks (CN)](#2-computer-networks-cn)
3. [Applied Statistics (Stats)](#3-applied-statistics-stats)
4. [Wireless & Mobile Computing (WMC)](#4-wireless--mobile-computing-wmc)
5. [Agile Software Development & DevOps (ASD&D)](#5-agile-software-development--devops-asdd)
6. [Live Demonstration Script for Examiners](#6-live-demonstration-script-for-examiners)

---

## 1. Artificial Intelligence & Soft Computing (AISC)

### Q1: What is the PEAS formulation of your academic chatbot? (Exp 1)
- **Answer**:
  - **Performance Measure**: Semantic accuracy of answers, retrieval confidence score, response latency (<500ms for RAG, <20ms for CAG), user satisfaction rating (1-5 stars), and cache hit ratio.
  - **Environment**: University engineering curriculum, syllabus guidelines, authoritative textbooks (Russell & Norvig, Tanenbaum, Charu Aggarwal), student queries via web/WebSocket, and multi-cloud LLM APIs.
  - **Actuators**: Groq LPU text generation engine, WebSocket token streaming, Redis CAG cache writer, and dynamic Recharts analytics renderer.
  - **Sensors**: HTTP REST query endpoints (`/api/chat/query`), WebSocket frames (`/api/chat/ws`), document upload multi-part stream (`/api/documents/upload`), and system network adapters.
- **Code Reference**: [`docs/peas_formulation.md`](file:///d:/Engineering/Projects/CampusMind/docs/peas_formulation.md) and [`backend/routers/chat.py`](file:///d:/Engineering/Projects/CampusMind/backend/routers/chat.py#L75-L165).

### Q2: How did you implement uninformed and informed search? (Exp 3 & 4)
- **Answer**:
  - We construct a semantic graph where vertices are document chunks and edges represent cosine similarity between dense embeddings ($threshold \ge 0.70$).
  - **BFS (Uninformed)**: Explores document chunks level-by-level using a FIFO `collections.deque` queue to discover broad topical neighbors.
  - **DFS (Uninformed)**: Traverses deep citation trees using a LIFO stack to follow specific sub-arguments.
  - **A\* Search (Informed)**: Evaluates nodes using the evaluation function:
    $$f(n) = g(n) + h(n)$$
    where $g(n)$ is the accumulated exploration path cost, and $h(n) = 1.0 - \text{cosine\_similarity}(q, \text{doc}_n)$ is the heuristic distance to the query vector. Since cosine distance never overestimates true relevance, $h(n)$ is **admissible and consistent**, guaranteeing optimal retrieval order.
- **Code Reference**: [`backend/services/search_service.py`](file:///d:/Engineering/Projects/CampusMind/backend/services/search_service.py#L12-L93).

### Q3: How is Perceptron used in intent classification? (Exp 7 & 8)
- **Answer**:
  - We built a custom `MultiClassPerceptron` neural network trained on 384-dimensional query sentence embeddings.
  - It maps each input vector $\mathbf{x}$ to logits across 4 academic intent classes (Academic, General, Feedback, Greeting):
    $$z_k = \mathbf{w}_k^T \mathbf{x} + b_k, \quad P(y=k|\mathbf{x}) = \frac{e^{z_k}}{\sum_{j} e^{z_j}}$$
  - Weights are updated via the Perceptron learning rule with learning rate $\eta = 0.01$ over 200 epochs.
- **Code Reference**: [`backend/ml/perceptron.py`](file:///d:/Engineering/Projects/CampusMind/backend/ml/perceptron.py) and [`backend/services/intent_classifier.py`](file:///d:/Engineering/Projects/CampusMind/backend/services/intent_classifier.py).

### Q4: How do Mamdani and Takagi-Sugeno Fuzzy Inference Systems evaluate answer quality? (Exp 13, 14 & 15)
- **Answer**:
  - **Mamdani FIS**: Evaluates retrieval confidence, response length, and source count using triangular membership functions (`low`, `medium`, `high`). Uses minimum t-norm implication and maximum t-conorm aggregation, defuzzified via Centroid (Center of Gravity):
    $$z^* = \frac{\sum z \cdot \mu(z)}{\sum \mu(z)}$$
  - **Takagi-Sugeno FIS**: Uses crisp linear polynomial consequents ($z_i = p_i x_1 + q_i x_2 + r_i$) and weighted average defuzzification:
    $$z^* = \frac{\sum w_i z_i}{\sum w_i}$$
  - **ANFIS Hybrid Scorer**: A 5-layer feedforward neuro-fuzzy architecture combining gradient descent with least-squares estimation to provide unified quality scores.
- **Code Reference**: [`backend/fuzzy/mamdani_fis.py`](file:///d:/Engineering/Projects/CampusMind/backend/fuzzy/mamdani_fis.py), [`backend/fuzzy/sugeno_fis.py`](file:///d:/Engineering/Projects/CampusMind/backend/fuzzy/sugeno_fis.py), and [`backend/fuzzy/neurofuzzy.py`](file:///d:/Engineering/Projects/CampusMind/backend/fuzzy/neurofuzzy.py).

---

## 2. Computer Networks (CN)

### Q1: How did you implement error detection and checksum algorithms? (Exp 5)
- **Answer**:
  - Document uploads require multi-layered integrity verification before parsing:
  1. **SHA-256**: Cryptographic 256-bit hash to detect tampering and deduplicate identical documents.
  2. **CRC-32**: Hardware-level Cyclic Redundancy Check using standard IEEE polynomial `0xEDB88320`, catching burst bit errors.
  3. **RFC 1071 Internet Checksum**: The official 16-bit one's complement addition of 16-bit words used in TCP, UDP, and IPv4 packet headers.
- **Code Reference**: [`backend/services/checksum_service.py`](file:///d:/Engineering/Projects/CampusMind/backend/services/checksum_service.py).

### Q2: How is real-time token streaming implemented over WebSockets? (Exp 8)
- **Answer**:
  - We implemented an RFC 6455 compliant full-duplex WebSocket connection at `/api/chat/ws`.
  - The client initiates an HTTP Upgrade request. Upon acceptance, the server streams LLM tokens asynchronously chunk-by-chunk using `async for chunk in rag.stream_query(query)` without HTTP polling overhead or repeated connection handshakes.
- **Code Reference**: [`backend/routers/chat.py`](file:///d:/Engineering/Projects/CampusMind/backend/routers/chat.py#L175-L197).

### Q3: Explain your network health check and DNS resolution endpoints. (Exp 2 & 10)
- **Answer**:
  - `/api/health/ping`: Simulates an ICMP echo request/reply (PING) returning service availability and server timestamps.
  - `/api/health/services`: Performs active TCP/HTTP connectivity checks against Groq LPU API, Redis, and internal SQLite storage.
  - `/api/health/dns-lookup/{hostname}`: Resolves domain names to both IPv4 and IPv6 addresses using POSIX socket `getaddrinfo()`.
- **Code Reference**: [`backend/routers/health.py`](file:///d:/Engineering/Projects/CampusMind/backend/routers/health.py).

---

## 3. Applied Statistics (Stats)

### Q1: What exploratory data analysis (EDA) metrics are computed? (Exp 1)
- **Answer**:
  - **Measures of Central Tendency**: Arithmetic Mean ($\bar{x}$), Median (robust 50th percentile), and Mode.
  - **Measures of Dispersion**: Unbiased Sample Variance ($s^2 = \frac{\sum (x_i - \bar{x})^2}{n-1}$), Standard Deviation ($s$), Interquartile Range ($\text{IQR} = Q_3 - Q_1$), and Range ($x_{\max} - x_{\min}$).
  - **Distribution Shape**: Fisher-Pearson Skewness coefficient ($g_1 = \frac{m_3}{s^3}$) and Excess Kurtosis ($g_2 = \frac{m_4}{s^4} - 3.0$).
- **Code Reference**: [`backend/services/stats_service.py`](file:///d:/Engineering/Projects/CampusMind/backend/services/stats_service.py#L17-L64) and [`stats_notebooks/01_eda_descriptive_stats.ipynb`](file:///d:/Engineering/Projects/CampusMind/stats_notebooks/01_eda_descriptive_stats.ipynb).

### Q2: How did you prove that CAG caching is statistically faster than RAG? (Exp 5)
- **Answer**:
  - We conducted a **Two-Sample Independent Welch's t-Test** (which does not assume equal variances):
    - **Null Hypothesis ($H_0$)**: $\mu_{\text{RAG}} = \mu_{\text{CAG}}$ (No latency difference).
    - **Alternative Hypothesis ($H_1$)**: $\mu_{\text{RAG}} > \mu_{\text{CAG}}$ (CAG is significantly faster).
  - Test Results on Live Corpus:
    - $\bar{x}_{\text{RAG}} = 364.37\text{ ms}$, $\bar{x}_{\text{CAG}} = 11.76\text{ ms}$.
    - Welch $t$-statistic = $10.527$, degrees of freedom $df = 26.03$.
    - $p\text{-value} < 0.001 \ll \alpha (0.05)$.
    - We reject $H_0$. CAG achieves a **$30.99\times$ speedup** with statistical significance.
- **Code Reference**: [`backend/services/stats_service.py`](file:///d:/Engineering/Projects/CampusMind/backend/services/stats_service.py#L66-L90) and [`stats_notebooks/05_hypothesis_testing_rag_vs_cag.ipynb`](file:///d:/Engineering/Projects/CampusMind/stats_notebooks/05_hypothesis_testing_rag_vs_cag.ipynb).

### Q3: How is Linear Regression and Pearson Correlation used? (Exp 8 & 9)
- **Answer**:
  - We fit an Ordinary Least Squares (OLS) regression line modeling response time $y$ as a function of query character length $x$:
    $$y = mx + c, \quad m = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}, \quad c = \bar{y} - m\bar{x}$$
  - Computes Pearson correlation $r$ and coefficient of determination $R^2$.
- **Code Reference**: [`backend/services/stats_service.py`](file:///d:/Engineering/Projects/CampusMind/backend/services/stats_service.py#L93-L117) and [`stats_notebooks/08_regression_correlation.ipynb`](file:///d:/Engineering/Projects/CampusMind/stats_notebooks/08_regression_correlation.ipynb).

### Q4: Explain your PCA and K-Means Clustering implementation. (Exp 12)
- **Answer**:
  - Converts high-dimensional (384-D) query vectors into 2D coordinates using Principal Component Analysis (eigenvalue decomposition of the covariance matrix).
  - Applies K-Means clustering ($k=3$) to automatically group queries into semantic topic clusters, rendered in the analytics scatter plot.
- **Code Reference**: [`backend/routers/analytics.py`](file:///d:/Engineering/Projects/CampusMind/backend/routers/analytics.py#L98-L127) and [`stats_notebooks/12_pca_clustering.ipynb`](file:///d:/Engineering/Projects/CampusMind/stats_notebooks/12_pca_clustering.ipynb).

---

## 4. Wireless & Mobile Computing (WMC)

### Q1: How does Cache-Augmented Generation (CAG) optimize mobile battery consumption?
- **Answer**:
  - In cellular networks (4G LTE / 5G NR), wireless modems operate under Radio Resource Control (RRC) state machines:
    1. **Active/Connected State**: Modem consumes $\sim 1500\text{--}2000\text{ mW}$ during active data transmission.
    2. **Tail State**: The modem stays awake for $10\text{--}15\text{ seconds}$ after packet transfer before sleeping ($\sim 800\text{--}1000\text{ mW}$).
    3. **Idle/Sleep State**: Consumes only $\sim 10\text{--}20\text{ mW}$.
  - Under traditional RAG, each query triggers heavy server-side generation ($\sim 500\text{ ms}$ round-trip), keeping the radio transmitter in the high-power tail state.
  - CAG serves cached responses in **$<12\text{ ms}$**, eliminating network re-transmissions, reducing radio active time by $92\%$, and directly mitigating the cellular tail-energy phenomenon.
- **Code Reference**: [`docs/wireless_analysis.md`](file:///d:/Engineering/Projects/CampusMind/docs/wireless_analysis.md) and [`backend/services/cag_service.py`](file:///d:/Engineering/Projects/CampusMind/backend/services/cag_service.py).

### Q2: How do you monitor mobile network interface telemetry?
- **Answer**:
  - The `/api/network/telemetry` endpoint reads local network adapter statistics via `psutil`, measuring bytes sent/received, packet drops, socket connections, and link speeds.
- **Code Reference**: [`backend/routers/network.py`](file:///d:/Engineering/Projects/CampusMind/backend/routers/network.py).

---

## 5. Agile Software Development & DevOps (ASD&D)

### Q1: Describe your Git branching and interval commit strategy. (Exp 1)
- **Answer**:
  - We followed strict Agile trunk-based development with semantic interval commits corresponding to project milestones:
    - `18be42a`: Phase 1 — Project setup, backend skeleton, Groq integration, document upload with checksum
    - `22f2775`: Phase 2 — RAG pipeline, CAG cache, Groq LLM integration, WebSocket chat
    - `6275ffc`: Phase 3 — Search algorithms, Perceptron intent classifier, Fuzzy (Mamdani+Sugeno), Neuro-Fuzzy ANFIS
    - `bc85127`: Stats Layer — EDA descriptive statistics, A/B Welch t-test, linear regression
    - `3bccc6d`: Phase 4 — Next.js frontend with dark glassmorphism UI, Chat, Analytics, and Document Vault
    - `b9c229e`: Phase 5 — DevOps — Docker, Docker Compose, K8s manifests, Terraform, Ansible, Prometheus, CI/CD
    - `5aead21`: Phase 6 — Jupyter notebooks for Stats experiments, comprehensive documentation, MIT license
    - `7a2b452`: CI/CD — Multi-stage standalone output, CPU torch optimization, and automated pytest suite
    - `2a7feac`: Knowledge — Multi-subject textbook knowledge ingestion engine with Groq multi-model failover
- **Code Reference**: `git log --oneline`.

### Q2: Explain your CI/CD Pipeline architecture on GitHub Actions. (Exp 2 & 3)
- **Answer**:
  - **CI Pipeline (`.github/workflows/ci.yml`)**:
    1. Checks out repository on `ubuntu-latest`.
    2. Installs Python 3.11 with CPU-optimized PyTorch wheels.
    3. Runs automated unit test suite with `pytest tests/ -v` (testing ping, checksums, search, perceptron, fuzzy, and stats).
    4. Sets up Node.js 20, installs dependencies, and runs `npm run build` validating all Next.js pages.
  - **CD Pipeline (`.github/workflows/cd.yml`)**:
    1. Sets up Docker Buildx with OCI caching.
    2. Compiles multi-stage standalone production containers for backend and frontend.
    3. Validates orchestration configurations with `docker compose config`.
- **Status**: **100% Passing & Green** on GitHub Actions.
- **Code Reference**: [`.github/workflows/ci.yml`](file:///d:/Engineering/Projects/CampusMind/.github/workflows/ci.yml) and [`.github/workflows/cd.yml`](file:///d:/Engineering/Projects/CampusMind/.github/workflows/cd.yml).

### Q3: Why did you use multi-stage Docker builds? (Exp 4 & 5)
- **Answer**:
  - Multi-stage builds decouple the heavy build toolchain from the production runtime image:
    - **Frontend**: Builder stage installs dependencies and compiles Next.js with `output: 'standalone'`. The runner stage copies only `.next/standalone`, public assets, and static files onto a minimal `node:20-slim` container, reducing image size by $>75\%$.
    - **Backend**: Uses `python:3.11-slim` with CPU-only PyTorch wheels (`--index-url https://download.pytorch.org/whl/cpu`), avoiding bloated 900MB GPU CUDA binaries.
- **Code Reference**: [`frontend/Dockerfile`](file:///d:/Engineering/Projects/CampusMind/frontend/Dockerfile) and [`backend/Dockerfile`](file:///d:/Engineering/Projects/CampusMind/backend/Dockerfile).

### Q4: Describe your Kubernetes and Infrastructure as Code configurations. (Exp 7-10)
- **Answer**:
  - **Kubernetes**: Declarative manifests in `devops/kubernetes/` defining Deployment (with readiness/liveness probes), ClusterIP Services, ConfigMaps, and Horizontal Pod Autoscaler (HPA) targeting 70% CPU utilization.
  - **Terraform**: IaC definitions in `devops/terraform/` managing VPC, subnets, EC2, and security groups.
  - **Ansible**: Playbooks in `devops/ansible/` automating Docker engine installation, system updates, and container deployment.
  - **Prometheus & Grafana**: Service metrics exposed at `/metrics` via `prometheus-fastapi-instrumentator` and scraped on port 9090.
- **Code Reference**: [`devops/kubernetes/`](file:///d:/Engineering/Projects/CampusMind/devops/kubernetes), [`devops/terraform/`](file:///d:/Engineering/Projects/CampusMind/devops/terraform), and [`devops/docker-compose.monitoring.yml`](file:///d:/Engineering/Projects/CampusMind/devops/docker-compose.monitoring.yml).

---

## 6. Live Demonstration Script for Examiners

When presenting to professors, follow this exact sequence:

1. **Start the Stack**:
   - Backend: `cd backend && .\venv\Scripts\Activate.ps1 && uvicorn main:app --reload --port 8000`
   - Frontend: `cd frontend && npm run dev`
2. **Tab 1: Academic Chat ([http://localhost:3000/chat](http://localhost:3000/chat))**:
   - Ask an AISC question: *"How does A\* search evaluate nodes according to Russell and Norvig?"*
     - Show the citation source: `Russell & Norvig - AI: A Modern Approach (4th Ed)`.
     - Show the intent tag: `academic` (classified by Perceptron).
     - Show the Fuzzy Quality Score badge ($\sim 0.85\text{--}0.92$).
   - Ask a CN question: *"Explain CRC error detection from Tanenbaum."*
     - Show citation from Tanenbaum Chapter 3.
   - Ask the same question again to demonstrate **CAG Caching**:
     - Point out the badge changes from `RAG (Vector Store)` to `CAG (Memory Cache)`.
     - Point out the latency drop from **$\sim 450\text{ ms}$ down to $11\text{ ms}$**!
3. **Tab 2: Analytics Dashboard ([http://localhost:3000/analytics](http://localhost:3000/analytics))**:
   - Show the **A/B Welch t-Test box**: highlight $t = 10.527$, $p < 0.001$, and $30.99\times$ speedup factor.
   - Show the **EDA Descriptive Statistics table**: Mean, Variance, IQR, Skewness, Kurtosis.
   - Show the **OLS Linear Regression equation**: $y = mx + c$.
   - Show the **2D PCA & K-Means semantic cluster map**.
4. **Tab 3: Document Vault & Networking ([http://localhost:3000/admin](http://localhost:3000/admin))**:
   - Show the catalog of 14 indexed textbooks with verified SHA-256 and CRC-32 checksums.
   - Run a live DNS Lookup on `google.com` or `github.com` to demonstrate RFC socket resolution.
5. **Terminal / GitHub Actions Tab**:
   - Open GitHub Actions: show the passing **CI Pipeline** (all tests green) and **CD Pipeline** (Docker images validated).
