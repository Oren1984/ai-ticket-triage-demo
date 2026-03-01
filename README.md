## AI Ticket Triage Demo

AI-powered IT ticket classification and runbook recommendation system.

Built with FastAPI, scikit-learn (TF-IDF + Logistic Regression), and ChromaDB.


## 📌 Overview

This project demonstrates a complete end-to-end AI ticket triage pipeline:

🎯 Ticket text classification (Category + Urgency)

🔎 Vector-based runbook retrieval (RAG-style)

🧩 Template-based response generation

🚀 REST API with Swagger documentation

💻 Lightweight demo web UI

🐳 Fully containerized with Docker

⚠️ The system is fully self-contained and does not require any external LLM API key.


## ⚡ Quick Start
1️⃣ Setup Environment
copy .env.example .env        # Windows
# cp .env.example .env        # Linux / macOS

2️⃣ Build & Run
docker compose up --build


## 🌐 Open in Browser
URL	Purpose
http://localhost:8000
	Demo UI
http://localhost:8000/docs
	Swagger API
http://localhost:8000/health
	Health Check


## 🏗 Architecture
Ticket Text
    ↓
Preprocessing
    ↓
TF-IDF + Logistic Regression
    ↓
Category + Urgency Prediction
    ↓
ChromaDB Retrieval (Top-K Runbooks)
    ↓
Template-based Response Generation
    ↓
JSON API Response
🧰 Tech Stack

⚡ FastAPI

🧠 scikit-learn

📚 ChromaDB

🐳 Docker

🧪 Pytest


## 📂 Project Structure
app/             → FastAPI application
scripts/         → Training & ingestion scripts
knowledge_base/  → Markdown runbooks
models/          → Serialized ML artifacts
vector_store/    → ChromaDB data
tests/           → Unit & integration tests
docs/            → Design & architecture documentation


## ✅ Status

✔ End-to-end pipeline verified

✔ 14 / 14 tests passing

✔ Docker build successful

✔ Demo UI integrated