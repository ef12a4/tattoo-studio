#!/usr/bin/env python3
"""
WSGI entry point for Tattoo Studio
"""

from app import app, db
from config import ProductionConfig

# Configure production settings
app.config.from_object(ProductionConfig)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
