import time
import uuid
import logging
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.classifier import predict
from app.rag.retriever import retrieve
from app.services.llm import generate_response

logger = logging.getLogger("app.routes")

router = APIRouter()


class TicketRequest(BaseModel):
    ticket_text: str


class RetrievedDoc(BaseModel):
    text: str
    source: str


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

    # Step 1: Classify
    classification = predict(req.ticket_text)

    # Step 2: RAG retrieval
    retrieved_docs = retrieve(req.ticket_text)

    # Step 3: Generate response
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
