ARG PY_VERSION=3.14
FROM python:${PY_VERSION}-rc-slim
#COPY --from=astral/uv:${UV_VERSION}-python${PY_VERSION}-trixie-slim /uv /uvx /bin/
COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/

# 原因特定用：最終的には不要
RUN apt-get update
RUN apt-get install -y curl iproute2 net-tools

WORKDIR /work
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

RUN uv sync --frozen
WORKDIR /work/app

# --host 0.0.0.0だとIPv6でアクセスできないので、--host ::に変更
CMD ["uv", "run", "uvicorn", "main:app", "--host", "::", "--port", "8000", "--reload", "--log-level", "debug", "--access-log"]
