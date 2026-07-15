# Use an official lightweight Python image
FROM python:3.14-slim

# Copy the uv binaries from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables to optimize Python/uv behavior inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# 1. Install system dependencies (Node.js & build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies (Cached by uv)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# 3. Copy ONLY Node dependency files first
COPY theme/static_src/package*.json /app/theme/static_src/

# 4. Install Node dependencies using an npm cache mount (Blazing fast!)
WORKDIR /app/theme/static_src
RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund

# 5. Copy the rest of your application code
WORKDIR /app
COPY . /app/

# Ensure the container uses the virtual environment created by uv.
ENV PATH="/app/.venv/bin:$PATH"

# 6. Build Tailwind CSS (Only takes a second because node_modules is already built)
WORKDIR /app/theme/static_src
RUN npm run build

WORKDIR /app

EXPOSE 8000