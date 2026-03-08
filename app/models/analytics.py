"""
Analytics System
Finansal analiz ve raporlama için modeller
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

class RevenueReport(db.Model):
    """Gelir raporları"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    period_type = db.Column(db.String(10), nullable=False)  # daily, weekly, monthly, yearly
    total_revenue = db.Column(db.Float, default=0)
    appointment_revenue = db.Column(db.Float, default=0)
    product_revenue = db.Column(db.Float, default=0)
    service_revenue = db.Column(db.Float, default=0)
    commission_amount = db.Column(db.Float, default=0)
    tax_amount = db.Column(db.Float, default=0)
    net_revenue = db.Column(db.Float, default=0)
    appointment_count = db.Column(db.Integer, default=0)
    product_count = db.Column(db.Integer, default=0)
    customer_count = db.Column(db.Integer, default=0)
    new_customer_count = db.Column(db.Integer, default=0)
    average_order_value = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ArtistPerformance(db.Model):
    """Sanatçı performans analizi"""
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    period_type = db.Column(db.String(10), nullable=False)  # daily, weekly, monthly
    total_revenue = db.Column(db.Float, default=0)
    appointment_count = db.Column(db.Integer, default=0)
    completed_appointments = db.Column(db.Integer, default=0)
    cancelled_appointments = db.Column(db.Integer, default=0)
    no_show_rate = db.Column(db.Float, default=0)
    average_session_price = db.Column(db.Float, default=0)
    average_session_duration = db.Column(db.Float, default=0)
    customer_satisfaction = db.Column(db.Float)  # 1-5 arası
    new_customers = db.Column(db.Integer, default=0)
    returning_customers = db.Column(db.Integer, default=0)
    utilization_rate = db.Column(db.Float, default=0)  # Zaman kullanım oranı
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    artist = db.relationship('Artist', backref='performance_reports')

class CustomerAnalytics(db.Model):
    """Müşteri analitikleri"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    first_visit_date = db.Column(db.Date)
    last_visit_date = db.Column(db.Date)
    total_visits = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Float, default=0)
    average_visit_value = db.Column(db.Float, default=0)
    favorite_artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    preferred_services = db.Column(db.Text)  # JSON formatında
    visit_frequency = db.Column(db.String(20))  # weekly, monthly, quarterly, yearly
    loyalty_score = db.Column(db.Float, default=0)  # 1-100 arası
    churn_risk = db.Column(db.String(10))  # low, medium, high
    lifetime_value = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='analytics')
    favorite_artist = db.relationship('Artist', backref='favorite_customers')

class WebsiteAnalytics(db.Model):
    """Web sitesi analitikleri"""
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('artist_website.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    page_views = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    sessions = db.Column(db.Integer, default=0)
    bounce_rate = db.Column(db.Float, default=0)
    average_session_duration = db.Column(db.Float, default=0)
    appointment_requests = db.Column(db.Integer, default=0)
    contact_form_submissions = db.Column(db.Integer, default=0)
    conversion_rate = db.Column(db.Float, default=0)
    top_pages = db.Column(db.Text)  # JSON formatında
    traffic_sources = db.Column(db.Text)  # JSON formatında
    device_breakdown = db.Column(db.Text)  # JSON formatında
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    website = db.relationship('ArtistWebsite', backref='analytics')

class FinancialMetrics(db.Model):
    """Finansal metrikler"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    period_type = db.Column(db.String(10), nullable=False)  # daily, weekly, monthly
    gross_revenue = db.Column(db.Float, default=0)
    net_revenue = db.Column(db.Float, default=0)
    gross_profit = db.Column(db.Float, default=0)
    net_profit = db.Column(db.Float, default=0)
    profit_margin = db.Column(db.Float, default=0)
    operating_expenses = db.Column(db.Float, default=0)
    marketing_expenses = db.Column(db.Float, default=0)
    staff_expenses = db.Column(db.Float, default=0)
    rent_expenses = db.Column(db.Float, default=0)
    other_expenses = db.Column(db.Float, default=0)
    cash_flow = db.Column(db.Float, default=0)
    accounts_receivable = db.Column(db.Float, default=0)
    accounts_payable = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ConversionFunnel(db.Model):
    """Dönüşüm hunisi analizi"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    website_visitors = db.Column(db.Integer, default=0)
    portfolio_views = db.Column(db.Integer, default=0)
    contact_form_views = db.Column(db.Integer, default=0)
    contact_submissions = db.Column(db.Integer, default=0)
    appointment_requests = db.Column(db.Integer, default=0)
    confirmed_appointments = db.Column(db.Integer, default=0)
    completed_appointments = db.Column(db.Integer, default=0)
    visitor_to_lead_rate = db.Column(db.Float, default=0)
    lead_to_appointment_rate = db.Column(db.Float, default=0)
    appointment_to_completion_rate = db.Column(db.Float, default=0)
    overall_conversion_rate = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PopularServices(db.Model):
    """Popüler hizmetler analizi"""
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    period_type = db.Column(db.String(10), nullable=False)  # daily, weekly, monthly
    booking_count = db.Column(db.Integer, default=0)
    revenue = db.Column(db.Float, default=0)
    average_price = db.Column(db.Float, default=0)
    completion_rate = db.Column(db.Float, default=0)
    customer_satisfaction = db.Column(db.Float, default=0)
    popularity_score = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    service = db.relationship('Service', backref='popularity_reports')

class TrendAnalysis(db.Model):
    """Trend analizi"""
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    change_percentage = db.Column(db.Float, default=0)
    trend_direction = db.Column(db.String(10))  # up, down, stable
    forecast_value = db.Column(db.Float)
    confidence_level = db.Column(db.Float)  # 0-1 arası
    seasonality_factor = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
