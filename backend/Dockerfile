FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt ./requirements.txt

# Install python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend app folder
COPY app ./app

# Default port for Railway
ENV PORT=8000
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
