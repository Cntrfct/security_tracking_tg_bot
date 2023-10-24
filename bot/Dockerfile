FROM python:3.11.6-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt

RUN python3 -m pip install wheel --no-cache-dir && \
    python3 -m pip install --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt

FROM python:3.11.6-slim

RUN groupadd -r bot &&  \
    useradd -r -s /bin/false -g bot bot

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH="/opt/venv/bin:/opt/venv/lib/python3.11/site-packages"

WORKDIR /app
COPY . .
RUN chown -R bot:bot /app
USER bot