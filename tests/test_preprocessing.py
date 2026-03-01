# tests/test_preprocessing.py
# This test file contains unit tests for the text preprocessing function used in the training script and FastAPI application.
# It uses pytest to define test cases that check the output of the clean_text function, ensuring that it correctly lowercases text,
# removes special characters, normalizes whitespace, and handles edge cases like empty strings.
# These tests help ensure that the text preprocessing step is working as expected, which

from app.services.preprocessing import clean_text

# lowercase test
def test_lowercase():
    assert clean_text("HELLO WORLD") == "hello world"

# remove special characters test
def test_remove_special_chars():
    assert clean_text("error: disk full!!!") == "error disk full"

# normalize whitespace test
def test_normalize_whitespace():
    assert clean_text("too   many    spaces") == "too many spaces"

# combined test
def test_combined():
    result = clean_text("  ERROR: CPU usage @100%!!  ")
    assert result == "error cpu usage 100"

# edge case: empty string
def test_empty_string():
    assert clean_text("") == ""
