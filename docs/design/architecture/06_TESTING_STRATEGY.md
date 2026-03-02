# Testing Strategy

## 1. Unit Tests

Test:

- Model loading
- Prediction output
- RAG retrieval
- Text preprocessing

Use pytest.

## 2. Integration Tests

Full flow:

Ticket → Classification → RAG → Response

## 3. Current Status

- 19 tests passing
- Docker validated
- Endpoints verified