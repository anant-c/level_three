FROM astral/uv:python3.12-bookworm

WORKDIR /app

COPY app/pyproject.toml app/uv.lock* ./

RUN uv sync

COPY ./app .

CMD ["uv", "run", "--host", "0.0.0.0", "--port", "8000", "main:app"]