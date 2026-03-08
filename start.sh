#!/bin/bash
# Glitch startup script

echo "🎨 Starting Tattoo Studio on Glitch..."

# Install dependencies
pip install -r requirements.txt

# Initialize database if needed
python init_db.py

# Start the server
export PORT=${PORT:-3000}
export FLASK_ENV=production
gunicorn --bind 0.0.0.0:$PORT wsgi:app
