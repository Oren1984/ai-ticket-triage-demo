# app/services/classifier.py
# Thin wrapper kept for backward compatibility with /predict endpoint.
# Uses the Kaggle-trained artifacts (vectorizer.pkl + classifier.pkl + label_encoder.pkl).
# Returns {"category": <Topic_group>, "urgency": "Medium"} to preserve existing schema.

import os
import joblib
from app.services.preprocessing import clean_text

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

_classifier = None
_vectorizer = None
_label_encoder = None


def _load_models():
    global _classifier, _vectorizer, _label_encoder
    if _vectorizer is None:
        _vectorizer = joblib.load(os.path.join(_MODEL_DIR, "vectorizer.pkl"))
        _classifier = joblib.load(os.path.join(_MODEL_DIR, "classifier.pkl"))
        _label_encoder = joblib.load(os.path.join(_MODEL_DIR, "label_encoder.pkl"))


def predict(ticket_text: str) -> dict:
    """Return predicted category and urgency for a ticket.

    'category' is the Kaggle Topic_group label.
    'urgency'  is always 'Medium' (dataset has no urgency signal).
    """
    _load_models()
    cleaned = clean_text(ticket_text)
    features = _vectorizer.transform([cleaned])
    idx = _classifier.predict(features)[0]
    category = _label_encoder.inverse_transform([idx])[0]
    return {"category": category, "urgency": "Medium"}
