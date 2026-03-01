# tests/test_integration.py
# This test file contains integration tests for the FastAPI application.
# It uses pytest and FastAPI's TestClient to test the /predict endpoint and the /health endpoint.
# The tests check that the /predict endpoint returns the expected keys and valid values,

import os
import pytest
from fastapi.testclient import TestClient

MODELS_EXIST = os.path.exists(
    os.path.join(os.path.dirname(__file__), "..", "models", "vectorizer.pkl")
)


@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_endpoint():
    from app.main import app
    client = TestClient(app)

    response = client.post("/predict", json={
        "ticket_text": "Cannot SSH into production server, connection times out"
    })

    assert response.status_code == 200
    data = response.json()

    # Verify all required fields
    assert "request_id" in data
    assert "category" in data
    assert "urgency" in data
    assert "retrieved_docs" in data
    assert "final_response" in data
    assert "latency_ms" in data

    # Types
    assert isinstance(data["request_id"], str)
    assert isinstance(data["latency_ms"], float)
    assert isinstance(data["retrieved_docs"], list)
    assert len(data["request_id"]) > 0


@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_health_endpoint():
    from app.main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
