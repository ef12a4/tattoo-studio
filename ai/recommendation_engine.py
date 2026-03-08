"""
AI Recommendation Engine
Sanatçı ve tasarım öneri sistemi
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import json
from datetime import datetime, timedelta

class TattooRecommendationEngine:
    """Dövme öneri motoru"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.artist_features = {}
        self.design_features = {}
        self.customer_preferences = {}
        
    def train_artist_model(self, artists, designs):
        """Sanatçı modelini eğit"""
        artist_data = []
        design_data = []
        
        # Sanatçı özelliklerini çıkar
        for artist in artists:
            features = f"{artist.specialty} {artist.bio} {artist.experience_years}"
            artist_data.append(features)
            
        # Tasarım özelliklerini çıkar
        for design in designs:
            features = f"{design.title} {design.description} {design.category} {design.style}"
            design_data.append(features)
        
        # Vektörleştirme
        if artist_data:
            self.artist_vectors = self.vectorizer.fit_transform(artist_data)
        if design_data:
            self.design_vectors = self.vectorizer.fit_transform(design_data)
            
    def recommend_artists(self, customer_id, limit=5):
        """Müşteri için sanatçı öner"""
        try:
            # Müşteri geçmişini al
            customer_history = self.get_customer_history(customer_id)
            
            if not customer_history:
                # Yeni müşteri için popüler sanatçılar
                return self.get_popular_artists(limit)
            
            # Müşteri tercihlerini analiz et
            preferences = self.analyze_customer_preferences(customer_history)
            
            # Benzer sanatçıları bul
            similar_artists = self.find_similar_artists(preferences, limit)
            
            return similar_artists
            
        except Exception as e:
            print(f"Öneri hatası: {e}")
            return self.get_popular_artists(limit)
    
    def recommend_designs(self, customer_id, artist_id=None, limit=10):
        """Müşteri için tasarım öner"""
        try:
            # Müşteri geçmişini al
            customer_history = self.get_customer_history(customer_id)
            
            # Sanatçı filtresi
            if artist_id:
                designs = self.get_artist_designs(artist_id)
            else:
                designs = self.get_all_designs()
            
            # Müşteri tercihlerini analiz et
            preferences = self.analyze_customer_preferences(customer_history)
            
            # Benzer tasarımları bul
            similar_designs = self.find_similar_designs(preferences, designs, limit)
            
            return similar_designs
            
        except Exception as e:
            print(f"Tasarım öneri hatası: {e}")
            return self.get_popular_designs(limit)
    
    def get_customer_history(self, customer_id):
        """Müşteri geçmişini getir"""
        # Veritabanından müşteri geçmişini al
        # Bu fonksiyon gerçek uygulamada veritabanı sorgusu yapar
        return []
    
    def analyze_customer_preferences(self, history):
        """Müşteri tercihlerini analiz et"""
        preferences = {
            'styles': [],
            'categories': [],
            'artists': [],
            'price_range': {'min': 0, 'max': 10000},
            'duration_range': {'min': 30, 'max': 480}
        }
        
        # Geçmiş randevulardan tercihleri çıkar
        for appointment in history:
            if appointment.design:
                if appointment.design.style:
                    preferences['styles'].append(appointment.design.style)
                if appointment.design.category:
                    preferences['categories'].append(appointment.design.category)
            
            if appointment.artist_id:
                preferences['artists'].append(appointment.artist_id)
                
            if appointment.total_price:
                preferences['price_range']['max'] = max(preferences['price_range']['max'], appointment.total_price)
                
            if appointment.duration:
                preferences['duration_range']['max'] = max(preferences['duration_range']['max'], appointment.duration)
        
        return preferences
    
    def find_similar_artists(self, preferences, limit):
        """Benzer sanatçıları bul"""
        # Tercihlere göre sanatçıları puanla
        artist_scores = {}
        
        # Stil bazında puanlama
        for style in preferences['styles']:
            matching_artists = self.get_artists_by_style(style)
            for artist in matching_artists:
                artist_scores[artist.id] = artist_scores.get(artist.id, 0) + 1
        
        # Kategori bazında puanlama
        for category in preferences['categories']:
            matching_artists = self.get_artists_by_category(category)
            for artist in matching_artists:
                artist_scores[artist.id] = artist_scores.get(artist.id, 0) + 1
        
        # En yüksek puanlı sanatçıları sırala
        sorted_artists = sorted(artist_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [artist_id for artist_id, score in sorted_artists[:limit]]
    
    def find_similar_designs(self, preferences, designs, limit):
        """Benzer tasarımları bul"""
        design_scores = {}
        
        for design in designs:
            score = 0
            
            # Stil eşleşmesi
            if design.style in preferences['styles']:
                score += 2
            
            # Kategori eşleşmesi
            if design.category in preferences['categories']:
                score += 2
            
            # Fiyat aralığı
            if design.estimated_price:
                if preferences['price_range']['min'] <= design.estimated_price <= preferences['price_range']['max']:
                    score += 1
            
            # Süre aralığı
            if design.estimated_duration:
                if preferences['duration_range']['min'] <= design.estimated_duration <= preferences['duration_range']['max']:
                    score += 1
            
            design_scores[design.id] = score
        
        # En yüksek puanlı tasarımları sırala
        sorted_designs = sorted(design_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [design_id for design_id, score in sorted_designs[:limit]]
    
    def get_popular_artists(self, limit):
        """Popüler sanatçıları getir"""
        # En çok randevu alan sanatçılar
        return []
    
    def get_popular_designs(self, limit):
        """Popüler tasarımları getir"""
        # En çok beğenilen tasarımlar
        return []
    
    def get_artists_by_style(self, style):
        """Stile göre sanatçıları getir"""
        # Veritabanından stil bazında sorgu
        return []
    
    def get_artists_by_category(self, category):
        """Kategoriye göre sanatçıları getir"""
        # Veritabanından kategori bazında sorgu
        return []
    
    def get_artist_designs(self, artist_id):
        """Sanatçının tasarımlarını getir"""
        # Veritabanından sanatçı tasarımları
        return []
    
    def get_all_designs(self):
        """Tüm tasarımları getir"""
        # Veritabanından tüm tasarımlar
        return []

class CustomerSegmentation:
    """Müşteri segmentasyonu"""
    
    def __init__(self):
        self.segments = {
            'new_customers': {
                'criteria': 'visits <= 1',
                'characteristics': ['price_sensitive', 'exploring'],
                'marketing_focus': ['introductory_offers', 'educational_content']
            },
            'regular_customers': {
                'criteria': '2 <= visits <= 5',
                'characteristics': ['loyal', 'moderate_spending'],
                'marketing_focus': ['loyalty_programs', 'referral_bonuses']
            },
            'vip_customers': {
                'criteria': 'visits > 5 AND total_spending > 5000',
                'characteristics': ['high_spending', 'brand_advocates'],
                'marketing_focus': ['exclusive_offers', 'early_access', 'personal_service']
            },
            'at_risk_customers': {
                'criteria': 'last_visit > 90_days',
                'characteristics': ['churn_risk', 'reengagement_needed'],
                'marketing_focus': ['win_back_campaigns', 'special_offers']
            }
        }
    
    def segment_customers(self, customers):
        """Müşterileri segmentlere ayır"""
        segmented_customers = {}
        
        for segment_name, segment_info in self.segments.items():
            segmented_customers[segment_name] = []
        
        for customer in customers:
            segment = self.determine_segment(customer)
            if segment:
                segmented_customers[segment].append(customer)
        
        return segmented_customers
    
    def determine_segment(self, customer):
        """Müşteri segmentini belirle"""
        # VIP müşteri kontrolü
        if (customer.total_visits > 5 and 
            customer.total_spending > 5000 and 
            customer.last_visit_days_ago <= 90):
            return 'vip_customers'
        
        # Riskli müşteri kontrolü
        elif customer.last_visit_days_ago > 90:
            return 'at_risk_customers'
        
        # Düzenli müşteri kontrolü
        elif 2 <= customer.total_visits <= 5:
            return 'regular_customers'
        
        # Yeni müşteri
        elif customer.total_visits <= 1:
            return 'new_customers'
        
        return None

class TrendAnalyzer:
    """Trend analizi"""
    
    def __init__(self):
        self.trends = {}
        
    def analyze_style_trends(self, designs, period='month'):
        """Stil trendlerini analiz et"""
        style_counts = {}
        
        for design in designs:
            style = design.style or 'other'
            if style not in style_counts:
                style_counts[style] = 0
            style_counts[style] += 1
        
        # Trendleri hesapla
        total_designs = len(designs)
        style_trends = {}
        
        for style, count in style_counts.items():
            percentage = (count / total_designs) * 100
            style_trends[style] = {
                'count': count,
                'percentage': percentage,
                'trend': self.calculate_trend(style, period)
            }
        
        return style_trends
    
    def calculate_trend(self, style, period):
        """Trend yönünü hesapla"""
        # Basit trend hesaplama
        # Gerçek uygulamada geçmiş verilerle karşılaştırma yapılır
        return 'stable'
    
    def predict_popular_styles(self, current_trends, forecast_period=3):
        """Popüler stilleri tahmin et"""
        # Basit tahmin algoritması
        predicted_styles = []
        
        for style, trend_data in current_trends.items():
            if trend_data['trend'] == 'up' and trend_data['percentage'] > 5:
                predicted_styles.append({
                    'style': style,
                    'predicted_growth': trend_data['percentage'] * 1.2,
                    'confidence': 0.75
                })
        
        return sorted(predicted_styles, key=lambda x: x['predicted_growth'], reverse=True)

# AI motorunu başlat
recommendation_engine = TattooRecommendationEngine()
customer_segmentation = CustomerSegmentation()
trend_analyzer = TrendAnalyzer()
