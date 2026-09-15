$ErrorActionPreference = 'Stop'

if (-not $env:SECRET_KEY) {
    throw 'Set SECRET_KEY before opening the app publicly, for example: $env:SECRET_KEY = [guid]::NewGuid().ToString("N")'
}

$cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue
if (-not $cloudflared) {
    Write-Host 'Installing Cloudflare Tunnel for the current user...'
    winget install --id Cloudflare.cloudflared --scope user --accept-source-agreements --accept-package-agreements
    $cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue
}

if (-not $cloudflared) {
    throw 'Cloudflared was not found. Restart PowerShell after installation, then run this script again.'
}

$python = Join-Path $PSScriptRoot 'venv\Scripts\python.exe'
if (-not (Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath $python -ArgumentList 'run.py' -WorkingDirectory $PSScriptRoot
}

Write-Host 'Starting a temporary public HTTPS URL. Keep this window open.'
& $cloudflared.Source tunnel --url http://127.0.0.1:5000