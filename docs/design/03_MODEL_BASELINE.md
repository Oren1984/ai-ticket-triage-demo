# ML Baseline Model

## 1. Objective

Predict:
- Category
- Urgency

## 2. Model Type

TF-IDF + Logistic Regression

## 3. Pipeline

Text → Clean → TF-IDF → Logistic Regression

## 4. Evaluation

Metrics:

- Accuracy
- F1 Score
- Confusion Matrix

## 5. Model Persistence

Save model as:

models/classifier.pkl
models/vectorizer.pkl

Use joblib or pickle.

## 6. Requirements

- sklearn
- pandas
- numpy