
FROM python:3.13-slim-bookworm AS python-build-stage

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG CURRENT_ENVIRONMENT=dev
ARG APP_HOME=/app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
ENV PYTHONOPTIMIZE=1

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev

WORKDIR $APP_HOME

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./uv.lock,target=uv.lock \
    --mount=type=bind,source=./pyproject.toml,target=pyproject.toml \
    if [ "$CURRENT_ENVIRONMENT" = "development" ]; then \
        uv sync --frozen --no-editable; \
    else \
        uv sync --frozen --no-editable --no-dev; \
    fi


FROM python:3.13-slim-bookworm AS python-run-stage

ARG CURRENT_ENVIRONMENT
ARG APP_HOME=/app

ENV PATH="$APP_HOME/.venv/bin:$PATH"

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        wait-for-it && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY --link --from=python-build-stage $APP_HOME $APP_HOME

WORKDIR $APP_HOME

COPY . .

COPY ./docker/django/entrypoint.sh ./docker/django/
COPY ./docker/django/celery/entrypoint.sh ./docker/django/celery/
COPY ./docker/django/init/entrypoint-$CURRENT_ENVIRONMENT.sh ./docker/django/init/

RUN sed -i 's/\r$//g' \
        ./docker/django/entrypoint.sh \
        ./docker/django/celery/entrypoint.sh \
        ./docker/django/init/entrypoint-$CURRENT_ENVIRONMENT.sh && \
    chmod +x \
        ./docker/django/entrypoint.sh \
        ./docker/django/celery/entrypoint.sh \
        ./docker/django/init/entrypoint-$CURRENT_ENVIRONMENT.sh
