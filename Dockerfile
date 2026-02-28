# ── Stage 1: base ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Create non-root user for security
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# ── Stage 2: dependencies ──────────────────────────────────────────────────
FROM base AS deps

# Install system dependencies needed for gevent
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 3: final ─────────────────────────────────────────────────────────
FROM deps AS final

# Copy app source
COPY --chown=app:app . .

# Create directory for SQLite database with correct permissions
RUN mkdir -p /app/instance && chown app:app /app/instance

# Switch to non-root user
USER app

# Expose port
EXPOSE 5000

# Initialise DB then start gunicorn
CMD ["sh", "-c", "python -c 'from run import app; from app import db; \
     app.app_context().__enter__(); db.create_all()' && \
     gunicorn --config gunicorn.conf.py run:app"]
