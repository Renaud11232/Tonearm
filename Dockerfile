FROM python:3.13 AS builder

ADD . /tmp/tonearm

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev libnacl-dev \
    && python -m venv /app \
    && /app/bin/pip install --no-cache-dir /tmp/tonearm


FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libffi-dev libnacl-dev \
    && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY --from=builder /app /app

ENTRYPOINT ["/app/bin/tonearm"]