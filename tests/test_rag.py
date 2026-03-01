import os
import pytest
from app.rag.ingest import chunk_text

VECTOR_STORE_EXISTS = os.path.exists(
    os.path.join(os.path.dirname(__file__), "..", "vector_store", "chroma.sqlite3")
)


def test_chunk_text_basic():
    text = "a" * 1200
    chunks = chunk_text(text, chunk_size=600, overlap=100)
    assert len(chunks) == 3
    assert len(chunks[0]) == 600


def test_chunk_text_short():
    text = "short text"
    chunks = chunk_text(text, chunk_size=600, overlap=100)
    assert len(chunks) == 1
    assert chunks[0] == "short text"


def test_chunk_overlap():
    text = "abcdefghij" * 100  # 1000 chars
    chunks = chunk_text(text, chunk_size=600, overlap=100)
    # The end of chunk[0] should match the beginning of chunk[1]
    assert chunks[0][-100:] == chunks[1][:100]


@pytest.mark.skipif(not VECTOR_STORE_EXISTS, reason="Vector store not ingested yet")
def test_retrieve_returns_results():
    from app.rag.retriever import retrieve
    results = retrieve("how to restart a service")
    assert isinstance(results, list)
    assert len(results) <= 3
    if results:
        assert "text" in results[0]
        assert "source" in results[0]
