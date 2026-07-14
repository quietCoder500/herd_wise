param(
    [string]$OutputDir = "$PSScriptRoot/../nginx/certs"
)

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$certPath = Join-Path $OutputDir "cert.pem"
$keyPath = Join-Path $OutputDir "key.pem"

& openssl req -x509 -nodes -newkey rsa:2048 -sha256 `
  -days 365 `
  -subj "/CN=localhost" `
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:::1" `
  -keyout $keyPath `
  -out $certPath

Write-Host "Generated self-signed certificate in $OutputDir"
Write-Host "Use docker compose up -d --build to pick it up"
