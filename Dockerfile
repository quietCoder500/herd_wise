# Use an official lightweight Python image
FROM python:3.14.6-slim

# Copy the uv binaries from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables to optimize Python/uv behavior inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (required for some Python packages like psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies into the container environment.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# -------------------------------------------------------------------------
# OPTION B: If you are still using a standard requirements.txt with uv
# (Uncomment the two lines below and comment out Option A if using this)
# -------------------------------------------------------------------------
# COPY requirements.txt /app/
# RUN --mount=type=cache,target=/root/.cache/uv uv pip install --system -r requirements.txt
# -------------------------------------------------------------------------

# Copy the rest of your application code into the container
COPY . /app/

# Ensure the container uses the virtual environment created by uv.
ENV PATH="/app/.venv/bin:$PATH"

# Build Tailwind CSS directly with the local npm pipeline for a faster compile.
WORKDIR /app/theme/static_src
RUN npm ci --no-audit --no-fund
RUN npm run build

WORKDIR /app

# Expose Gunicorn's port
EXPOSE 8000