FROM python:3.12-slim

ENV PORT=8000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY static ./static
COPY appconfig.json ./appconfig.json
COPY docker/entrypoint.sh ./docker/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker/entrypoint.sh"]
