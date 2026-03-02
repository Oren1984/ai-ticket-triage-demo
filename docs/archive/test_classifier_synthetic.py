# tests/test_classifier.py
# This test file contains unit tests for the classifier service in the FastAPI application.
# It uses pytest to define test cases that check the output of the predict function, 
# ensuring that it returns the expected keys and valid category and urgency values.
# The tests are skipped if the models have

import os
import pytest
from app.services.classifier import predict

MODELS_EXIST = os.path.exists(
    os.path.join(os.path.dirname(__file__), "..", "models", "vectorizer.pkl")
)

# The following tests will be skipped if the models have not been trained yet
@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_returns_required_keys():
    result = predict("Cannot connect to VPN from remote office")
    assert "category" in result
    assert "urgency" in result

# The following tests check that the predicted category and urgency are valid values based on the training data.
@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_category_is_valid():
    valid_categories = [
        "Network Issue", "Access / Permissions", "Deployment Failure",
        "Monitoring / Alert", "Database Issue", "Infrastructure Issue",
    ]
    result = predict("Database replica is lagging behind primary")
    assert result["category"] in valid_categories

# The following test checks that the predicted urgency is one of the expected values: Low, Medium, or High.
@pytest.mark.skipif(not MODELS_EXIST, reason="Models not trained yet")
def test_predict_urgency_is_valid():
    result = predict("Production server is down")
    assert result["urgency"] in ["Low", "Medium", "High"]
