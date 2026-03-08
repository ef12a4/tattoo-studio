#!/usr/bin/env python3
"""
Render için minimal Flask uygulaması
"""

import os
from flask import Flask, render_template

app = Flask(__name__)

# Render için ayarlar
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'render_secret_key_2024')

@app.route('/')
def home():
    return """
    <h1>🎨 Tattoo Studio - Render Test</h1>
    <h2>✅ Uygulama Çalışıyor!</h2>
    <p>URL: <a href="/health">/health</a></p>
    <p>URL: <a href="/test">/test</a></p>
    """

@app.route('/health')
def health():
    return {"status": "sağlıklı", "message": "Tattoo Studio çalışıyor"}

@app.route('/test')
def test():
    return "<h1>Test Sayfası - Başarılı! 🎉</h1>"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Tattoo Studio starting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
