# ==============================
# Base Image
# ==============================
FROM python:3.12-slim

# ==============================
# Environment Variables
# ==============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ==============================
# Working Directory
# ==============================
WORKDIR /app

# ==============================
# Install System Dependencies
# ==============================
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# Install Python Dependencies
# ==============================
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ==============================
# Copy Application
# ==============================
COPY . .

# ==============================
# Create Non-Root User
# ==============================
RUN useradd -ms /bin/bash appuser

RUN chown -R appuser:appuser /app

USER appuser

# ==============================
# Expose Port
# ==============================
EXPOSE 5000

# ==============================
# Run Application
# ==============================
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
