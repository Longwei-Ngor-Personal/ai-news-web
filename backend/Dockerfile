FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Install system dependencies (if needed later for some libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create data directory for SQLite DB
RUN mkdir -p /app/data

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY app /app/app

# Expose the port FastAPI will run on
EXPOSE 8000

# Default command to run the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
