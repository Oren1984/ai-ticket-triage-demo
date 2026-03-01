# AI Ticket Triage + RAG Assistant
Owner: Oren
Type: End-to-End Applied AI Demo
Scope: Lean MVP (No GPU, No Over-Engineering)

---

## 1. Goal

Build a lightweight but realistic AI system that processes IT / DevOps service tickets end-to-end.

The system must:

1. Classify ticket category
2. Predict urgency level
3. Retrieve relevant runbook knowledge (RAG)
4. Generate a concise response using LLM API

This is a demo product — not a research project.

---

## 2. MVP Definition

The MVP must include:

- Dataset: 800–1500 records
- One working ML baseline model
- RAG over 20–30 documents
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
- No production-grade cloud infra

Keep it lean and working.

---

## 4. Success Criteria

- F1 Score ≥ 0.75 (or reasonable baseline)
- Avg latency < 5 seconds end-to-end
- 0 crashes in E2E flow
- All components start with one docker compose up

---

## 5. High Level Architecture

User → FastAPI → ML Classifier → RAG Retriever → LLM → Response