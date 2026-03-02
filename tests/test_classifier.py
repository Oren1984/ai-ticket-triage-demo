# tests/test_classifier.py
# Unit tests for the classifier service (app/services/classifier.predict).
# Validates that the Kaggle-trained model loads and returns the expected schema.
#
# NOTE: The synthetic-dataset version of this file (which hardcoded IT-ops category
# names like "Network Issue", "Deployment Failure", etc.) has been archived to
# docs/archive/test_classifier_synthetic.py because the model is now trained on
# the Kaggle dataset (Topic_group labels: Hardware, Access, HR Support, …).

import os
import pytest
from app.ml.classifier import labels as known_labels
from app.services.classifier import predict

MODELS_EXIST = all(
    os.path.exists(os.path.join(os.path.dirname(__file__), "..", "models", f))
    for f in ("vectorizer.pkl", "classifier.pkl", "label_encoder.pkl")
)


@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_returns_required_keys():
    result = predict("Cannot connect to VPN from remote office")
    assert "category" in result
    assert "urgency" in result


@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_category_is_valid():
    """Category must be one of the Kaggle Topic_group labels."""
    result = predict("Database replica is lagging behind primary")
    assert result["category"] in known_labels()


@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_urgency_is_valid():
    result = predict("Production server is down")
    assert result["urgency"] in ["Low", "Medium", "High"]
