FROM python:3.13 AS builder

ADD dist/*.whl /tmp/

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl unzip libffi-dev libnacl-dev \
    && curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh -s -- -y \
    && python -m venv /app \
    && /app/bin/pip install --no-cache-dir /tmp/*.whl


FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libffi-dev libnacl-dev \
    && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY --from=builder /app /app

COPY --from=builder /usr/local/bin/deno /usr/local/bin/deno

ENV DATA_PATH=/data

ENTRYPOINT ["/app/bin/tonearm"]