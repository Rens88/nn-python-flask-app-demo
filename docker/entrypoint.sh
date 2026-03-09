#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="${APPCONFIG_PATH:-appconfig.json}"

read_json_key() {
  local file="$1"
  local key="$2"
  python - "$file" "$key" <<'PY'
import json
import sys

file_path = sys.argv[1]
key = sys.argv[2]

try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("")
    raise SystemExit(0)

value = data.get(key, "")
print(value if value is not None else "")
PY
}

DEFAULT_APP_TYPE="$(read_json_key "$CONFIG_FILE" "app_type")"
DEFAULT_APP_MODULE="$(read_json_key "$CONFIG_FILE" "app_module")"
DEFAULT_PORT="$(read_json_key "$CONFIG_FILE" "port")"

APP_TYPE="${APP_TYPE:-${DEFAULT_APP_TYPE:-flask}}"
APP_MODULE="${APP_MODULE:-${DEFAULT_APP_MODULE:-src.app}}"
PORT="${PORT:-${DEFAULT_PORT:-8000}}"

case "$APP_TYPE" in
  flask)
    exec gunicorn "${APP_MODULE}:app" \
      --bind "0.0.0.0:${PORT}" \
      --workers 2 \
      --threads 4 \
      --timeout 120
    ;;
  dash)
    exec gunicorn "${APP_MODULE}:server" \
      --bind "0.0.0.0:${PORT}" \
      --workers 2 \
      --threads 4
    ;;
  streamlit)
    exec streamlit run src/app.py \
      --server.address 0.0.0.0 \
      --server.port "${PORT}" \
      --server.headless true \
      --browser.gatherUsageStats false
    ;;
  *)
    echo "Unsupported APP_TYPE: ${APP_TYPE}. Supported values: flask, streamlit, dash" >&2
    exit 1
    ;;
esac
