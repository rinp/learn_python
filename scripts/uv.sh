#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# 独立した project 名にして、既存の compose と衝突しないようにする
: "${COMPOSE_PROJECT_NAME:=learn_python_tools}"
export COMPOSE_PROJECT_NAME

uv_args=("$@")
if [ ${#uv_args[@]} -eq 0 ]; then
  echo "usage: $0 <uv arguments...>" >&2
  echo "example: $0 init" >&2
  exit 1
fi

compose=(docker compose -f docker-compose-tools.yml)

cleanup() {
  # `-v` を付けると uv_tools_venv / uv_tools_cache も消える
  ${compose[@]} down
}
trap cleanup EXIT

echo "Starting check environment..."
${compose[@]} up -d --no-deps tools >/dev/null

echo "Running uv: ${uv_args[*]}"
${compose[@]} exec -T tools uv "${uv_args[@]}"
echo "finished"
