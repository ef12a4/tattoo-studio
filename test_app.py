#!/usr/bin/env python3
"""
Render için test
"""

import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Tattoo Studio - Render Test!"

@app.route('/health')
def health():
    return {"status": "ok", "message": "Tattoo Studio running"}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting test app on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
