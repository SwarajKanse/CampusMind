# PEAS Formulation — CampusMind (AISC Experiment 1)

## 🎯 Problem Statement
Design an intelligent, multi-subject academic assistant chatbot for engineering university students that retrieves answers from course materials, provides confidence/quality metrics, and optimizes network transfers.

## 📋 PEAS Model

| Component | Description |
|-----------|-------------|
| **Performance Measure (P)** | Response accuracy, semantic relevance (cosine similarity > 0.7), latency (<1s via Groq/CAG), cache hit rate, fuzzy quality score (Mamdani/Sugeno/ANFIS), and user satisfaction ratings. |
| **Environment (E)** | University academic repository, course syllabus, textbook chapters, mobile and Wi-Fi networks (varying packet loss and bandwidth), diverse student natural language queries. |
| **Actuators (A)** | Streamed response text, source citations (document name + chunk index), confidence scores, fuzzy quality metrics, network telemetry indicators, cached responses. |
| **Sensors (S)** | Natural language text inputs, uploaded document files (PDF/TXT), network socket connections, ping round-trip times, user feedback/ratings. |

---

## 🤖 Agent Classification & Properties

- **Agent Type**: Goal-based & Utility-based Intelligent Agent with Learning Capability.
- **Environment Properties**:
  - **Partially Observable**: The agent only knows the text chunks stored in its vector database and context window.
  - **Deterministic / Stochastic**: Retrieval is deterministic; LLM sampling has low temperature (0.3) for high reproducibility.
  - **Sequential**: Previous query logs and cache entries inform future responses and performance tuning.
  - **Dynamic**: New documents can be uploaded at runtime, updating the knowledge base dynamically.
  - **Continuous**: Response times, confidence values, and fuzzy membership degrees operate over continuous domains.
  - **Multi-Agent**: Client-server architecture with distributed microservices (FastAPI backend, Groq cloud inference engine, Redis cache, Next.js frontend).

---

## 🧠 Reasoning & Learning Systems
1. **Search**: BFS & DFS for unguided exploration of chunk graph; A* search heuristic ($f(n) = g(n) + h(n)$) where $h(n)$ is embedding cosine distance.
2. **Learning**: Multi-class Perceptron (AISC Exp 7 & 8) trained to categorize incoming student queries into intents: `academic`, `general`, `feedback`, `greeting`.
3. **Fuzzy Reasoning**: Triple-engine quality assessment (Mamdani FIS, Sugeno FIS, and ANFIS Neuro-Fuzzy) evaluating response length, confidence, and source citations.
