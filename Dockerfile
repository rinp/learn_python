ARG PY_VERSION=3.14
FROM python:${PY_VERSION}-rc-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/

RUN apt-get update

WORKDIR /work
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY .env.dev .env.dev
COPY .env.local .env.local
COPY .env.test .env.test

ENV UV_LINK_MODE=copy 
RUN uv sync --frozen

# --host 0.0.0.0だとIPv6でアクセスできないので、--host ::に変更
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "::", "--port", "8000", "--reload", "--log-level", "debug", "--access-log"]
