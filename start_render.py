#!/usr/bin/env python3
"""
Render için basit start
"""

import os
import sys

# Render için port ayarı
port = int(os.environ.get('PORT', 5000))

try:
    from app import app
    
    # Render için ayarlar
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'render_secret_key')
    
    if __name__ == "__main__":
        print(f"Starting app on port {port}...")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
