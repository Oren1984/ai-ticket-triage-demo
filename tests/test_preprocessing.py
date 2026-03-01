from app.services.preprocessing import clean_text


def test_lowercase():
    assert clean_text("HELLO WORLD") == "hello world"


def test_remove_special_chars():
    assert clean_text("error: disk full!!!") == "error disk full"


def test_normalize_whitespace():
    assert clean_text("too   many    spaces") == "too many spaces"


def test_combined():
    result = clean_text("  ERROR: CPU usage @100%!!  ")
    assert result == "error cpu usage 100"


def test_empty_string():
    assert clean_text("") == ""
