# Quick Demo

Three commands to get the AI Ticket Triage API running locally.

## 1. Build and start

```bash
copy .env.example .env   # Windows
# cp .env.example .env  # Linux / macOS

docker compose up --build
```

## 2. Health check

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok"}`

## 3. Classify a ticket

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"ticket_text": "Production database is unreachable from all app servers"}'
```

Example response:

```json
{
  "request_id": "3f1a2b...",
  "category": "Database Issue",
  "urgency": "High",
  "retrieved_docs": [
    {
      "text": "# PostgreSQL Replication Lag...",
      "source": "postgres_replication.md"
    }
  ],
  "final_response": "Ticket classified as **Database Issue** with **High** urgency.\n\nRecommended actions based on relevant runbooks:\n  1. [postgres_replication.md] ...",
  "latency_ms": 142.5
}
```

## Stop

```bash
docker compose down
```

---

> **No API key required** — the LLM layer uses a template-based mock (`app/services/llm.py`).
> See [RUN.md](RUN.md) for the full local Python setup.
