# Backend API Design

## 1. Framework

FastAPI

## 2. Endpoints

POST /predict

Request:
{
  "ticket_text": "..."
}

Response:
{
  "category": "...",
  "urgency": "...",
  "retrieved_docs": [...],
  "final_response": "...",
  "latency_ms": ...
}

## 3. Logging Requirements

- Structured JSON logs
- Unique Request ID
- Latency measurement

## 4. Project Structure

app/
  main.py
  routes.py
  services/
  models/
  rag/