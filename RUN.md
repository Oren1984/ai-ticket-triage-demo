# How to Run

## Prerequisites

- Python 3.11+
- Docker (optional, for containerized run)

## Local Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate dataset

```bash
python scripts/generate_dataset.py
```

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
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"ticket_text\": \"Cannot connect to production database\"}"
```

### 7. Run tests

```bash
python -m pytest tests/ -v
```

## Docker

### Build and run with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

The API will be available at http://localhost:8000

### Test the containerized API

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"ticket_text\": \"VPN connection dropping intermittently\"}"
```

## API Endpoints

- `POST /predict` - Classify a ticket and get recommendations
- `GET /health` - Health check
