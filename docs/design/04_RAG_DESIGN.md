# RAG Design

## 1. Knowledge Base

20–30 IT Runbook documents in Markdown format.

Examples:
- restart_service.md
- reset_password.md
- check_disk_usage.md
- redeploy_container.md

## 2. Chunking Strategy

- Chunk size: 500–800 characters
- Overlap: 100 characters

## 3. Embeddings

Use external LLM API for embeddings.

## 4. Vector Store

Use Chroma (local, simple).

Store in:

/vector_store/

## 5. Retrieval Strategy

Top-K = 3

Return:
- Retrieved text
- Source file