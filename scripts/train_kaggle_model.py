"""Phase C: Train TF-IDF + LogisticRegression on train_hybrid.csv.

Evaluates ONLY on real val.csv / test.csv.
Saves artifacts to models/ and reports to reports/.
"""

import os
import sys

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.services.preprocessing import clean_text

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


def load_split(name: str) -> tuple[list[str], list[str]]:
    path = os.path.join(PROCESSED_DIR, f"{name}.csv")
    df = pd.read_csv(path)
    texts = df["Document"].fillna("").apply(clean_text).tolist()
    labels = df["Topic_group"].tolist()
    return texts, labels


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # ---- Load data ----
    train_texts, train_labels = load_split("train_hybrid")
    val_texts, val_labels = load_split("val")
    test_texts, test_labels = load_split("test")

    print(f"Train (hybrid) : {len(train_texts)}")
    print(f"Val  (real)    : {len(val_texts)}")
    print(f"Test (real)    : {len(test_texts)}")

    # ---- Label encoder ----
    le = LabelEncoder()
    le.fit(train_labels + val_labels + test_labels)  # all known classes

    y_train = le.transform(train_labels)
    y_val   = le.transform(val_labels)
    y_test  = le.transform(test_labels)

    # ---- TF-IDF ----
    vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), sublinear_tf=True)
    X_train = vectorizer.fit_transform(train_texts)
    X_val   = vectorizer.transform(val_texts)
    X_test  = vectorizer.transform(test_texts)

    # ---- Logistic Regression ----
    clf = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42,
        C=1.0,
        solver="lbfgs",
    )
    clf.fit(X_train, y_train)

    # ---- Evaluate on val ----
    y_val_pred = clf.predict(X_val)
    val_report = classification_report(
        val_labels,
        le.inverse_transform(y_val_pred),
        zero_division=0,
    )
    print("\n=== Val Classification Report ===")
    print(val_report)
    with open(os.path.join(REPORTS_DIR, "classification_report_val.txt"), "w") as f:
        f.write("=== Val Classification Report ===\n")
        f.write(val_report)

    # ---- Evaluate on test ----
    y_test_pred = clf.predict(X_test)
    test_report = classification_report(
        test_labels,
        le.inverse_transform(y_test_pred),
        zero_division=0,
    )
    print("\n=== Test Classification Report ===")
    print(test_report)
    with open(os.path.join(REPORTS_DIR, "classification_report_test.txt"), "w") as f:
        f.write("=== Test Classification Report ===\n")
        f.write(test_report)

    # ---- Confusion matrix (test) ----
    cm = confusion_matrix(y_test, y_test_pred)
    cm_df = pd.DataFrame(cm, index=le.classes_, columns=le.classes_)
    cm_df.to_csv(os.path.join(REPORTS_DIR, "confusion_matrix_test.csv"))
    print("\nConfusion matrix saved.")

    # ---- Save artifacts ----
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))
    joblib.dump(clf,        os.path.join(MODEL_DIR, "classifier.pkl"))
    joblib.dump(le,         os.path.join(MODEL_DIR, "label_encoder.pkl"))
    print(f"Artifacts saved to {MODEL_DIR}/")


if __name__ == "__main__":
    main()
