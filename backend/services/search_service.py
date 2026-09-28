"""
Graph-based document search using BFS, DFS, and A*.
AISC Exp 3: Uninformed search (BFS, DFS)
AISC Exp 4: Informed search (A*)
"""
import heapq
from collections import deque
import numpy as np


class SearchService:
    def build_adjacency(self, documents: list[str], embeddings: list[list[float]], threshold: float = 0.7) -> dict:
        """Build document chunk graph based on embedding cosine similarity."""
        adjacency = {i: [] for i in range(len(documents))}
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]) + 1e-10
                )
                if sim >= threshold:
                    adjacency[i].append(j)
                    adjacency[j].append(i)
        return adjacency

    def bfs_search(self, start: int, adjacency: dict, max_nodes: int = 10) -> list[int]:
        """BFS traversal of document graph. AISC Exp 3."""
        visited = set()
        queue = deque([start])
        result = []
        while queue and len(result) < max_nodes:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in adjacency.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
        return result

    def dfs_search(self, start: int, adjacency: dict, max_nodes: int = 10) -> list[int]:
        """DFS traversal of document graph. AISC Exp 3."""
        visited = set()
        stack = [start]
        result = []
        while stack and len(result) < max_nodes:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in reversed(adjacency.get(node, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return result

    def a_star_search(
        self,
        query_embedding: list[float],
        doc_embeddings: list[list[float]],
        documents: list[str],
        top_k: int = 5
    ) -> list[dict]:
        """
        A* search: rank documents by f(n) = g(n) + h(n).
        g(n) = exploration path cost (order index factor)
        h(n) = cosine distance to query (heuristic)
        AISC Exp 4.
        """
        heap = []
        query_vec = np.array(query_embedding)
        for i, emb in enumerate(doc_embeddings):
            emb_vec = np.array(emb)
            cosine_dist = 1.0 - (
                np.dot(query_vec, emb_vec) /
                (np.linalg.norm(query_vec) * np.linalg.norm(emb_vec) + 1e-10)
            )
            g = i * 0.05
            h = float(cosine_dist)
            f = g + h
            heapq.heappush(heap, (f, i))

        results = []
        while heap and len(results) < top_k:
            f_val, idx = heapq.heappop(heap)
            results.append({
                "index": idx,
                "document": documents[idx],
                "f_score": round(float(f_val), 4),
                "relevance": round(float(1.0 - f_val), 4),
            })
        return results


search_service = SearchService()
