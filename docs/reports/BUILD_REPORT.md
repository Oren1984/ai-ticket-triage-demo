# Build Report

**Project:** AI Ticket Triage + RAG Assistant
**Build system:** Docker + Docker Compose
**Base image:** `python:3.11-slim` (Debian, ~150MB)

---

## 1. Build Pipeline: `docker compose build`

The Docker build executes 7 discrete steps, each cached as a separate layer.

### Step-by-step breakdown

| Step | Dockerfile instruction | What happens | Observed time |
|---|---|---|---|
| 1 | `FROM python:3.11-slim` | Pulls base Python 3.11 image (if not cached) | ~3s |
| 2 | `WORKDIR /app` | Sets working directory inside container | <0.1s |
| 3 | `COPY requirements.txt .` | Copies only the requirements file (enables dependency caching) | <0.1s |
| 4 | `RUN pip install --no-cache-dir -r requirements.txt` | Downloads and installs all Python dependencies | **~53s** |
| 5 | `COPY . .` | Copies project source code, data, and knowledge base | ~0.2s |
| 6 | `RUN python scripts/train_model.py` | Trains TF-IDF + LogReg models, saves .pkl files | **~3.2s** |
| 7 | `RUN python scripts/ingest_knowledge.py` | Chunks 20 runbooks, embeds, stores in Chroma | **~2.4s** |

**Total build time (cold): ~85 seconds**
**Rebuild after code change only (steps 5-7): ~6 seconds** (dependency layer cached)

### Layer caching strategy

The Dockerfile is structured so that the expensive dependency installation (step 4) is cached unless `requirements.txt` changes. Code changes only invalidate steps 5-7, keeping rebuilds fast at ~6 seconds.

```
requirements.txt changes  →  full rebuild (~85s)
Source code changes only   →  partial rebuild (~6s)
No changes                 →  fully cached (<1s)
```

### .dockerignore

The `.dockerignore` file prevents build artifacts from leaking into the image:

```
vector_store/    # Host Chroma DB (incompatible version risk)
models/          # Host .pkl files (rebuilt inside container)
__pycache__/     # Python bytecode
.env             # Secrets
.git/            # Repository history
.claude/         # IDE settings
.pytest_cache/   # Test cache
```

This is critical: the `vector_store/` exclusion prevents a chromadb version mismatch between the host (where a different chromadb version may be installed) and the container. The container builds its own vector store from scratch during step 7.

---

## 2. Runtime: `docker compose up`

### What `docker-compose.yml` configures

| Setting | Value | Purpose |
|---|---|---|
| Service name | `api` | Single service, no microservices |
| Build context | `.` (current directory) | Uses local Dockerfile |
| Port mapping | `8000:8000` | Exposes API on host port 8000 |
| Env file | `.env` | Loads environment variables |
| Environment | `LOG_LEVEL=info` | Explicit log level override |
| Volume | `./vector_store:/app/vector_store` | Persists Chroma DB across restarts |

### Startup sequence

1. Docker creates and starts the container
2. Uvicorn launches on `0.0.0.0:8000` with a single worker
3. FastAPI application registers routes (`POST /predict`, `GET /health`)
4. Server is immediately ready — no initialization delay

**Time from container start to first request: <1 second**

This is possible because all heavy work (training + ingestion) happened at build time. The container starts with pre-trained models and a populated vector store baked into the image.

---

## 3. Dependency Installation (Step 4)

### Direct dependencies (10 packages)

| Package | Version | Purpose |
|---|---|---|
| fastapi | 0.115.6 | API framework |
| uvicorn | 0.34.0 | ASGI server |
| pydantic | 2.10.4 | Request/response validation |
| scikit-learn | 1.6.1 | TF-IDF + Logistic Regression |
| joblib | 1.4.2 | Model serialization |
| numpy | 2.2.1 | Numerical operations |
| pandas | 2.2.3 | Data loading |
| chromadb | 1.5.2 | Vector store |
| pytest | 8.3.4 | Testing (included for in-container test runs) |
| httpx | 0.28.1 | HTTP client for test suite |

### Transitive dependency tree

The 10 direct dependencies resolve to ~80 installed packages. The heaviest subtrees:

- **chromadb** pulls in: onnxruntime, tokenizers, grpcio, opentelemetry, kubernetes, huggingface-hub
- **scikit-learn** pulls in: scipy (~35MB), threadpoolctl
- **pandas** pulls in: pytz, tzdata, python-dateutil

`--no-cache-dir` is used to avoid storing pip's download cache in the image, reducing layer size.

---

## 4. Model Training (Step 6)

### What happens

1. Loads `data/tickets.json` (1,002 records)
2. Preprocesses all ticket text (lowercase, strip special chars, normalize whitespace)
3. Fits `TfidfVectorizer(max_features=5000, ngram_range=(1,2))`
4. Trains `LogisticRegression(max_iter=1000)` for category (6 classes)
5. Trains `LogisticRegression(max_iter=1000)` for urgency (3 classes)
6. Evaluates both on 20% held-out test set
7. Saves 3 artifacts to `models/`:
   - `vectorizer.pkl`
   - `category_model.pkl`
   - `urgency_model.pkl`

### Build output (from observed run)

```
Loaded 1002 tickets

=== Category Classification ===
Accuracy: 1.0000
Macro F1: 1.00

=== Urgency Classification ===
Accuracy: 0.3632
Macro F1: 0.29

Models saved to /app/models/
```

**Duration: 3.2 seconds**

---

## 5. Knowledge Ingestion (Step 7)

### What happens

1. Reads all 20 `.md` files from `knowledge_base/`
2. Chunks each document into 600-character segments with 100-character overlap
3. Embeds each chunk using `MockEmbeddingFunction` (SHA256 hash to 384D vector)
4. Stores all chunks in Chroma persistent collection `runbooks`
5. Chroma writes SQLite database to `vector_store/`

### Build output

```
Ingested 40 chunks from /app/knowledge_base into /app/vector_store
```

**Duration: 2.4 seconds**

---

## 6. Why Build-Time Training Was Chosen

### The decision

Model training and knowledge ingestion run as `RUN` commands during `docker build`, not at container startup.

### Advantages

| Advantage | Explanation |
|---|---|
| **Instant startup** | Container is ready in <1 second. No waiting for training or ingestion. |
| **Reproducible builds** | Same Dockerfile always produces the same trained models (deterministic seeds). |
| **Cacheable** | Docker layer cache means training only re-runs when code or data changes. |
| **No runtime failures** | If training or ingestion fails, the build fails — you never deploy a broken image. |
| **Smaller attack surface** | Runtime container only serves predictions, never runs training scripts. |

### Trade-offs

| Trade-off | Impact | Mitigation |
|---|---|---|
| **Larger image size** | Model artifacts and vector store are baked into the image | Acceptable for a demo; use multi-stage build for production |
| **Full rebuild on data change** | Changing `tickets.json` or runbooks triggers training/ingestion re-run | Docker layer cache limits this to steps 5-7 (~6s) |
| **No hot model updates** | Updating models requires a new image build and container restart | Acceptable for MVP; production would use a model registry |
| **Build requires compute** | CI/CD runners need enough RAM for training (~512MB) | Training is lightweight (TF-IDF, no GPU) |

---

## 7. Failure Scenarios

### Missing dependency in requirements.txt

**Symptom:** Build fails at step 4 (`pip install`) with `ERROR: No matching distribution found`.

**Impact:** Build stops entirely. No image is produced. No broken container can be started.

**Recovery:** Fix the version pin in `requirements.txt` and rebuild. Docker will re-run step 4 from scratch (no cache hit on changed requirements file).

**Example:** If `chromadb==1.5.2` were removed, step 7 would fail with `ModuleNotFoundError: No module named 'chromadb'`. In practice, step 4 catches most issues earlier.

### vector_store volume not mounted

**Symptom:** The API starts successfully (vector store is baked into the image at build time). However, the Chroma DB state is not persisted between container restarts.

**Impact:**
- **First run:** Works correctly — uses the build-time vector store inside the image.
- **Subsequent restarts:** Still works — falls back to the image's baked-in vector store.
- **If container is rebuilt without the volume:** No data loss — vector store is recreated during build.

**When this matters:** Only if you modify the vector store at runtime (e.g., adding documents via an API) and expect those changes to survive container restarts. For this MVP, the volume mount is a convenience, not a requirement.

### data/tickets.json missing or malformed

**Symptom:** Build fails at step 6 (`train_model.py`) with `FileNotFoundError` or `json.JSONDecodeError`.

**Impact:** Build stops. No image produced.

**Recovery:** Regenerate with `python scripts/generate_dataset.py`, then rebuild.

### knowledge_base/ directory empty

**Symptom:** Build succeeds but step 7 ingests 0 chunks. API returns empty `retrieved_docs` arrays.

**Impact:** Classification still works. RAG retrieval returns no results. Response generation falls back to "No relevant runbook documents found."

### Port 8000 already in use

**Symptom:** `docker compose up` fails with `Bind for 0.0.0.0:8000 failed: port is already allocated`.

**Recovery:** Stop the conflicting process, or change the port mapping in `docker-compose.yml` (e.g., `"8001:8000"`).

---

## 8. Demo Readiness Checklist

Before presenting, verify all five:

- [ ] **`docker compose up --build` completes without errors** — build exits cleanly, container starts, uvicorn prints "Application startup complete"
- [ ] **`curl http://localhost:8000/health` returns `{"status":"ok"}`** — API is reachable and responding
- [ ] **`curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"ticket_text":"test"}'` returns valid JSON** — full pipeline (classify + RAG + response) works end-to-end
- [ ] **Response includes all required fields** — `request_id`, `category`, `urgency`, `retrieved_docs`, `final_response`, `latency_ms` are all present and non-empty
- [ ] **`latency_ms` is under 5000** — meets the <5 second end-to-end performance target (first request may be ~2s due to model loading; subsequent requests are faster)
