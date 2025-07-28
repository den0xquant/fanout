FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code/

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

ENV PATH="/code/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/code

COPY ./scripts /code/scripts

COPY ./pyproject.toml ./uv.lock ./alembic.ini /code/

COPY ./alembic /code/alembic

COPY ./app /code/app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Command to run the application
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
