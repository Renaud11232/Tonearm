FROM python:3.13-slim

ADD . /tmp/tonearm

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libffi-dev libnacl-dev \
    && rm -rf /var/cache/apt/archives /var/lib/apt/lists/* \
    && pip install --no-cache-dir /tmp/tonearm \
    && rm -rf /tmp/tonearm

ENTRYPOINT ["tonearm"]