#!/bin/bash
set -e # Exit immediately if any command fails

echo "Pulling latest code from Git..."
git pull origin master

echo "Rebuilding and starting containers..."
docker compose build web
docker compose up -d

echo "Running migrations..."
docker compose exec -e ENV_NAME=Production web uv run manage.py migrate --noinput

echo "Collecting static files..."
docker compose exec -e ENV_NAME=Production web uv run manage.py collectstatic --noinput

echo "Deployment complete!"