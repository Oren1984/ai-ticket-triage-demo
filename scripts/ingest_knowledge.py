# scripts/ingest_knowledge.py
# This script is responsible for ingesting knowledge base runbooks into the Chroma vector store.
# It imports the ingest function from the app.rag.ingest module and executes it when the script is run directly.
# This allows for easy population of the vector store with relevant documents for retrieval during ticket triage.

"""Ingest knowledge base runbooks into Chroma vector store."""

import os
import sys

# Add the parent directory to the Python path to allow importing from the app package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.rag.ingest import ingest

if __name__ == "__main__":
    ingest()
