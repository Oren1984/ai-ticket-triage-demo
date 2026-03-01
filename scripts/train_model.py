"""Train TF-IDF + Logistic Regression models for category and urgency prediction."""

import json
import os
import sys

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.services.preprocessing import clean_text

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.json")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Load data
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        tickets = json.load(f)

    print(f"Loaded {len(tickets)} tickets")

    texts = [clean_text(t["ticket_text"]) for t in tickets]
    categories = [t["category"] for t in tickets]
    urgencies = [t["urgency"] for t in tickets]

    # TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)

    # Split
    X_train, X_test, cat_train, cat_test, urg_train, urg_test = train_test_split(
        X, categories, urgencies, test_size=0.2, random_state=42
    )

    # Train category model
    cat_model = LogisticRegression(max_iter=1000, random_state=42)
    cat_model.fit(X_train, cat_train)
    cat_pred = cat_model.predict(X_test)
    print("\n=== Category Classification ===")
    print(f"Accuracy: {accuracy_score(cat_test, cat_pred):.4f}")
    print(classification_report(cat_test, cat_pred))

    # Train urgency model
    urg_model = LogisticRegression(max_iter=1000, random_state=42)
    urg_model.fit(X_train, urg_train)
    urg_pred = urg_model.predict(X_test)
    print("\n=== Urgency Classification ===")
    print(f"Accuracy: {accuracy_score(urg_test, urg_pred):.4f}")
    print(classification_report(urg_test, urg_pred))

    # Save
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))
    joblib.dump(cat_model, os.path.join(MODEL_DIR, "category_model.pkl"))
    joblib.dump(urg_model, os.path.join(MODEL_DIR, "urgency_model.pkl"))
    print(f"\nModels saved to {MODEL_DIR}/")


if __name__ == "__main__":
    main()
