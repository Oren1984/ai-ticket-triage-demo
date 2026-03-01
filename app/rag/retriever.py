# app/rag/retriever.py
# This file defines a function to retrieve relevant runbook chunks from a Chroma vector store based on a query.
# It connects to the Chroma collection, performs a similarity search using a mock embedding function, and returns the top-K results with their source metadata.
# The retriever is designed to be used in the RAG pipeline for ticket triage.

"""Retrieve relevant runbook chunks from Chroma."""

import os
import chromadb
from app.rag.embeddings import MockEmbeddingFunction

# Configuration constants
VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "vector_store")
COLLECTION_NAME = "runbooks"
TOP_K = 3

# Function to retrieve relevant chunks based on a query
def retrieve(query: str, top_k: int = TOP_K, vector_store_dir: str = VECTOR_STORE_DIR) -> list[dict]:
    """Query the vector store and return top-K results."""
    client = chromadb.PersistentClient(path=vector_store_dir)

    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=MockEmbeddingFunction(),
        )
    except Exception:
        return []

    results = collection.query(query_texts=[query], n_results=top_k)

    # Process results to extract text and source metadata
    docs = []
    if results and results["documents"]:
        for i, doc_text in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            docs.append({
                "text": doc_text,
                "source": metadata.get("source", "unknown"),
            })
    return docs
