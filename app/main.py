import logging
import sys
from fastapi import FastAPI
from app.routes import router

# Structured JSON logging
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","message":"%(message)s"}'
))
logging.basicConfig(level=logging.INFO, handlers=[handler])

app = FastAPI(title="AI Ticket Triage", version="1.0.0")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
