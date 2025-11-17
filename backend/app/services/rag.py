"""
Lightweight FAISS-based RAG helper for Render testing.
Lazily loads the SentenceTransformer only when needed.
"""

import os
import numpy as np
import faiss

class RAG:
    def __init__(self, llm_client=None, model_name="all-MiniLM-L6-v2"):
        self.llm = llm_client
        self.model_name = model_name
        self.embedder = None
        self.dim = 384  # default for all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.dim)
        self.documents = []
        self.mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"

    def _load_model(self):
        """Load model only when actually needed."""
        if self.embedder is None and not self.mock_mode:
            from sentence_transformers import SentenceTransformer
            self.embedder = SentenceTransformer(self.model_name)

    def _embed(self, texts):
        """Return fake or real embeddings."""
        if self.mock_mode:
            # Fake embeddings for Render free tier (no model load)
            return np.random.rand(len(texts), self.dim).astype("float32")
        else:
            self._load_model()
            return self.embedder.encode(texts, convert_to_numpy=True)

    def index_documents(self, docs: list[str]):
        if not docs:
            return
        embs = self._embed(docs)
        if embs.ndim == 1:
            embs = embs.reshape(1, -1)
        self.index.add(embs)
        self.documents.extend(docs)

    def retrieve(self, query: str, top_k: int = 3):
        if len(self.documents) == 0:
            return []
        q_emb = self._embed([query])
        D, I = self.index.search(q_emb, top_k)
        hits = []
        for i in I[0]:
            if i < len(self.documents):
                hits.append(self.documents[i])
        return hits
