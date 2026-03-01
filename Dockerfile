# Dockerfile

# # Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Train model and ingest knowledge base during build time
RUN python scripts/train_model.py
RUN python scripts/ingest_knowledge.py

# Expose API port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
