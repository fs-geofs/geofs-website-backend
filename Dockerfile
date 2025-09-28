FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1
ENV UV_NO_CACHE=1

RUN apk update
RUN apk upgrade --no-cache
RUN apk add --no-cache git

# Install UV
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

RUN mkdir git-content
RUN chown 1000:1000 git-content

WORKDIR /app

COPY . .
RUN uv sync --no-cache --locked
RUN uv add --no-cache gunicorn

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "run:app"]