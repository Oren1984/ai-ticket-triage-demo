# 🚀 Project Summary – AI Ticket Triage + RAG Assistant (Kaggle Hybrid Demo)

## 🎯 Project Goal

Build a complete end-to-end AI system that receives IT / DevOps support tickets and performs:

1. Category classification (8 real-world classes)
2. Placeholder urgency level
3. Relevant runbook retrieval (RAG)
4. Structured response generation

The system is designed as an applied ML engineering demonstration.

---

## 📊 Dataset

- Source: Kaggle IT Support Tickets
- Total samples: 47,837
- 8 real-world categories
- Stratified 80/10/10 split
- No leakage between train/val/test

### Hybrid Strategy

- Train set augmented using EDA techniques
- Validation and test sets remain 100% real
- Final training size: 65,375 samples
- Imbalance ratio improved from 0.129 → 0.700

---

## 🤖 ML Model

- TF-IDF Vectorizer (20k features, bigrams)
- Logistic Regression
- class_weight="balanced"

### 📈 Performance (Real Test Set)

- Accuracy: 0.86
- Macro F1: 0.86
- No overfitting (val ≈ test)

> Urgency currently returns `"Medium"` (placeholder).
> Extendable with labeled urgency data.

---

## 📚 RAG Component

- Markdown runbooks
- Chroma Vector Store
- Top-K retrieval
- Template-based response generation
- No external LLM dependency

---

## 🌐 Backend Architecture

- FastAPI
- Modular structure:
  - `app/ml/` – ML wrapper
  - `app/services/` – orchestration
  - `app/rag/` – retrieval layer
- Main endpoint: `POST /triage`
- Debug endpoint: `POST /classify`
- Health endpoint: `GET /health`
- Swagger auto-generated

---

## 🧪 Testing & Validation

- 19 automated tests (unit + integration)
- Docker build validated
- Endpoints verified
- Model artifacts load correctly
- Full pipeline tested: classify → retrieve → respond

---

## 🐳 Dockerization

- Full ML training during build
- RAG ingestion during build
- Deterministic reproducible container
- Single command deployment:
  docker compose up --build

---

## ⚙️ What This Demonstrates

✔ Applied ML engineering  
✔ Real-world dataset integration  
✔ Data balancing without leakage  
✔ Backend modularization  
✔ ML + RAG hybrid architecture  
✔ Test-driven validation  
✔ Containerized reproducibility  

---

## ⚠️ Known Limitations

- No real urgency model (placeholder)
- No external LLM
- Not production-scaled
- CPU-only inference

---

## 🚀 Current Status

✔ Fully working end-to-end  
✔ Real dataset validated  
✔ Dockerized  
✔ Demo-ready  
✔ Architecture extendable  

---

## 💡 Future Extensions

- Add real urgency dataset
- Integrate external LLM
- Use semantic embeddings
- Add monitoring & logging dashboard
- Deploy to cloud

---

**Author:** Oren  
**Purpose:** Applied AI / ML Engineering demonstration project