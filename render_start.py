#!/usr/bin/env python3
"""
Render için WSGI entry point
"""

import os
from app import app, db

# Render environment ayarları
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    with app.app_context():
        db.create_all()
    
    # Render'da çalışması için
    app.run(host='0.0.0.0', port=port)
