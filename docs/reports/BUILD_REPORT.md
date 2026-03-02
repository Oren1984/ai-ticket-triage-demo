# 🐳 Build Report – AI Ticket Triage + RAG Assistant (Kaggle Hybrid Version)

## 📦 What Happens During `docker compose build`?

During the build phase, the container executes a full reproducible ML pipeline:

### 1️⃣ Install Dependencies
- All packages from `requirements.txt`
- Includes: FastAPI, scikit-learn, nltk, chromadb, pytest

### 2️⃣ Data Split (Real Dataset)
Script: `scripts/split_data.py`

- Source: Kaggle IT Support dataset (47,837 samples)
- Stratified split:
  - 80% Train
  - 10% Validation
  - 10% Test
- No data leakage

### 3️⃣ Train-only EDA Augmentation
Script: `scripts/augment_data.py`

- Applied ONLY on train split
- WordNet synonym replacement
- Random swap
- Random deletion
- Final hybrid train size: 65,375 samples
- Val/Test remain 100% real data

### 4️⃣ Model Training
Script: `scripts/train_kaggle_model.py`

- TF-IDF (20k features, bigrams)
- Logistic Regression
- class_weight="balanced"
- Validation Accuracy: 0.86
- Test Accuracy: 0.86
- Macro F1: 0.86

Artifacts created:
- models/vectorizer.pkl
- models/classifier.pkl
- models/label_encoder.pkl

### 5️⃣ RAG Ingestion
Script: `scripts/ingest_knowledge.py`

- Markdown runbooks loaded
- Chunked into segments
- Embedded into ChromaDB
- Vector store ready at container startup

---

## ⏱ Build Time

- First build (cold): ~120–150 seconds
- Subsequent builds (cached layers): ~5–10 seconds

---

## 🚀 What Happens During `docker compose up`?

1. Container starts
2. FastAPI loads
3. Model artifacts are loaded into memory
4. Chroma vector store initialized
5. Server listens on port 8000

⏱ Startup time: < 1 second  
No retraining or ingestion required at runtime.

---

## 🎯 Why Train During Build?

✔ Deterministic reproducible container  
✔ Fail-fast if model training breaks  
✔ No demo latency  
✔ Fully self-contained artifact  
✔ No runtime surprises  

---

## ⚠️ Possible Failure Scenarios

- Missing dependency → build fails
- Dataset missing → training fails
- knowledge_base empty → RAG returns no results
- Port 8000 occupied → container fails to start

All failures are detected early.

---

## ✅ Pre-Demo Validation Checklist

- `docker compose up --build` completes successfully
- `GET /health` returns {"status":"ok"}
- `POST /triage` returns valid JSON
- Swagger UI accessible
- Test suite passes (19 tests)

---

## 🏁 Status

✔ Reproducible ML pipeline  
✔ Real dataset integration  
✔ Train-only EDA balancing  
✔ Backend modularized  
✔ Demo-ready containerized system