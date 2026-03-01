import os
import pytest
from app.services.classifier import predict

MODELS_EXIST = os.path.exists(
    os.path.join(os.path.dirname(__file__), "..", "models", "vectorizer.pkl")
)


@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_returns_required_keys():
    result = predict("Cannot connect to VPN from remote office")
    assert "category" in result
    assert "urgency" in result


@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_category_is_valid():
    valid_categories = [
        "Network Issue", "Access / Permissions", "Deployment Failure",
        "Monitoring / Alert", "Database Issue", "Infrastructure Issue",
    ]
    result = predict("Database replica is lagging behind primary")
    assert result["category"] in valid_categories


@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_urgency_is_valid():
    result = predict("Production server is down")
    assert result["urgency"] in ["Low", "Medium", "High"]
