# Docker Plan

## 1. Services

- api
- vector store (if required)

## 2. Requirements

Single command:

docker compose up --build

## 3. Environment Variables

Use .env file for:

- API keys
- Config values

Do not hardcode secrets.

## 4. Build Strategy

Package only after core logic works locally.