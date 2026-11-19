FROM denoland/deno:bin-2.9.8 AS deno

FROM mwader/static-ffmpeg:9.0.2-1 AS ffmpeg

FROM python:3.14 AS builder

ADD dist/*.whl /tmp/

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev libnacl-dev \
    && python -m venv /app \
    && /app/bin/pip install --no-cache-dir /tmp/*.whl


FROM python:3.14-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libffi-dev libnacl-dev \
    && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY --from=deno /deno /usr/local/bin/deno

COPY --from=ffmpeg /ffmpeg /ffprobe /usr/local/bin/

COPY --from=builder /app /app

ENV DATA_PATH=/data

ENTRYPOINT ["/app/bin/tonearm"]