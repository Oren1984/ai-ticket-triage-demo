# RAG Design

## 1. Knowledge Base

Markdown IT Runbooks stored locally.

Examples:
- restart_service.md
- reset_password.md
- check_disk_usage.md
- redeploy_container.md

## 2. Chunking Strategy

- Chunk size: 500–800 characters
- Overlap: 100 characters

## 3. Embeddings

Local embeddings (no external API).

No LLM dependency.

## 4. Vector Store

Chroma (local persistence).

Stored under:

/vector_store/

## 5. Retrieval Strategy

Top-K = 3

Returns:
- Retrieved text
- Source file