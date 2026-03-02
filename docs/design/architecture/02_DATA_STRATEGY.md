# Data Strategy

## 1. Dataset Source

- Kaggle IT Support Tickets
- 47,837 real samples
- 8 categories
- No urgency labels

## 2. Split Strategy

Stratified split:

- 80% Train
- 10% Validation
- 10% Test

No leakage between splits.

## 3. Hybrid Training Strategy

EDA applied ONLY on train set:

- WordNet synonym replacement
- Random swap
- Random deletion

Goal:
- Improve class balance
- Avoid overfitting
- Keep validation and test fully real

Final train size: 65,375 samples

## 4. Preprocessing Rules

- Lowercase
- Basic text cleaning
- TF-IDF vectorization (20k features, bigrams)