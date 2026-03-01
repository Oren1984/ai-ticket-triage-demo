# How to Run

## Prerequisites

- Python 3.11+
- Docker (optional, for containerized run)

---

## Option A — Local (Python)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate dataset *(skip if `data/tickets.json` already exists)*

```bash
python scripts/generate_dataset.py
```

> `data/tickets.json` is committed to the repo — this step is only needed if you delete it.

### 3. Train ML models

```bash
python scripts/train_model.py
```

### 4. Ingest knowledge base into vector store

```bash
python scripts/ingest_knowledge.py
```

### 5. Run the API server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 6. Test the API

```bash
# Linux / macOS / Git Bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"ticket_text": "Cannot connect to production database"}'

# Windows PowerShell
Invoke-RestMethod -Uri http://localhost:8000/predict -Method POST `
  -ContentType "application/json" `
  -Body '{"ticket_text": "Cannot connect to production database"}' | ConvertTo-Json
```

### 7. Run tests

```bash
python -m pytest tests/ -v
```

---

## Option B — Docker *(recommended for clean demo)*

> Steps 2–4 above run automatically inside the container during `docker compose build`.

### 1. Copy the example env file

```bash
# Linux / macOS
cp .env.example .env

# Windows
copy .env.example .env
```

### 2. Build and start

```bash
docker compose up --build
```

The API will be available at http://localhost:8000

### 3. Smoke test the containerized API

```bash
# Linux / macOS / Git Bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"ticket_text": "VPN connection dropping intermittently"}'

# Windows PowerShell
Invoke-RestMethod -Uri http://localhost:8000/predict -Method POST `
  -ContentType "application/json" `
  -Body '{"ticket_text": "VPN connection dropping intermittently"}' | ConvertTo-Json
```

### 4. Stop the container

```bash
docker compose down
```

---

## API Endpoints

| Method | Endpoint   | Description                               |
|--------|------------|-------------------------------------------|
| GET    | `/`        | Web UI — paste a ticket and see results   |
| POST   | `/predict` | Classify a ticket and get recommendations |
| GET    | `/health`  | Health check — returns `{"status": "ok"}` |
| GET    | `/docs`    | Interactive Swagger UI                    |
