# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for GUI and Windows API access
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs assets config

# Set environment variables
ENV PYTHONPATH=/app
ENV DISPLAY=:0

# Expose any ports if needed (for future web interface)
# EXPOSE 8000

# Set default environment variables
ENV LOG_LEVEL=INFO
ENV PET_NAME=Pixie
ENV PET_PERSONALITY="helpful and friendly"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import src.utils.helpers; print('healthy')" || exit 1

# Run the application
CMD ["python", "main.py"]