"""
Multi-language Support System
Çoklu dil desteği için modeller
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Language(db.Model):
    """Desteklenen diller"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)  # tr, en, de
    name = db.Column(db.String(50), nullable=False)  # Türkçe, English, Deutsch
    flag = db.Column(db.String(10))  # 🇹🇷, 🇬🇧, 🇩🇪
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Translation(db.Model):
    """Çeviri tablosu"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(200), nullable=False)  # anahtar kelime
    language_code = db.Column(db.String(5), db.ForeignKey('language.code'), nullable=False)
    value = db.Column(db.Text, nullable=False)  # çevrilmiş metin
    context = db.Column(db.String(100))  # bağlam (navbar, buttons, forms vb.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    language = db.relationship('Language', backref='translations')

class ArtistTranslation(db.Model):
    """Sanatçı çoklu dil bilgileri"""
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    language_code = db.Column(db.String(5), db.ForeignKey('language.code'), nullable=False)
    bio = db.Column(db.Text)
    specialty = db.Column(db.String(200))
    website_title = db.Column(db.String(200))
    about_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    artist = db.relationship('Artist', backref='translations')
    language = db.relationship('Language', backref='artist_translations')

class ServiceTranslation(db.Model):
    """Hizmet çoklu dil bilgileri"""
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    language_code = db.Column(db.String(5), db.ForeignKey('language.code'), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    service = db.relationship('Service', backref='translations')
    language = db.relationship('Language', backref='service_translations')
