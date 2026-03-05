FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

RUN addgroup --system app && adduser --system --group app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy BOTH requirements files
COPY requirements.txt requirements.prod.txt ./

# Install prod dependencies (includes gunicorn + gevent)
RUN pip install --no-cache-dir -r requirements.prod.txt

COPY --chown=app:app . .

RUN mkdir -p /app/instance && chown app:app /app/instance

USER app

EXPOSE 5000

CMD ["sh", "-c", "\
    python -c \"\
import sys; sys.path.insert(0, '/app'); \
from run import app; \
from app import db; \
from app.models import Room; \
ctx = app.app_context(); ctx.push(); \
db.create_all(); \
Room.get_or_create('general'); \
print('DB ready'); \
\" && gunicorn --config gunicorn.conf.py run:app"]
