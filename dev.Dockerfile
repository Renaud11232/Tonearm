FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libffi-dev libnacl-dev \
    && pip install --no-cache-dir "https://github.com/Renaud11232/Tonearm/archive/refs/heads/dev.zip"

ENTRYPOINT ["tonearm"]