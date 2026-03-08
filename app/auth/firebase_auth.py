"""Firebase Authentication Integration"""
from flask import Blueprint, request, jsonify, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash
import requests
import jwt
import json
from datetime import datetime, timedelta
from config.firebase_config import FirebaseManager, OAUTH_PROVIDERS
from app import db
from app.models import User, Studio, Artist, Customer

firebase_auth_bp = Blueprint('firebase_auth', __name__)

class FirebaseAuthService:
    """Firebase Authentication Service"""
    
    def __init__(self):
        self.firebase = FirebaseManager()
    
    def handle_firebase_login(self, id_token):
        """Firebase ile giriş işlemini yönet"""
        try:
            # ID token'ı doğrula
            decoded_token = self.firebase.verify_id_token(id_token)
            if not decoded_token:
                return {'success': False, 'message': 'Token doğrulanamadı'}
            
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            name = decoded_token.get('name', '')
            picture = decoded_token.get('picture', '')
            
            # Veritabanında kullanıcıyı kontrol et
            user = User.query.filter_by(email=email).first()
            
            if not user:
                # Yeni kullanıcı oluştur
                user = User(
                    username=email.split('@')[0],
                    email=email,
                    password_hash=generate_password_hash('firebase_user'), # Dummy password
                    role='customer'
                )
                db.session.add(user)
                db.session.flush()
                
                # Müşteri kaydı oluştur
                customer = Customer(
                    name=name,
                    email=email,
                    user_id=user.id
                )
                db.session.add(customer)
                db.session.commit()
            
            # Firebase UID'yi kullanıcıya kaydet
            user.firebase_uid = uid
            user.profile_picture = picture
            db.session.commit()
            
            return {
                'success': True,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.customer.name if hasattr(user, 'customer') else name,
                    'role': user.role,
                    'picture': picture
                }
            }
            
        except Exception as e:
            print(f"Firebase login hatası: {e}")
            return {'success': False, 'message': str(e)}
    
    def handle_oauth_login(self, provider, code):
        """OAuth ile giriş işlemini yönet"""
        try:
            provider_config = OAUTH_PROVIDERS.get(provider)
            if not provider_config or not provider_config.get('enabled'):
                return {'success': False, 'message': f'{provider} entegrasyonu aktif değil'}
            
            if provider == 'google':
                return self._handle_google_oauth(code)
            elif provider == 'facebook':
                return self._handle_facebook_oauth(code)
            elif provider == 'github':
                return self._handle_github_oauth(code)
            elif provider == 'apple':
                return self._handle_apple_oauth(code)
            elif provider == 'twitter':
                return self._handle_twitter_oauth(code)
            else:
                return {'success': False, 'message': 'Desteklenmeyen sağlayıcı'}
                
        except Exception as e:
            print(f"OAuth login hatası: {e}")
            return {'success': False, 'message': str(e)}
    
    def _handle_google_oauth(self, code):
        """Google OAuth"""
        try:
            # Access token al
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                'code': code,
                'client_id': OAUTH_PROVIDERS['google']['client_id'],
                'client_secret': 'your-google-client-secret', # Gerçek uygulamada environment'den alınmalı
                'redirect_uri': OAUTH_PROVIDERS['google']['redirect_uri'],
                'grant_type': 'authorization_code'
            }
            
            response = requests.post(token_url, data=data)
            token_data = response.json()
            
            if 'access_token' not in token_data:
                return {'success': False, 'message': 'Google token alınamadı'}
            
            # Kullanıcı bilgilerini al
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {'Authorization': f"Bearer {token_data['access_token']}"}
            user_response = requests.get(user_info_url, headers=headers)
            user_data = user_response.json()
            
            return self._create_or_update_user(user_data, 'google')
            
        except Exception as e:
            return {'success': False, 'message': f'Google OAuth hatası: {str(e)}'}
    
    def _handle_facebook_oauth(self, code):
        """Facebook OAuth"""
        try:
            # Access token al
            token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
            params = {
                'code': code,
                'client_id': OAUTH_PROVIDERS['facebook']['app_id'],
                'client_secret': OAUTH_PROVIDERS['facebook']['app_secret'],
                'redirect_uri': OAUTH_PROVIDERS['facebook']['redirect_uri']
            }
            
            response = requests.get(token_url, params=params)
            token_data = response.json()
            
            if 'access_token' not in token_data:
                return {'success': False, 'message': 'Facebook token alınamadı'}
            
            # Kullanıcı bilgilerini al
            user_info_url = "https://graph.facebook.com/me"
            params = {
                'fields': 'id,name,email,picture',
                'access_token': token_data['access_token']
            }
            
            user_response = requests.get(user_info_url, params=params)
            user_data = user_response.json()
            
            return self._create_or_update_user(user_data, 'facebook')
            
        except Exception as e:
            return {'success': False, 'message': f'Facebook OAuth hatası: {str(e)}'}
    
    def _handle_github_oauth(self, code):
        """GitHub OAuth"""
        try:
            # Access token al
            token_url = "https://github.com/login/oauth/access_token"
            data = {
                'code': code,
                'client_id': OAUTH_PROVIDERS['github']['client_id'],
                'client_secret': OAUTH_PROVIDERS['github']['client_secret']
            }
            headers = {'Accept': 'application/json'}
            
            response = requests.post(token_url, data=data, headers=headers)
            token_data = response.json()
            
            if 'access_token' not in token_data:
                return {'success': False, 'message': 'GitHub token alınamadı'}
            
            # Kullanıcı bilgilerini al
            user_info_url = "https://api.github.com/user"
            headers = {'Authorization': f"token {token_data['access_token']}"}
            
            user_response = requests.get(user_info_url, headers=headers)
            user_data = user_response.json()
            
            # Email için ayrı istek
            email_url = "https://api.github.com/user/emails"
            email_response = requests.get(email_url, headers=headers)
            emails = email_response.json()
            
            # Primary email'i bul
            primary_email = None
            for email_info in emails:
                if email_info.get('primary') and email_info.get('verified'):
                    primary_email = email_info['email']
                    break
            
            user_data['email'] = primary_email or user_data.get('email', '')
            
            return self._create_or_update_user(user_data, 'github')
            
        except Exception as e:
            return {'success': False, 'message': f'GitHub OAuth hatası: {str(e)}'}
    
    def _handle_apple_oauth(self, code):
        """Apple Sign In"""
        try:
            # Apple Sign In implementasyonu
            # JWT token validation gerektirir
            return {'success': False, 'message': 'Apple Sign In yakında eklenecek'}
            
        except Exception as e:
            return {'success': False, 'message': f'Apple OAuth hatası: {str(e)}'}
    
    def _handle_twitter_oauth(self, code):
        """Twitter OAuth"""
        try:
            # Twitter OAuth 2.0 implementasyonu
            return {'success': False, 'message': 'Twitter OAuth yakında eklenecek'}
            
        except Exception as e:
            return {'success': False, 'message': f'Twitter OAuth hatası: {str(e)}'}
    
    def _create_or_update_user(self, user_data, provider):
        """OAuth ile kullanıcı oluştur veya güncelle"""
        try:
            email = user_data.get('email')
            name = user_data.get('name', '')
            picture = user_data.get('picture', user_data.get('avatar_url', ''))
            
            if not email:
                return {'success': False, 'message': 'Email bilgisi alınamadı'}
            
            # Veritabanında kullanıcıyı kontrol et
            user = User.query.filter_by(email=email).first()
            
            if not user:
                # Yeni kullanıcı oluştur
                user = User(
                    username=email.split('@')[0],
                    email=email,
                    password_hash=generate_password_hash('oauth_user'), # Dummy password
                    role='customer'
                )
                db.session.add(user)
                db.session.flush()
                
                # Müşteri kaydı oluştur
                customer = Customer(
                    name=name,
                    email=email,
                    user_id=user.id
                )
                db.session.add(customer)
            
            # OAuth bilgilerini güncelle
            user.oauth_provider = provider
            user.oauth_id = user_data.get('id')
            user.profile_picture = picture
            db.session.commit()
            
            return {
                'success': True,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.customer.name if hasattr(user, 'customer') else name,
                    'role': user.role,
                    'picture': picture,
                    'provider': provider
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Kullanıcı oluşturma hatası: {str(e)}'}

# Service instance
firebase_auth_service = FirebaseAuthService()

# Routes
@firebase_auth_bp.route('/firebase/login', methods=['POST'])
def firebase_login():
    """Firebase ile giriş"""
    try:
        data = request.get_json()
        id_token = data.get('idToken')
        
        if not id_token:
            return jsonify({'success': False, 'message': 'ID token gerekli'})
        
        result = firebase_auth_service.handle_firebase_login(id_token)
        
        if result['success']:
            # Session oluştur
            session['user_id'] = result['user']['id']
            session['email'] = result['user']['email']
            session['authenticated'] = True
            
            return jsonify(result)
        else:
            return jsonify(result)
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@firebase_auth_bp.route('/auth/<provider>')
def oauth_login(provider):
    """OAuth login başlat"""
    try:
        if provider == 'google':
            auth_url = (
                f"https://accounts.google.com/o/oauth2/v2/auth?"
                f"client_id={OAUTH_PROVIDERS['google']['client_id']}&"
                f"redirect_uri={OAUTH_PROVIDERS['google']['redirect_uri']}&"
                f"response_type=code&"
                f"scope={' '.join(OAUTH_PROVIDERS['google']['scopes'])}&"
                f"access_type=offline"
            )
            return redirect(auth_url)
            
        elif provider == 'facebook':
            auth_url = (
                f"https://www.facebook.com/v18.0/dialog/oauth?"
                f"client_id={OAUTH_PROVIDERS['facebook']['app_id']}&"
                f"redirect_uri={OAUTH_PROVIDERS['facebook']['redirect_uri']}&"
                f"response_type=code&"
                f"scope={' '.join(OAUTH_PROVIDERS['facebook']['scopes'])}"
            )
            return redirect(auth_url)
            
        elif provider == 'github':
            auth_url = (
                f"https://github.com/login/oauth/authorize?"
                f"client_id={OAUTH_PROVIDERS['github']['client_id']}&"
                f"redirect_uri={OAUTH_PROVIDERS['github']['redirect_uri']}&"
                f"scope={' '.join(OAUTH_PROVIDERS['github']['scopes'])}"
            )
            return redirect(auth_url)
            
        else:
            return jsonify({'success': False, 'message': 'Desteklenmeyen sağlayıcı'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@firebase_auth_bp.route('/auth/<provider>/callback')
def oauth_callback(provider):
    """OAuth callback"""
    try:
        code = request.args.get('code')
        error = request.args.get('error')
        
        if error:
            return redirect(f'/register?error={error}')
        
        if not code:
            return redirect('/register?error=no_code')
        
        result = firebase_auth_service.handle_oauth_login(provider, code)
        
        if result['success']:
            # Session oluştur
            session['user_id'] = result['user']['id']
            session['email'] = result['user']['email']
            session['authenticated'] = True
            
            # Onboarding veya dashboard'a yönlendir
            return redirect('/onboarding' if result['user']['role'] in ['artist', 'studio'] else '/dashboard')
        else:
            return redirect(f'/register?error={result["message"]}')
            
    except Exception as e:
        return redirect(f'/register?error={str(e)}')

@firebase_auth_bp.route('/auth/logout')
def oauth_logout():
    """OAuth logout"""
    session.clear()
    return redirect('/')

@firebase_auth_bp.route('/firebase/config')
def firebase_config():
    """Frontend için Firebase config"""
    return jsonify(FirebaseManager.get_firebase_config())
