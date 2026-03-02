# tests/test_new_api.py
# Phase E: Tests for the new Kaggle-trained classifier and new endpoints.
# Covers: artifact loading, /classify debug endpoint, /triage main endpoint.

import os
import pytest
from fastapi.testclient import TestClient

ARTIFACTS_EXIST = all(
    os.path.exists(os.path.join(os.path.dirname(__file__), "..", "models", f))
    for f in ("vectorizer.pkl", "classifier.pkl", "label_encoder.pkl")
)


# ---------------------------------------------------------------------------
# Artifact loading
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not ARTIFACTS_EXIST, reason="New artifacts not trained yet")
def test_artifacts_load():
    from app.ml.classifier import classify, labels
    known = labels()
    assert isinstance(known, list)
    assert len(known) > 0


# ---------------------------------------------------------------------------
# /classify  debug endpoint
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not ARTIFACTS_EXIST, reason="New artifacts not trained yet")
def test_classify_endpoint():
    from app.main import app
    client = TestClient(app)

    response = client.post("/classify", json={"ticket_text": "Cannot login to my computer"})
    assert response.status_code == 200

    data = response.json()
    assert "label" in data
    assert "confidence" in data
    assert "timings_ms" in data
    assert isinstance(data["label"], str)
    assert 0.0 <= data["confidence"] <= 1.0
    assert data["timings_ms"] >= 0


# ---------------------------------------------------------------------------
# /triage  main endpoint
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not ARTIFACTS_EXIST, reason="New artifacts not trained yet")
def test_triage_returns_expected_keys():
    from app.main import app
    client = TestClient(app)

    response = client.post("/triage", json={"ticket_text": "My keyboard is broken"})
    assert response.status_code == 200

    data = response.json()
    # Required keys (schema-stable)
    for key in ("request_id", "category", "urgency", "retrieved_docs", "final_response", "latency_ms"):
        assert key in data, f"Missing key: {key}"

    assert isinstance(data["request_id"], str) and len(data["request_id"]) > 0
    assert isinstance(data["category"], str) and len(data["category"]) > 0
    assert isinstance(data["urgency"], str)
    assert isinstance(data["retrieved_docs"], list)
    assert isinstance(data["latency_ms"], float)


@pytest.mark.skipif(not ARTIFACTS_EXIST, reason="New artifacts not trained yet")
def test_triage_label_is_known_class():
    from app.main import app
    from app.ml.classifier import labels as known_labels
    client = TestClient(app)

    response = client.post("/triage", json={"ticket_text": "Need access to the shared drive"})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] in known_labels()


@pytest.mark.skipif(not ARTIFACTS_EXIST, reason="New artifacts not trained yet")
def test_health_endpoint():
    from app.main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
