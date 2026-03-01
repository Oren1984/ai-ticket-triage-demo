# Implementation Summary

**Project:** AI Ticket Triage + RAG Assistant
**Type:** End-to-End Applied AI Demo (Lean MVP)
**Author:** Oren

---

## 1. Architecture Overview

```
User Request
     |
     v
[ FastAPI POST /predict ]
     |
     v
[ Text Preprocessing ]   -- lowercase, strip special chars, normalize whitespace
     |
     v
[ ML Classification ]    -- TF-IDF vectorizer + Logistic Regression (x2)
     |                       outputs: category (6 classes), urgency (3 levels)
     v
[ RAG Retrieval ]         -- Chroma vector store, top-3 similar runbook chunks
     |
     v
[ Response Generation ]   -- template-based (mock LLM, no API key required)
     |
     v
JSON Response (request_id, category, urgency, retrieved_docs, final_response, latency_ms)
```

All components run in a single Python process. No external services, GPUs, or API keys required.

---

## 2. Layer-by-Layer Breakdown

### 2.1 Dataset

| Property | Value |
|---|---|
| File | `data/tickets.json` |
| Records | 1,002 |
| Categories | 6 (balanced at ~167 each) |
| Urgency levels | 3 (Low 30%, Medium 40%, High 30%) |
| Generation | Deterministic templates with random substitution (`random.seed(42)`) |

**Categories:** Network Issue, Access / Permissions, Deployment Failure, Monitoring / Alert, Database Issue, Infrastructure Issue.

Each category has 18 unique sentence templates with variable slots (`{target}`, `{source}`, `{user}`, `{n}`, `{stage}`, `{error}`, `{port}`) filled from curated pools of realistic values (20 server targets, 10 network sources, 10 usernames, etc.).

**Generator:** `scripts/generate_dataset.py` — fully self-contained, no external dependencies.

---

### 2.2 ML Baseline

| Property | Value |
|---|---|
| Algorithm | TF-IDF + Logistic Regression |
| Vectorizer | `TfidfVectorizer(max_features=5000, ngram_range=(1, 2))` |
| Models | Two separate classifiers — one for category, one for urgency |
| Train/Test split | 80/20, `random_state=42` |
| Persistence | Joblib serialization to `models/` directory |

**Training script:** `scripts/train_model.py`

**Saved artifacts:**
- `models/vectorizer.pkl` — fitted TF-IDF vectorizer
- `models/category_model.pkl` — category LogisticRegression
- `models/urgency_model.pkl` — urgency LogisticRegression

**Evaluation results:**

| Task | Accuracy | Macro F1 |
|---|---|---|
| Category | 1.00 | 1.00 |
| Urgency | 0.36 | 0.29 |

Category performance is perfect because the synthetic templates contain strong category-specific keywords. Urgency performance is low because urgency is assigned randomly during generation — the text carries no urgency signal. This is expected and documented as a known limitation.

**Runtime behavior:** Models are loaded lazily on first prediction and cached in module-level globals, avoiding redundant disk reads.

---

### 2.3 RAG Pipeline

| Property | Value |
|---|---|
| Knowledge base | 20 markdown runbook documents in `knowledge_base/` |
| Vector store | ChromaDB (persistent, SQLite-backed) |
| Embedding | Mock deterministic function (SHA256-based, 384 dimensions) |
| Chunking | 600-character chunks, 100-character overlap |
| Retrieval | Top-K = 3 most similar chunks |
| Storage path | `vector_store/` |

**Ingestion script:** `scripts/ingest_knowledge.py` (calls `app/rag/ingest.py`)

**Runbook documents cover:**

| Domain | Files |
|---|---|
| Network/Connectivity | `vpn_troubleshoot.md`, `dns_resolution.md`, `firewall_rules.md`, `network_latency.md`, `nginx_config.md` |
| Database | `database_backup.md`, `postgres_replication.md`, `redis_cache_clear.md` |
| Deployment/CI | `redeploy_container.md`, `ci_cd_pipeline_fix.md` |
| Infrastructure | `aws_ec2_recovery.md`, `k8s_pod_restart.md`, `restart_service.md`, `ssl_cert_renew.md` |
| Access/Security | `reset_password.md`, `permission_escalation.md` |
| Monitoring/Ops | `check_disk_usage.md`, `log_rotation.md`, `memory_leak_debug.md`, `monitoring_alerts.md` |

Each runbook contains a title, brief description, and 6-8 numbered steps with real CLI commands.

**Ingestion result:** 40 chunks stored in the Chroma collection `runbooks`.

**Retrieval flow:** Query text is embedded using the same mock function, then cosine similarity search returns the 3 closest chunks with their source filenames.

---

### 2.4 FastAPI Backend

| Property | Value |
|---|---|
| Framework | FastAPI 0.115.6 |
| Server | Uvicorn |
| Endpoints | `POST /predict`, `GET /health` |

**`POST /predict`**

Request:
```json
{ "ticket_text": "Cannot connect to production database" }
```

Response:
```json
{
  "request_id": "uuid-v4",
  "category": "Database Issue",
  "urgency": "High",
  "retrieved_docs": [
    { "text": "...", "source": "postgres_replication.md" }
  ],
  "final_response": "Ticket classified as **Database Issue** with **High** urgency...",
  "latency_ms": 42.5
}
```

The endpoint orchestrates three steps sequentially: classify → retrieve → generate. All input/output is validated via Pydantic models (`TicketRequest`, `TicketResponse`, `RetrievedDoc`).

**`GET /health`** — returns `{"status": "ok"}` for readiness checks.

---

### 2.5 Logging

| Property | Value |
|---|---|
| Format | Structured JSON to stdout |
| Fields | `time`, `level`, `name`, `message` |
| Request tracking | UUID v4 `request_id` per prediction |
| Latency | Measured in milliseconds, included in both response and log |

Example log line:
```json
{"time":"2026-03-01 11:15:19","level":"INFO","name":"app.routes","message":"request_id=e2042cf2... category=Database Issue urgency=High latency_ms=42.5"}
```

JSON logging was chosen for easy integration with log aggregation tools (ELK, CloudWatch, Datadog).

---

### 2.6 Testing

| File | Tests | Type | What it covers |
|---|---|---|---|
| `test_preprocessing.py` | 5 | Unit | `clean_text()`: lowercase, special chars, whitespace, combined, empty |
| `test_classifier.py` | 3 | Unit | `predict()`: required keys, valid category, valid urgency |
| `test_rag.py` | 4 | Unit | `chunk_text()`: basic, short, overlap; `retrieve()`: results structure |
| `test_integration.py` | 2 | Integration | Full `POST /predict` flow; `GET /health` |
| **Total** | **14** | | |

All 14 tests pass. Classifier and integration tests use `@pytest.mark.skipif` to gracefully skip when models or vector store haven't been built yet, making the test suite usable at any stage of setup.

---

### 2.7 Docker Setup

**Dockerfile** — multi-step build on `python:3.11-slim`:
1. Install dependencies from `requirements.txt`
2. Copy project files
3. Run `scripts/train_model.py` at build time
4. Run `scripts/ingest_knowledge.py` at build time
5. Start uvicorn on port 8000

**docker-compose.yml** — single service:
- Service: `api`
- Port: `8000:8000`
- Env file: `.env`
- Volume: `./vector_store:/app/vector_store` (persistent)

The design decision to train and ingest at build time means containers start instantly with zero initialization delay.

---

## 3. Design Decisions

| Decision | Rationale |
|---|---|
| **Template-based dataset** | Provides consistent, reproducible training data without requiring LLM API calls. Enables perfect category separation for a clear demo. |
| **Separate category/urgency models** | Allows independent evaluation and tuning. Category prediction benefits from text features; urgency is an independent axis. |
| **TF-IDF over transformers** | No GPU required. Fast training (~1 second). Sufficient for template-based data. Aligns with "lean MVP" requirement. |
| **Mock embeddings (SHA256)** | Eliminates API key dependency. Deterministic and reproducible. Allows the full RAG pipeline to function end-to-end. |
| **Template-based LLM response** | No API key required. Demonstrates the response generation step without external dependencies. |
| **Lazy model loading** | Models are loaded on first request and cached. Avoids startup cost if health checks run before predictions. |
| **Build-time training in Docker** | Container starts instantly. No runtime initialization. Reproducible from a clean build. |
| **JSON structured logging** | Industry standard for observability pipelines. Easy to parse, filter, and aggregate. |

---

## 4. Simplifications

| Area | Simplification |
|---|---|
| **Embeddings** | SHA256 hash instead of real semantic embeddings. Retrieval quality is approximate — not semantically aware. |
| **LLM generation** | Template string instead of real LLM API call. Output is structured but not context-aware. |
| **Urgency prediction** | Random assignment in training data means urgency model cannot learn meaningful patterns from text alone. |
| **Authentication** | No auth on API endpoints. Suitable for local demo only. |
| **Error handling** | Minimal — relies on FastAPI's default exception handling. |
| **Data validation** | Basic Pydantic validation only. No input sanitization beyond preprocessing. |

---

## 5. Mock Components

| Component | What's mocked | What a real version would use |
|---|---|---|
| **Embeddings** | `MockEmbeddingFunction` — SHA256 hash → 384D float vector | OpenAI `text-embedding-3-small`, Cohere `embed-v3`, or sentence-transformers |
| **LLM generation** | `generate_response()` — markdown template | OpenAI GPT-4, Anthropic Claude, or similar via API |
| **Dataset** | Synthetic template-based tickets | Real IT ticketing system export (ServiceNow, Jira, etc.) |

All mock components implement the same interfaces as their real counterparts, making replacement straightforward.

---

## 6. Known Limitations

1. **Urgency classification is weak (F1 ~0.29)** — urgency is randomly assigned in the synthetic data and has no correlation with ticket text. A real dataset with human-labeled urgency would dramatically improve this.

2. **RAG retrieval is approximate** — the mock embedding function maps text to vectors via hashing, not semantic understanding. Two semantically similar but lexically different texts may not be retrieved together.

3. **No real LLM integration** — the response generation is a template, not a context-aware LLM completion. The architecture supports swapping in a real LLM client.

4. **Single-process, single-threaded** — uvicorn runs with one worker by default. Not designed for concurrent load.

5. **No persistent request logging** — logs go to stdout only. No database or file persistence for request history.

6. **Category model overfits on templates** — real tickets with diverse language would require a larger, more varied dataset or pre-trained embeddings.

---

## 7. Demo Script (3-Minute Walkthrough)

### Minute 1 — Context and Architecture (30 seconds talk + 30 seconds visual)

> "This is an AI-powered IT ticket triage system. It takes a raw support ticket, classifies it by category and urgency, retrieves relevant runbook documentation, and generates an actionable response — all in a single API call."

Show the architecture diagram from Section 1.

### Minute 2 — Live API Demo (60 seconds)

Start the server (or have it running):
```bash
uvicorn app.main:app --port 8000
```

Send a request:
```bash
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"ticket_text\": \"VPN tunnel dropped. Remote users cannot access internal services.\"}" | python -m json.tool
```

Walk through the response:
- "Category correctly identified as **Network Issue**"
- "Urgency assigned as **Medium**"
- "Three relevant runbook chunks retrieved — notice `vpn_troubleshoot.md` appears"
- "Response generated with actionable next steps"
- "Latency measured at **X ms** — well under the 5-second target"

### Minute 3 — Engineering Depth (60 seconds)

> "Under the hood: TF-IDF + Logistic Regression for classification — simple, fast, no GPU. Chroma vector store for document retrieval with 20 ingested runbooks. Structured JSON logging with unique request IDs for observability. 14 passing tests covering preprocessing, classification, RAG, and full integration. The entire system starts with a single `docker compose up --build`."

Show:
```bash
python -m pytest tests/ -v    # 14 passed
docker compose up --build      # one command deployment
```

---

## 8. Future Improvements

| Priority | Improvement | Effort |
|---|---|---|
| **High** | Replace mock embeddings with real embedding API (OpenAI/Cohere) | Small — swap `MockEmbeddingFunction` with API-backed class |
| **High** | Replace template response with real LLM API call | Small — update `llm.py` to call OpenAI/Claude API |
| **High** | Use real labeled ticket data instead of synthetic templates | Medium — requires data sourcing and cleaning |
| **Medium** | Add urgency signals to dataset (keyword correlation, SLA metadata) | Medium — improves urgency F1 significantly |
| **Medium** | Add Prometheus metrics endpoint (`/metrics`) | Small — use `prometheus-fastapi-instrumentator` |
| **Medium** | Add request history to SQLite for audit trail | Small — append predictions to a local database |
| **Low** | Add Streamlit or Gradio frontend | Medium — simple UI for non-technical demos |
| **Low** | Add multi-worker uvicorn configuration | Small — `--workers 4` in CMD |
| **Low** | Add CI/CD pipeline (GitHub Actions) | Small — lint, test, build Docker image |
| **Low** | Evaluate transformer-based classifier (DistilBERT) | Medium — better generalization, still CPU-friendly |

---

## 9. Repository Statistics

| Metric | Value |
|---|---|
| Python source files | 15 |
| Total Python lines | ~700 |
| Test cases | 14 (all passing) |
| Dataset records | 1,002 |
| Knowledge base docs | 20 |
| Ingested chunks | 40 |
| Model artifacts | 3 (.pkl) |
| External API dependencies | 0 |
| Docker services | 1 |

---

## 10. File Reference

```
ai-ticket-triage-demo/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, structured logging setup
│   ├── routes.py                # POST /predict, GET /health
│   ├── services/
│   │   ├── __init__.py
│   │   ├── preprocessing.py     # clean_text() — lowercase, regex, whitespace
│   │   ├── classifier.py        # Lazy-loaded TF-IDF + LogReg prediction
│   │   └── llm.py               # Template-based mock LLM response
│   └── rag/
│       ├── __init__.py
│       ├── embeddings.py        # MockEmbeddingFunction (SHA256 → 384D)
│       ├── ingest.py            # Chunk markdown, store in Chroma
│       └── retriever.py         # Query Chroma, return top-3
├── scripts/
│   ├── generate_dataset.py      # 1002 synthetic tickets
│   ├── train_model.py           # Train + evaluate + save models
│   └── ingest_knowledge.py      # Ingest runbooks into vector store
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py    # 5 tests
│   ├── test_classifier.py       # 3 tests
│   ├── test_rag.py              # 4 tests
│   └── test_integration.py      # 2 tests
├── data/
│   └── tickets.json             # Training dataset
├── knowledge_base/              # 20 markdown runbooks
├── models/                      # Trained .pkl artifacts
├── vector_store/                # Chroma persistent DB
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env / .env.example
├── .gitignore
└── RUN.md
```
