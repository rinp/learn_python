#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# 独立した project 名にして、既存の compose と衝突しないようにする
: "${COMPOSE_PROJECT_NAME:=learn_python_tools}"
export COMPOSE_PROJECT_NAME

compose=(docker compose -f docker-compose-tools.yml)

cleanup() {
  # `-v` を付けると uv_tools_venv / uv_tools_cache も消える
  ${compose[@]} down
}
trap cleanup EXIT

echo "Starting check environment..."
${compose[@]} up -d --no-deps tools >/dev/null

echo "Formatting code with ruff..."
${compose[@]} exec -T tools uv run ruff format .
echo "Checking code with ruff..."
${compose[@]} exec -T tools uv run ruff check .  --fix
echo " Running mypy..."
${compose[@]} exec -T tools uv run mypy app
echo "finished"
