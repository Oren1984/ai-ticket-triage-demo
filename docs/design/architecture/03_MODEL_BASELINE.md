# ML Baseline Model

## 1. Objective

Predict ticket category (8 classes).

Urgency currently returned as placeholder ("Medium").

## 2. Model Type

- TF-IDF Vectorizer
- Logistic Regression
- class_weight="balanced"

## 3. Pipeline

Text → Clean → TF-IDF → Logistic Regression

## 4. Evaluation

Metrics:

- Accuracy
- Macro F1
- Confusion Matrix

Real Test Results:

- Accuracy: 0.86
- Macro F1: 0.86
- No overfitting (val ≈ test)

## 5. Model Persistence

Artifacts:

models/vectorizer.pkl  
models/classifier.pkl  
models/label_encoder.pkl