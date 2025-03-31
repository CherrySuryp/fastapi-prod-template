FROM ghcr.io/astral-sh/uv:python3.13-alpine AS build
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-cache
COPY . /app

FROM build AS dev
ENV ENV=LOCAL
CMD ["uv", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

FROM build AS test
ENV ENV=TEST
CMD ["uv", "run", "pytest"]
