# app/rag/ingest.py
# This file defines a script to ingest markdown runbooks into a Chroma vector store.
# It reads .md files from a specified knowledge directory, chunks the content into overlapping pieces,
# and stores the chunks in a Chroma collection with metadata about the source file. The script uses a mock embedding function for testing purposes.

"""Ingest markdown runbooks into Chroma vector store."""

import os
import chromadb
from app.rag.embeddings import MockEmbeddingFunction

# Configuration constants
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base")
VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "vector_store")
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
COLLECTION_NAME = "runbooks"

# Function to chunk text into overlapping pieces
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Main ingestion function
def ingest(knowledge_dir: str = KNOWLEDGE_DIR, vector_store_dir: str = VECTOR_STORE_DIR):
    """Read all .md files, chunk them, and store in Chroma."""
    client = chromadb.PersistentClient(path=vector_store_dir)

    # Delete existing collection if present, then recreate
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=MockEmbeddingFunction(),
    )
    
    # Ingest documents
    doc_id = 0
    total_chunks = 0
    for filename in sorted(os.listdir(knowledge_dir)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(knowledge_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunk_text(content)
        for chunk in chunks:
            collection.add(
                ids=[f"doc_{doc_id}"],
                documents=[chunk],
                metadatas=[{"source": filename}],
            )
            doc_id += 1
            total_chunks += 1

    print(f"Ingested {total_chunks} chunks from {knowledge_dir} into {vector_store_dir}")
    return total_chunks


if __name__ == "__main__":
    ingest()
