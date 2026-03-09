#!/usr/bin/env bash
set -euo pipefail

require_command() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: '$cmd' command not found." >&2
    exit 1
  fi
}

require_command docker

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon is not available." >&2
  exit 1
fi

echo "Building local-app image..."
docker build -t local-app .

docker rm -f local-app-dev >/dev/null 2>&1 || true

echo "Starting container at http://localhost:8000"
exec docker run \
  --rm \
  --name local-app-dev \
  -p 8000:8000 \
  local-app
