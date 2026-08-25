#!/usr/bin/env bash
# Host Intelligent Quiz Management System using MacBook Pro CPU & GPU

echo "🚀 Starting Intelligent Quiz Management System on MacBook Pro..."
cd "$(dirname "$0")"

# Activate virtualenv
source venv/bin/activate

# Start Django server in background
python manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!

echo "⚡ Django server started on http://0.0.0.0:8000 (PID: $SERVER_PID)"
echo "📡 Launching Cloudflare Tunnel for live public HTTPS access..."

# Launch Cloudflare tunnel
/opt/homebrew/bin/cloudflared tunnel --url http://127.0.0.1:8000
