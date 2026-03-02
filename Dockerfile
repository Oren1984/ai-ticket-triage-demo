# Dockerfile

# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data needed for EDA augmentation
RUN python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

# Copy project files
COPY . .

# Run the full training pipeline at build time
RUN python scripts/split_data.py
RUN python scripts/augment_data.py
RUN python scripts/train_kaggle_model.py
RUN python scripts/ingest_knowledge.py

# Expose API port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
