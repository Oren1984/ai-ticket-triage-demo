# app/rag/embeddings.py
# This file defines a mock embedding function that generates deterministic embeddings
# by hashing input text.

"""Mock embedding function — deterministic, no API key needed."""

import hashlib
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

EMBEDDING_DIM = 384

# This mock embedding function is for testing and development purposes only.
class MockEmbeddingFunction(EmbeddingFunction):
    """Generates deterministic embeddings by hashing text."""

    # The __call__ method takes a list of documents (strings) and returns a list of embeddings (lists of floats).
    def __init__(self):
        pass

    # The name method returns the name of the embedding function.
    def name(self) -> str:
        return "mock-embedding"

    # The __call__ method generates a deterministic embedding for each input document by hashing the text and converting the hash to a vector of floats.
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
