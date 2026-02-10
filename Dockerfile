
# Use Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage cache
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories and set permissions before switching user
RUN mkdir -p logs scraped_pages chroma_db && \
    chmod -R 777 logs scraped_pages chroma_db

# Create a non-root user (Hugging Face Spaces requirement)
RUN useradd -m -u 1000 user && \
    chown -R user:user /app

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
