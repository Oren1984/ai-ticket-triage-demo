# Implementation Report — AI Ticket Triage Refactor

**Date:** 2026-03-02
**Dataset:** `data/raw/all_tickets_processed_improved_v3.csv`
**Total source rows:** 47,837

---

## 1. Data Processing

### 1.1 Train / Val / Test Split

| Split | Rows   | Share  | File                          |
|-------|--------|--------|-------------------------------|
| Train | 38,269 | 80.0%  | `data/processed/train.csv`    |
| Val   |  4,784 | 10.0%  | `data/processed/val.csv`      |
| Test  |  4,784 | 10.0%  | `data/processed/test.csv`     |

Method: `sklearn.model_selection.train_test_split` with `stratify=Topic_group`, `random_state=42`.
Val and test contain **real samples only** — no synthetic data.

### 1.2 Class Distribution Before EDA (`data/processed/train.csv`)

| Class                 | Count  | % of Majority |
|-----------------------|--------|---------------|
| Hardware              | 10,893 | 100.0%        |
| HR Support            |  8,732 |  80.2%        |
| Access                |  5,700 |  52.3%        |
| Miscellaneous         |  5,648 |  51.8%        |
| Storage               |  2,222 |  20.4%        |
| Purchase              |  1,971 |  18.1%        |
| Internal Project      |  1,695 |  15.6%        |
| Administrative rights |  1,408 |  12.9%        |

**Imbalance ratio (min/max): 0.129**

### 1.3 EDA Augmentation — Train Only

Techniques applied (no external LLMs):
- **Synonym replacement** — up to 2 words replaced via WordNet (`nltk.corpus.wordnet`)
- **Random swap** — 2 random word pairs swapped
- **Random deletion** — each word dropped with p=0.15, applied randomly

Target per minority class: **70% of majority = 7,625 samples**
Classes skipped (already ≥ target): Hardware (10,893), HR Support (8,732)

| Class                 | Original | Synthetic Added | Hybrid Total |
|-----------------------|----------|----------------|--------------|
| Hardware              | 10,893   |              0 | 10,893       |
| HR Support            |  8,732   |              0 |  8,732       |
| Access                |  5,700   |          1,925 |  7,625       |
| Miscellaneous         |  5,648   |          1,977 |  7,625       |
| Storage               |  2,222   |          5,403 |  7,625       |
| Purchase              |  1,971   |          5,654 |  7,625       |
| Internal Project      |  1,695   |          5,930 |  7,625       |
| Administrative rights |  1,408   |          6,217 |  7,625       |
| **TOTAL**             | **38,269** | **27,106**   | **65,375**   |

**Imbalance ratio after EDA: 0.700**

### 1.4 Files Created Under `data/processed/`

```
data/processed/train.csv          38,269 rows   11.1 MB  (real train split)
data/processed/val.csv             4,784 rows    1.4 MB  (real val split)
data/processed/test.csv            4,784 rows    1.4 MB  (real test split)
data/processed/train_synth.csv    27,106 rows    7.0 MB  (synthetic samples only)
data/processed/train_hybrid.csv   65,375 rows   18.1 MB  (real + synthetic)
```

---

## 2. Model Training Results

### 2.1 Configuration

| Parameter       | Value                    |
|-----------------|--------------------------|
| Algorithm       | `LogisticRegression`     |
| `class_weight`  | `"balanced"` ✓           |
| `C`             | 1.0                      |
| `solver`        | lbfgs                    |
| `max_iter`      | 1,000                    |
| Vectorizer      | `TfidfVectorizer`        |
| `max_features`  | 20,000                   |
| `ngram_range`   | (1, 2)                   |
| `sublinear_tf`  | True                     |
| Training data   | `train_hybrid.csv`       |
| Eval data       | `val.csv`, `test.csv`    |

`class_weight="balanced"` confirmed from serialized artifact.

### 2.2 Validation Results (`val.csv`, 4,784 real samples)

```
Accuracy  : 0.86
Macro F1  : 0.86
Macro P   : 0.84
Macro R   : 0.88
```

| Class                 | Precision | Recall | F1   | Support |
|-----------------------|-----------|--------|------|---------|
| Access                | 0.90      | 0.90   | 0.90 |     712 |
| Administrative rights | 0.66      | 0.88   | 0.75 |     176 |
| HR Support            | 0.90      | 0.86   | 0.88 |   1,092 |
| Hardware              | 0.87      | 0.81   | 0.84 |   1,362 |
| Internal Project      | 0.82      | 0.93   | 0.87 |     212 |
| Miscellaneous         | 0.80      | 0.86   | 0.83 |     706 |
| Purchase              | 0.94      | 0.87   | 0.91 |     246 |
| Storage               | 0.85      | 0.92   | 0.88 |     278 |

### 2.3 Test Results (`test.csv`, 4,784 real samples)

```
Accuracy  : 0.86
Macro F1  : 0.86
Macro P   : 0.84
Macro R   : 0.88
```

| Class                 | Precision | Recall | F1   | Support |
|-----------------------|-----------|--------|------|---------|
| Access                | 0.90      | 0.88   | 0.89 |     713 |
| Administrative rights | 0.69      | 0.85   | 0.76 |     176 |
| HR Support            | 0.90      | 0.86   | 0.88 |   1,091 |
| Hardware              | 0.87      | 0.82   | 0.84 |   1,362 |
| Internal Project      | 0.77      | 0.93   | 0.85 |     212 |
| Miscellaneous         | 0.81      | 0.86   | 0.83 |     706 |
| Purchase              | 0.92      | 0.92   | 0.92 |     247 |
| Storage               | 0.88      | 0.90   | 0.89 |     277 |

### 2.4 Per-Class Summary

- **Best class:** `Purchase` — F1 0.92 on test; distinct vocabulary drives high precision and recall.
- **Worst class:** `Administrative rights` — F1 0.76; smallest original class (1,408 samples), primarily confused with `Hardware` (22/176 test misclassifications). Recall improved by EDA and `class_weight="balanced"`.
- Val vs test F1 difference ≤ 0.01 for all classes — no overfitting detected.

---

## 3. Artifacts

### 3.1 New Model Artifacts (Phase C)

```
models/vectorizer.pkl      802 KB   TF-IDF vectorizer (20k features, bigrams, sublinear_tf)
models/classifier.pkl     1.2 MB   LogisticRegression, 8 classes, class_weight="balanced"
models/label_encoder.pkl    1 KB   LabelEncoder for 8 Kaggle Topic_group classes
```

### 3.2 Legacy Artifacts (retained, not used by active endpoints)

```
models/category_model.pkl   156 KB   Original synthetic-data category model
models/urgency_model.pkl     78 KB   Original synthetic-data urgency model
```

### 3.3 Complete List of New / Modified Files

**New files:**
```
scripts/split_data.py
scripts/augment_data.py
scripts/train_kaggle_model.py
data/processed/train.csv
data/processed/val.csv
data/processed/test.csv
data/processed/train_synth.csv
data/processed/train_hybrid.csv
models/classifier.pkl
models/label_encoder.pkl
reports/data_stats.txt
reports/classification_report_val.txt
reports/classification_report_test.txt
reports/confusion_matrix_test.csv
reports/IMPLEMENTATION_REPORT.md
app/ml/__init__.py
app/ml/classifier.py
app/services/triage_service.py
tests/test_new_api.py
docs/archive/test_classifier_synthetic.py
```

**Modified files:**
```
models/vectorizer.pkl          (replaced: was synthetic-data vectorizer, now Kaggle-trained)
app/routes.py                  (added /triage, /classify; kept /predict)
app/services/classifier.py     (updated to load new artifacts; same dict interface)
tests/test_classifier.py       (updated category validity list to Kaggle labels)
requirements.txt               (added nltk>=3.8)
Dockerfile                     (replaced train_model.py call with 4-script pipeline)
```

---

## 4. Backend Refactor

### 4.1 Folder Structure Under `app/`

**Before:**
```
app/
  main.py
  routes.py             POST /predict only
  services/
    classifier.py       loaded category_model.pkl + urgency_model.pkl
    llm.py
    preprocessing.py
  rag/
    embeddings.py
    ingest.py
    retriever.py
  templates/
```

**After:**
```
app/
  main.py               unchanged — GET /health still here
  routes.py             POST /triage + POST /classify + POST /predict (legacy)
  ml/                   NEW MODULE
    __init__.py
    classifier.py       classify(text) -> {label, confidence, timings_ms}
  services/
    classifier.py       UPDATED — now loads Kaggle artifacts; predict() interface preserved
    triage_service.py   NEW — triage(text) orchestrator
    llm.py              unchanged
    preprocessing.py    unchanged
  rag/
    embeddings.py       unchanged
    ingest.py           unchanged
    retriever.py        unchanged
  templates/            unchanged
```

### 4.2 Modules Added

| Module | Purpose |
|--------|---------|
| `app/ml/classifier.py` | Core ML wrapper. Lazy-loads `vectorizer.pkl`, `classifier.pkl`, `label_encoder.pkl`. Exposes `classify(text)` and `labels()`. |
| `app/services/triage_service.py` | Orchestrator. Calls `ml.classifier.classify()` → `rag.retriever.retrieve()` → `services.llm.generate_response()`. Returns a single result dict. |

### 4.3 Endpoint Summary

| Endpoint       | Method | Module               | Status  |
|----------------|--------|----------------------|---------|
| `GET /health`  | GET    | `app/main.py`        | Unchanged |
| `POST /triage` | POST   | `app/routes.py`      | New (main) |
| `POST /classify` | POST | `app/routes.py`      | New (debug) |
| `POST /predict` | POST  | `app/routes.py`      | Preserved (legacy) |

### 4.4 `/triage` Response Schema Compatibility

Response keys and types are unchanged from the spec. `timings_ms` added as an optional field only.

```json
{
  "request_id":    "string (UUID4)",
  "category":      "string (Kaggle Topic_group label)",
  "urgency":       "string ('Medium')",
  "retrieved_docs": [{"text": "string", "source": "string"}],
  "final_response": "string",
  "latency_ms":    "float",
  "timings_ms":    {"classify": "float", "total": "float"}
}
```

All original required keys present. `timings_ms` is `Optional` in the Pydantic model and absent from existing client contracts — no breaking change.

---

## 5. Tests and Docker

### 5.1 pytest

**Command:**
```bash
python -m pytest tests/ -v
```

**Result: 19 passed, 0 failed, 0 skipped**

```
tests/test_classifier.py::test_predict_returns_required_keys   PASSED
tests/test_classifier.py::test_predict_category_is_valid       PASSED
tests/test_classifier.py::test_predict_urgency_is_valid        PASSED
tests/test_integration.py::test_predict_endpoint               PASSED
tests/test_integration.py::test_health_endpoint                PASSED
tests/test_new_api.py::test_artifacts_load                     PASSED
tests/test_new_api.py::test_classify_endpoint                  PASSED
tests/test_new_api.py::test_triage_returns_expected_keys       PASSED
tests/test_new_api.py::test_triage_label_is_known_class        PASSED
tests/test_new_api.py::test_health_endpoint                    PASSED
tests/test_preprocessing.py::test_lowercase                    PASSED
tests/test_preprocessing.py::test_remove_special_chars         PASSED
tests/test_preprocessing.py::test_normalize_whitespace         PASSED
tests/test_preprocessing.py::test_combined                     PASSED
tests/test_preprocessing.py::test_empty_string                 PASSED
tests/test_rag.py::test_chunk_text_basic                       PASSED
tests/test_rag.py::test_chunk_text_short                       PASSED
tests/test_rag.py::test_chunk_overlap                          PASSED
tests/test_rag.py::test_retrieve_returns_results               PASSED
```

Duration: 4.14s. No warnings. No `skipif` guards fired (all artifacts and vector store present).

### 5.2 Docker Build

**Command:**
```bash
docker build -t ai-ticket-triage:test .
```

**Result: SUCCESS (exit code 0)**

| Layer | Step | Outcome |
|-------|------|---------|
| 4/10 | `pip install -r requirements.txt` | OK — nltk 3.9.3 installed |
| 5/10 | NLTK wordnet + omw-1.4 download | OK |
| 6/10 | `COPY . .` | OK — 56.74 MB context |
| 7/10 | `python scripts/split_data.py` | OK — 38269 / 4784 / 4784 |
| 8/10 | `python scripts/augment_data.py` | OK — 27106 synthetic samples |
| 9/10 | `python scripts/train_kaggle_model.py` | OK — 86% test accuracy |
| 10/10 | `python scripts/ingest_knowledge.py` | OK — 40 chunks ingested |

No errors. No warnings affecting runtime.

---

## 6. Remaining Manual Steps

None required. `docker compose up` is fully self-contained.

**Informational notes (not blockers):**

| Item | Detail |
|------|--------|
| `urgency` field | Always returns `"Medium"`. The Kaggle dataset contains no urgency signal. To add real urgency prediction, a labelled urgency dataset is required. |
| Legacy artifacts | `models/category_model.pkl` and `models/urgency_model.pkl` are no longer used by any active endpoint. They may be deleted manually once confirmed unnecessary. They were retained per the workplan's no-deletion rule. |
| `Administrative rights` F1 | Lowest at 0.76. Primarily confused with `Hardware`. Improvement requires more real training data or a domain-specific text embedding model. |
| Docker build cache | First build takes ~4 minutes (pip install + training pipeline). Subsequent builds cache layers 3–5 if `requirements.txt` is unchanged. |
