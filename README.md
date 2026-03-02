### 🎫 AI Ticket Triage Demo

AI-powered IT ticket classification and runbook recommendation system.

Built with FastAPI, scikit-learn (TF-IDF + Logistic Regression), and ChromaDB.


### 📌 Overview

This project demonstrates a complete end-to-end AI ticket triage pipeline:

🎯 Ticket text classification (Kaggle real dataset)

⚖️ Train-only EDA balancing (no data leakage)

🔎 Vector-based runbook retrieval (RAG-style)

🧩 Template-based response generation

🚀 REST API with Swagger documentation

💻 Lightweight demo web UI

🐳 Fully containerized with Docker

⚠️ The system is fully self-contained and does not require any external LLM API key.


### 🧠 ML Strategy
📂 Dataset

Source: Kaggle IT Support Tickets

Total samples: 47,837 real tickets

Split: 80 / 10 / 10 (train / val / test) — stratified

EDA applied only to training set (no data leakage)

Final hybrid training size: 65,375 samples


### 🏗 Model Architecture
Ticket Text
    ↓
Preprocessing
    ↓
TF-IDF Vectorization
    ↓
Logistic Regression (Category Prediction)
    ↓
ChromaDB Retrieval (Top-K Runbooks)
    ↓
Template-based Response Generation
    ↓
JSON API Response
Model Details

TfidfVectorizer

LogisticRegression

class_weight="balanced"


### 📊 Model Performance (Real Test Set)
Metric	Score
Accuracy	0.86
Macro F1	0.86

✔ Validation ≈ Test → No overfitting
✔ Real test set evaluation

ℹ️ Urgency field currently returns "Medium" as placeholder (extendable with labeled urgency data).

### ⚡ Quick Start
1️⃣ Setup Environment
copy .env.example .env        # Windows
# cp .env.example .env        # Linux / macOS

2️⃣ Build & Run
docker compose up --build
🌐 Access the Application
URL	Purpose
http://localhost:8000
	Demo UI
http://localhost:8000/docs
	Swagger API
http://localhost:8000/health
	Health Check
🧰 Tech Stack

⚡ FastAPI

🧠 scikit-learn

📚 ChromaDB

🐳 Docker

🧪 Pytest

📦 NLTK (WordNet for EDA)


### 📂 Project Structure
app/               → FastAPI application (modular backend)
scripts/           → Data split, augmentation, training, ingestion
knowledge_base/    → Markdown runbooks
models/            → Serialized ML artifacts
vector_store/      → ChromaDB persistence
tests/             → Unit & integration tests
docs/              → Design & architecture documentation
🔌 API Endpoints
Method	Endpoint	Description
POST	/triage	Main orchestration endpoint
POST	/classify	ML-only debug endpoint
POST	/predict	Legacy compatibility endpoint
GET	/health	Service health check


### 🧪 Testing & Validation

✅ 19 tests passing (3 conditional skips)

✅ Docker build successful

✅ Endpoints verified

✅ UI validated

✅ Model artifacts load correctly

Run tests locally:

pytest

### 🚀 Status

✔ Kaggle real dataset integrated

✔ Train-only EDA implemented

✔ Backend refactored to modular architecture

✔ Dockerized reproducible pipeline

✔ Demo-ready


### 📎 Notes

No external LLM required (mock LLM used for demo purposes)

Legacy synthetic-only models moved to models/archive/

Designed for educational demonstration of applied ML + backend integration