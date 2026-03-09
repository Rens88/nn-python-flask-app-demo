#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="local-app"
CONTAINER_NAME="local-app-test"
CHECK_URL="http://localhost:8000"
MAX_ATTEMPTS=30

require_command() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: '$cmd' command not found." >&2
    exit 1
  fi
}

cleanup() {
  docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT

require_command docker
require_command curl

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon is not available." >&2
  exit 1
fi

docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

echo "Building local-app image..."
docker build -t "$IMAGE_NAME" .

echo "Starting local-app-test container..."
docker run --rm -d --name "$CONTAINER_NAME" -p 8000:8000 "$IMAGE_NAME" >/dev/null

for _ in $(seq 1 "$MAX_ATTEMPTS"); do
  http_code="$(curl -s -o /dev/null -w "%{http_code}" "$CHECK_URL" || true)"
  if [[ "${http_code}" =~ ^[1-5][0-9][0-9]$ ]]; then
    echo "OK: container responded on port 8000"
    exit 0
  fi
  sleep 1
done

echo "ERROR: container did not respond on port 8000"
docker logs "$CONTAINER_NAME" || true
exit 1
