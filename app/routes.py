# app/routes.py
# API routes for the FastAPI application.
# Endpoints:
#   POST /triage   – main triage pipeline (new Kaggle-trained classifier)
#   POST /classify – debug: raw ML classification only
#   POST /predict  – legacy endpoint (kept for backward compatibility)

import time
import uuid
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.ml import classifier as ml_clf
from app.services.triage_service import triage as run_triage
from app.services.classifier import predict as legacy_predict
from app.rag.retriever import retrieve
from app.services.llm import generate_response

logger = logging.getLogger("app.routes")

router = APIRouter()

# ---------------------------------------------------------------------------
# Shared schemas
# ---------------------------------------------------------------------------

class TicketRequest(BaseModel):
    ticket_text: str


class RetrievedDoc(BaseModel):
    text: str
    source: str


# ---------------------------------------------------------------------------
# /triage  – main endpoint (schema-stable; may add optional fields)
# ---------------------------------------------------------------------------

class TriageTimings(BaseModel):
    classify: float
    total: float


class TriageResponse(BaseModel):
    request_id: str
    category: str
    urgency: str
    retrieved_docs: list[RetrievedDoc]
    final_response: str
    latency_ms: float
    timings_ms: Optional[TriageTimings] = None


@router.post("/triage", response_model=TriageResponse)
def triage_ticket(req: TicketRequest):
    result = run_triage(req.ticket_text)
    logger.info(
        f"request_id={result['request_id']} category={result['category']} "
        f"latency_ms={result['latency_ms']}"
    )
    return TriageResponse(
        request_id=result["request_id"],
        category=result["category"],
        urgency=result["urgency"],
        retrieved_docs=[RetrievedDoc(**d) for d in result["retrieved_docs"]],
        final_response=result["final_response"],
        latency_ms=result["latency_ms"],
        timings_ms=TriageTimings(**result["timings_ms"]) if result.get("timings_ms") else None,
    )


# ---------------------------------------------------------------------------
# /classify  – debug: ML classification only, no RAG
# ---------------------------------------------------------------------------

class ClassifyResponse(BaseModel):
    label: str
    confidence: float
    timings_ms: float


@router.post("/classify", response_model=ClassifyResponse)
def classify_ticket(req: TicketRequest):
    result = ml_clf.classify(req.ticket_text)
    return ClassifyResponse(
        label=result["label"],
        confidence=result["confidence"],
        timings_ms=result["timings_ms"],
    )


# ---------------------------------------------------------------------------
# /predict  – legacy endpoint (backward compatibility)
# ---------------------------------------------------------------------------

class TicketResponse(BaseModel):
    request_id: str
    category: str
    urgency: str
    retrieved_docs: list[RetrievedDoc]
    final_response: str
    latency_ms: float


@router.post("/predict", response_model=TicketResponse)
def predict_ticket(req: TicketRequest):
    request_id = str(uuid.uuid4())
    start = time.time()

    classification = legacy_predict(req.ticket_text)
    retrieved_docs = retrieve(req.ticket_text)
    final_response = generate_response(
        category=classification["category"],
        urgency=classification["urgency"],
        retrieved_docs=retrieved_docs,
    )

    latency_ms = round((time.time() - start) * 1000, 2)
    logger.info(
        f"request_id={request_id} category={classification['category']} "
        f"urgency={classification['urgency']} latency_ms={latency_ms}"
    )

    return TicketResponse(
        request_id=request_id,
        category=classification["category"],
        urgency=classification["urgency"],
        retrieved_docs=[RetrievedDoc(**d) for d in retrieved_docs],
        final_response=final_response,
        latency_ms=latency_ms,
    )
