# Goal
Refactor backend architecture + train real ML classifier on Kaggle data + add controlled hybrid augmentation (EDA, train only).
Keep API behavior stable.

## Input dataset
- data/raw/all_tickets_processed_improved_v3.csv
  Columns: Document (text), Topic_group (label)

## Strict rules
- DO NOT use external LLM APIs for data augmentation.
- DO NOT include synthetic samples in val/test.
- Keep existing /triage response schema stable (allowed: add timings_ms).
- DO NOT delete existing docs or tests; if something is obsolete move to docs/archive/.
- Keep existing folders (knowledge_base, vector_store, models) unless explicitly reorganized; prefer minimal changes.
- Ensure backward compatibility: /triage endpoint and response keys must remain (allowed: add optional fields).
- Use only the Kaggle CSV at data/raw/all_tickets_processed_improved_v3.csv as the real source of truth.

## Phase A: Data split (real-only)
1) Read data/raw/all_tickets_processed_improved_v3.csv
2) Create stratified splits:
   - data/processed/train.csv (80%)
   - data/processed/val.csv (10%)
   - data/processed/test.csv (10%)
3) Save stats to reports/data_stats.txt (counts per class for each split)

## Phase B: EDA augmentation (train only)
1) Identify minority classes from train.csv
2) Implement EDA without external LLM:
   - synonym replacement (WordNet-based)
   - random swap
   - random deletion
3) Generate synthetic samples ONLY for minority classes to reach a target ratio (e.g., up to ~70% of the majority class size)
4) Save:
   - data/processed/train_synth.csv
   - data/processed/train_hybrid.csv (train + synth)

## Phase C: Train model + artifacts
1) Train TF-IDF + LogisticRegression (class_weight="balanced")
2) Evaluate on val/test (real-only)
3) Save artifacts to models/:
   - vectorizer.pkl
   - classifier.pkl
   - label_encoder.pkl
4) Save reports to reports/:
   - classification_report_val.txt
   - classification_report_test.txt
   - confusion_matrix_test.csv

## Phase D: Backend refactor (as backend notes)
1) Keep FastAPI thin: app/api/routes.py + app/api/schemas.py
2) Create app/services/triage_service.py orchestrator
3) Create app/ml/classifier.py that loads artifacts and predicts
4) Endpoints:
   - POST /triage (main)
   - POST /classify (debug)
   - GET /health

## Phase E: Tests + Docker
1) Add pytest tests:
   - artifacts load
   - /classify works
   - /triage returns expected keys
2) Ensure docker compose build works

## Final
- Run tests
- Run docker build
- Provide "What changed" + "Remaining manual steps" summary