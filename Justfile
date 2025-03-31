LOCAL_IMAGE := "fastapi-lambda"

default:
    @just --list

venv:
    #!/usr/bin/env sh
    if [ ! -f .venv/bin/activate ]; then
        uv python install ">=3.13,<3.14"
        uv venv --python ">=3.13,<3.14"
        source .venv/bin/activate
        echo "\033[32m🍰 .venv created\033[0m"
    else
        echo "\033[33m🍰 .venv exists\033[0m"
    fi

deps: venv
    @uv sync --no-cache

pre-commit:
    @pre-commit install

init: venv deps pre-commit

serve-local:
    uv run uvicorn app.main:app --reload

docker-build-dev:
    docker build --target=dev -t {{ LOCAL_IMAGE }} -f infra/docker/local.Dockerfile .

docker-build-test:
    docker build --target=test -t {{ LOCAL_IMAGE }} -f infra/docker/local.Dockerfile .

serve-docker: docker-build-dev
    LOCAL_IMAGE={{ LOCAL_IMAGE }} docker compose \
     -f infra/docker-compose/base.yml \
     -f infra/docker-compose/server.yml \
     up

docker-down:
    LOCAL_IMAGE={{ LOCAL_IMAGE }} docker compose \
     -f infra/docker-compose/base.yml \
     -f infra/docker-compose/server.yml \
     down

# Testing commands
test-local:
    uv run pytest

test-docker: docker-build-test
    docker run --rm --env-file="infra/docker-compose/.env.local" {{ LOCAL_IMAGE }}

fmt:
    uv tool run ruff format
    uv tool run ruff check --fix
