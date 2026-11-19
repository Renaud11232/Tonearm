FROM denoland/deno:bin AS deno

FROM python:3.14 AS builder

ADD dist/*.whl /tmp/

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev libnacl-dev \
    && python -m venv /app \
    && /app/bin/pip install --no-cache-dir /tmp/*.whl


FROM python:3.14-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libffi-dev libnacl-dev \
    && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY --from=deno /deno /usr/local/bin/deno

COPY --from=builder /app /app

ENV DATA_PATH=/data

ENTRYPOINT ["/app/bin/tonearm"]