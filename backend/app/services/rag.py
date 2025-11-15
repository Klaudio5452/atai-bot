# app/services/rag.py
# Lightweight mock RAG module for free Render deployment.
# This version skips FAISS and SentenceTransformer entirely.

class RAG:
    def __init__(self, llm_client=None, model_name="mock-model"):
        self.llm = llm_client
        self.model_name = model_name
        self.documents = []
        print("[RAG MOCK] Initialized lightweight RAG (no embeddings loaded).")

    def index_documents(self, docs):
        """Pretend to index documents (mock mode)."""
        if not docs:
            return
        self.documents.extend(docs)
        print(f"[RAG MOCK] Indexed {len(docs)} docs (mock mode).")

    def retrieve(self, query, top_k=3):
        """Return up to top_k stored docs (mock mode)."""
        if not self.documents:
            return []
        print(f"[RAG MOCK] Retrieving from {len(self.documents)} fake docs.")
        return self.documents[:top_k]
