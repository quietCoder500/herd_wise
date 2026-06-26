#!/bin/bash

echo "Pulling latest code from Git..."
git pull origin master

echo "Rebuilding and starting containers (uv handling dependencies)..."
docker compose up -d --build

echo "Building Tailwind assets inside the web container..."
docker compose exec -e ENV_NAME=Production web sh -lc "cd /app/theme/static_src && npm ci --no-audit --no-fund && npm run build"

echo "Running migrations..."
docker compose exec -e ENV_NAME=Production web uv run manage.py migrate --noinput

echo "Collecting static files..."
docker compose exec -e ENV_NAME=Production web uv run manage.py collectstatic --noinput

echo "Deployment complete!"