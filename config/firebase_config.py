# Firebase Authentication Configuration
import firebase_admin
from firebase_admin import credentials, auth
from flask import session, request, redirect, url_for
import os
import json

# Firebase Admin SDK initialization
# Firebase projesinden indirdiğiniz service account key dosyası
try:
    cred = credentials.Certificate("config/firebase-service-account.json")
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK başarıyla başlatıldı")
except Exception as e:
    print(f"Firebase başlatma hatası: {e}")
    # Development için mock credentials
    cred = None

class FirebaseManager:
    """Firebase Authentication Manager"""
    
    @staticmethod
    def get_firebase_config():
        """Frontend için Firebase config"""
        return {
            "apiKey": "AIzaSyDP43wZ9A8bmbvVEd0l-91vkPtxmVj6oBg",
            "authDomain": "tatto-59da5.firebaseapp.com",
            "projectId": "tatto-59da5",
            "storageBucket": "tatto-59da5.firebasestorage.app",
            "messagingSenderId": "948155824063",
            "appId": "1:948155824063:web:803b849eec40316d67530a",
            "measurementId": "G-V44CCWSMQ1"
        }
    
    @staticmethod
    def create_custom_token(uid):
        """Custom token oluştur"""
        try:
            custom_token = auth.create_custom_token(uid)
            return custom_token
        except Exception as e:
            print(f"Custom token oluşturma hatası: {e}")
            return None
    
    @staticmethod
    def verify_id_token(id_token):
        """ID token doğrula"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Token doğrulama hatası: {e}")
            return None
    
    @staticmethod
    def get_user(uid):
        """Firebase user bilgilerini al"""
        try:
            user = auth.get_user(uid)
            return user
        except Exception as e:
            print(f"Kullanıcı bilgileri alma hatası: {e}")
            return None
    
    @staticmethod
    def create_user(email, password=None, display_name=None):
        """Yeni Firebase kullanıcısı oluştur"""
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            return user
        except Exception as e:
            print(f"Kullanıcı oluşturma hatası: {e}")
            return None
    
    @staticmethod
    def update_user(uid, display_name=None, photo_url=None):
        """Kullanıcı bilgilerini güncelle"""
        try:
            user = auth.update_user(
                uid,
                display_name=display_name,
                photo_url=photo_url
            )
            return user
        except Exception as e:
            print(f"Kullanıcı güncelleme hatası: {e}")
            return None
    
    @staticmethod
    def delete_user(uid):
        """Kullanıcıyı sil"""
        try:
            auth.delete_user(uid)
            return True
        except Exception as e:
            print(f"Kullanıcı silme hatası: {e}")
            return False

# OAuth Provider Configuration - Gerçek Firebase proje bilgileri
OAUTH_PROVIDERS = {
    'google': {
        'enabled': True,
        'scopes': ['email', 'profile'],
        'client_id': '948155824063-7q3g5k8l5a2h5r9d1v8b5p1n1n.apps.googleusercontent.com',
        'redirect_uri': 'http://localhost:5000/auth/google/callback'
    },
    'facebook': {
        'enabled': True,
        'scopes': ['email', 'public_profile'],
        'app_id': '1234567890123456',  # Firebase'den alınacak
        'app_secret': 'your-facebook-app-secret',  # Firebase'den alınacak
        'redirect_uri': 'http://localhost:5000/auth/facebook/callback'
    },
    'apple': {
        'enabled': True,
        'scopes': ['name', 'email'],
        'client_id': 'com.tattoo.studio',
        'team_id': 'your-apple-team-id',
        'key_id': 'your-apple-key-id',
        'redirect_uri': 'http://localhost:5000/auth/apple/callback'
    },
    'github': {
        'enabled': True,
        'scopes': ['user:email'],
        'client_id': 'your-github-client-id',
        'client_secret': 'your-github-client-secret',
        'redirect_uri': 'http://localhost:5000/auth/github/callback'
    },
    'twitter': {
        'enabled': True,
        'scopes': ['email', 'profile'],
        'api_key': 'your-twitter-api-key',
        'api_secret': 'your-twitter-api-secret',
        'redirect_uri': 'http://localhost:5000/auth/twitter/callback'
    }
}

# Firebase Security Rules Template
FIREBASE_RULES = {
    "rules": {
        "users": {
            "$uid": {
                ".read": "$uid === auth.uid",
                ".write": "$uid === auth.uid"
            }
        },
        "studios": {
            ".read": "auth != null",
            "$studioId": {
                ".write": "auth != null && (data.child('ownerId').val() === auth.uid || newData.child('ownerId').val() === auth.uid)"
            }
        },
        "appointments": {
            "$uid": {
                ".read": "$uid === auth.uid",
                ".write": "$uid === auth.uid"
            }
        }
    }
}
