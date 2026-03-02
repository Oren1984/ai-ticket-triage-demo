# AI Ticket Triage + RAG Assistant

Owner: Oren  
Type: End-to-End Applied AI Demo  
Scope: Lean MVP (Real Dataset + No External LLM)

---

## 1. Goal

Build a lightweight but realistic AI system that processes IT / DevOps service tickets end-to-end.

The system performs:

1. Category classification (8 real Kaggle classes)
2. Urgency placeholder ("Medium", extendable)
3. Retrieval of relevant runbook knowledge (RAG)
4. Structured template-based response generation

This is an applied ML engineering demo — not a research system.

---

## 2. MVP Definition

The MVP includes:

- Kaggle IT Support dataset (47,837 records)
- Stratified 80/10/10 split
- Train-only EDA augmentation
- TF-IDF + Logistic Regression baseline
- RAG over Markdown runbooks
- FastAPI backend
- Structured logging
- Unit + Integration tests
- Docker Compose packaging

---

## 3. Explicit Non-Goals

- No fine-tuning LLMs
- No GPU usage
- No Kubernetes
- No microservices
- No production cloud infra
- No external LLM API dependency

Keep it lean, deterministic, and reproducible.

---

## 4. Success Criteria

- Macro F1 ≥ 0.80 (real test set)
- Avg latency < 1 second
- 0 crashes in E2E flow
- All components start with one docker compose up

---

## 5. High Level Architecture

User → FastAPI → ML Classifier → RAG Retriever → Template Response