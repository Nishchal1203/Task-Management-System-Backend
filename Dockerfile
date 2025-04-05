FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -m appuser

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir pandas==2.0.3 && \
    pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Create directory for migrations and set permissions
RUN mkdir -p /app/migrations && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"] 