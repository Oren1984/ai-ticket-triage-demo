import os
import joblib
from app.services.preprocessing import clean_text

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

_category_model = None
_urgency_model = None
_vectorizer = None


def _load_models():
    global _category_model, _urgency_model, _vectorizer
    if _vectorizer is None:
        _vectorizer = joblib.load(os.path.join(_MODEL_DIR, "vectorizer.pkl"))
        _category_model = joblib.load(os.path.join(_MODEL_DIR, "category_model.pkl"))
        _urgency_model = joblib.load(os.path.join(_MODEL_DIR, "urgency_model.pkl"))


def predict(ticket_text: str) -> dict:
    """Return predicted category and urgency for a ticket."""
    _load_models()
    cleaned = clean_text(ticket_text)
    features = _vectorizer.transform([cleaned])
    category = _category_model.predict(features)[0]
    urgency = _urgency_model.predict(features)[0]
    return {"category": category, "urgency": urgency}
