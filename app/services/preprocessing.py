# app/services/preprocessing.py
# This file defines a function to clean and preprocess ticket text before classification.
# The `clean_text` function lowercases the text, removes special characters,
# and normalizes whitespace to improve the performance of the machine learning models used for category and urgency prediction.

import re

# Text preprocessing function
def clean_text(text: str) -> str:
    """Lowercase, remove special characters, normalize whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
