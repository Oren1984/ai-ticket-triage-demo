# Backend API Design

## 1. Framework

FastAPI

## 2. Main Endpoint

POST /triage

Request:
{
  "ticket_text": "..."
}

Response:
{
  "category": "...",
  "urgency": "Medium",
  "retrieved_docs": [...],
  "final_response": "...",
  "latency_ms": ...
}

## 3. Additional Endpoints

POST /classify  → ML only  
GET /health     → Health check  

## 4. Logging Requirements

- Structured JSON logs
- Unique Request ID
- Latency measurement

## 5. Project Structure

app/
  main.py
  services/
  ml/
  rag/