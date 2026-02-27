#!/usr/bin/env bash
set -euo pipefail

if [[ -f .env ]]; then
  set -a
  source .env
  set +a
fi

HOST="${APP_HOST:-0.0.0.0}"
PORT="${APP_PORT:-8080}"

PYTHONPATH=src uvicorn blindsearch_engine.api.app:app --host "$HOST" --port "$PORT"
