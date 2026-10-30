FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies as root.
COPY services/search_api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Prepare application files.
RUN mkdir -p /app/scripts && \
    useradd --create-home --shell /usr/sbin/nologin appuser

COPY --chown=appuser:appuser services/search_api/main.py ./main.py
COPY --chown=appuser:appuser scripts/search_subjects.py ./scripts/search_subjects.py

# Run as an unprivileged user.
USER appuser

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
