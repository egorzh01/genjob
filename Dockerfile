FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /genjob

# UV
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Системные зависимости
RUN apt-get update && apt-get install -y \
    media-types \
    && rm -rf /var/lib/apt/lists/*

# Зависимости отдельно для кеша
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ENV PATH="/genjob/.venv/bin:$PATH"

# Копируем проект
COPY . .

# Установка самого проекта
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Если нужен PYTHONPATH
ENV PYTHONPATH="/genjob/src"

CMD ["uvicorn", "genjob.cmd.api:app", "--host", "0.0.0.0", "--port", "8000"]
