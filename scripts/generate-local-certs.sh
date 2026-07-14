#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CERT_DIR="${1:-$ROOT_DIR/nginx/certs}"

mkdir -p "$CERT_DIR"

openssl req -x509 -nodes -newkey rsa:2048 -sha256 \
  -days 365 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:::1" \
  -keyout "$CERT_DIR/key.pem" \
  -out "$CERT_DIR/cert.pem"

echo "Generated self-signed certificate in $CERT_DIR"
echo "Use docker compose up -d --build to pick it up"
