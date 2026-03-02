# app/ml/classifier.py
# Loads the Kaggle-trained TF-IDF + LogisticRegression artifacts and exposes
# a classify() function used by triage_service.

import os
import time

import joblib

from app.services.preprocessing import clean_text

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

_vectorizer = None
_classifier = None
_label_encoder = None


def _load() -> None:
    global _vectorizer, _classifier, _label_encoder
    if _vectorizer is None:
        _vectorizer = joblib.load(os.path.join(_MODEL_DIR, "vectorizer.pkl"))
        _classifier = joblib.load(os.path.join(_MODEL_DIR, "classifier.pkl"))
        _label_encoder = joblib.load(os.path.join(_MODEL_DIR, "label_encoder.pkl"))


def classify(text: str) -> dict:
    """Return label and confidence for *text*.

    Returns:
        {
          "label": str,           # predicted Topic_group
          "confidence": float,    # probability of predicted class
          "timings_ms": float,    # inference wall-clock time
        }
    """
    _load()
    t0 = time.perf_counter()
    cleaned = clean_text(text)
    features = _vectorizer.transform([cleaned])
    idx = _classifier.predict(features)[0]
    proba = _classifier.predict_proba(features)[0][idx]
    label = _label_encoder.inverse_transform([idx])[0]
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    return {"label": label, "confidence": round(float(proba), 4), "timings_ms": elapsed}


def labels() -> list[str]:
    """Return all known class labels."""
    _load()
    return list(_label_encoder.classes_)
