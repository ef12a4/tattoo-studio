#!/usr/bin/env python3
"""
Production configuration for Tattoo Studio
"""

import os
from dotenv import load_dotenv

load_dotenv()

class ProductionConfig:
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tattoo_studio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tattoo_studio_production_secret_key_2024'
    
    # Session
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Payment
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    IYZICO_API_KEY = os.environ.get('IYZICO_API_KEY')
    IYZICO_SECRET_KEY = os.environ.get('IYZICO_SECRET_KEY')
    
    # Firebase
    FIREBASE_CONFIG = os.environ.get('FIREBASE_CONFIG')
    
    # Logging
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    # Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
