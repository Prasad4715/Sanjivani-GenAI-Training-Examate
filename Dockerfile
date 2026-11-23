
FROM python:3.11-slim

WORKDIR /app

# Python environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .

# CPU-only PyTorch
RUN pip install --no-cache-dir torch \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and legal PDFs
COPY . .

# Download and cache the embedding model
RUN python -c "from app.embed import get_embedding_model; get_embedding_model()"

# Build the ChromaDB index inside the Docker image
RUN python -m app.vectorstore

# Default API port
EXPOSE 8000

# Start FastAPI
CMD ["sh", "-c", "exec python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
