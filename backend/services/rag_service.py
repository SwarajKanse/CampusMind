"""
RAG (Retrieval-Augmented Generation) Service.
AISC Exp 11: RAG Framework for Contextual Question Answering.
"""
from config import settings
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService


class RAGService:
    def __init__(self):
        import chromadb
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
        self.llm = LLMService()

    async def query(self, query_text: str, top_k: int = 5) -> dict:
        query_embedding = EmbeddingService.encode_single(query_text)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        documents = results["documents"][0] if results.get("documents") and results["documents"] else []
        metadatas = results["metadatas"][0] if results.get("metadatas") and results["metadatas"] else []
        distances = results["distances"][0] if results.get("distances") and results["distances"] else []

        context = "\n\n---\n\n".join(documents[:5])

        prompt = f"""You are CampusMind, an intelligent academic assistant chatbot for university students.
Answer the question based ONLY on the provided context from academic documents.
If the context doesn't contain the answer, say "I don't have enough information from the uploaded documents to answer this question."
Be concise but thorough. Use bullet points for clarity when appropriate.

Context from academic documents:
{context if context else "No documents have been uploaded yet."}

Student's Question: {query_text}

Answer:"""

        answer = await self.llm.generate(prompt)

        confidence = 0.0
        if distances:
            avg_similarity = 1 - (sum(distances) / len(distances))
            confidence = min(max(avg_similarity, 0.0), 1.0)

        sources = [m.get("source", "unknown") for m in metadatas[:5]]

        return {"answer": answer, "sources": sources, "confidence": round(confidence, 3)}

    async def stream_query(self, query_text: str, top_k: int = 5):
        query_embedding = EmbeddingService.encode_single(query_text)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents"]
        )
        documents = results["documents"][0] if results.get("documents") and results["documents"] else []
        context = "\n\n---\n\n".join(documents[:5])

        prompt = f"""You are CampusMind, an academic assistant chatbot. Answer based on the provided context.

Context:
{context if context else "No documents uploaded."}

Question: {query_text}

Answer:"""

        async for chunk in self.llm.stream_generate(prompt):
            yield chunk

    def add_documents(self, chunks: list[dict]):
        texts = [c["text"] for c in chunks]
        embeddings = EmbeddingService.encode(texts)
        ids = [f"chunk_{c['doc_id']}_{c['chunk_idx']}" for c in chunks]
        metadatas = [{"source": c["source"], "chunk_idx": c["chunk_idx"]} for c in chunks]
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
