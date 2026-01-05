#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# FIXME jsonファイルの生成をfastAPI起動してjson出力させるようにできればベスト

docker run --rm -v "$PWD":/app -w /app redocly/cli build-docs ./page/openApi/openapi.json -o ./page/openApi/index.html
