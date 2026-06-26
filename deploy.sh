#!/bin/bash

echo "Pulling latest code from Git..."
git pull origin main

echo "Rebuilding and starting containers (uv handling dependencies)..."
docker-compose up -d --build

echo "Running migrations..."
docker-compose exec web python manage.py migrate --noinput

echo "Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "Deployment complete!"