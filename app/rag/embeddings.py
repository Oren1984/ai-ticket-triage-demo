"""Mock embedding function — deterministic, no API key needed."""

import hashlib
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

EMBEDDING_DIM = 384


class MockEmbeddingFunction(EmbeddingFunction):
    """Generates deterministic embeddings by hashing text."""

    def __init__(self):
        pass

    def name(self) -> str:
        return "mock-embedding"

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            h = hashlib.sha256(text.encode("utf-8")).hexdigest()
            vec = []
            for i in range(0, min(len(h), EMBEDDING_DIM * 2), 2):
                byte_val = int(h[i : i + 2], 16)
                vec.append((byte_val / 127.5) - 1.0)
            while len(vec) < EMBEDDING_DIM:
                vec.append(0.0)
            embeddings.append(vec[:EMBEDDING_DIM])
        return embeddings
