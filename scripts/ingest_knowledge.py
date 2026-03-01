"""Ingest knowledge base runbooks into Chroma vector store."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.rag.ingest import ingest

if __name__ == "__main__":
    ingest()
