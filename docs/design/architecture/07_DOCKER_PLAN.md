# Docker Plan

## 1. Build Phase

During docker compose build:

- Install dependencies
- Split dataset
- Augment train set
- Train model
- Ingest runbooks

Artifacts baked into image.

## 2. Runtime Phase

docker compose up:

- Load trained artifacts
- Start FastAPI
- No retraining at runtime

## 3. Environment Variables

Use .env for configuration.

No hardcoded secrets.

## 4. Deployment Strategy

Single command:

docker compose up --build

Reproducible container.