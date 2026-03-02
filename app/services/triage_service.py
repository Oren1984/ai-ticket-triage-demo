# app/services/triage_service.py
# Orchestrates the full triage pipeline:
#   classify → RAG retrieve → template response

import time
import uuid

from app.ml import classifier as ml_clf
from app.rag.retriever import retrieve
from app.services.llm import generate_response


def triage(ticket_text: str) -> dict:
    """Run the full triage pipeline and return a structured result dict.

    Returned keys:
        request_id, category, urgency, retrieved_docs,
        final_response, latency_ms, timings_ms (optional breakdown)
    """
    request_id = str(uuid.uuid4())
    t_start = time.perf_counter()

    # 1. ML classification
    classification = ml_clf.classify(ticket_text)
    category = classification["label"]

    # 2. RAG retrieval
    retrieved_docs = retrieve(ticket_text)

    # 3. Template response
    final_response = generate_response(
        category=category,
        urgency="Medium",           # dataset has no urgency label; keep field for schema compat
        retrieved_docs=retrieved_docs,
    )

    latency_ms = round((time.perf_counter() - t_start) * 1000, 2)

    return {
        "request_id": request_id,
        "category": category,
        "urgency": "Medium",
        "retrieved_docs": retrieved_docs,
        "final_response": final_response,
        "latency_ms": latency_ms,
        "timings_ms": {
            "classify": classification["timings_ms"],
            "total": latency_ms,
        },
    }
