#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

COMPOSE_PROJECT_NAME="$(basename "$PWD")_test"

cleanup() {
  # `-v` を付けると uv_tools_venv / uv_tools_cache も消える
  docker compose -f docker-compose-test.yml down -v
}
trap cleanup EXIT

docker compose -f docker-compose-test.yml up --build -d
docker compose -f docker-compose-test.yml exec test_web uv run pytest --cov=app
