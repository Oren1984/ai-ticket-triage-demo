# app/main.py
# This file serves as the entry point for the FastAPI application.
# It sets up structured logging, initializes the FastAPI app, and defines basic routes for the index page and health check. The

import logging
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routes import router

# Structured JSON logging
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","message":"%(message)s"}'
))
logging.basicConfig(level=logging.INFO, handlers=[handler])

_TEMPLATES = Path(__file__).parent / "templates"

app = FastAPI(title="AI Ticket Triage", version="1.0.0")
app.include_router(router)

# Basic routes
@app.get("/", include_in_schema=False)
def index():
    return FileResponse(_TEMPLATES / "index.html")

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
