"""
Automation System
SMS ve E-posta otomasyonu için modeller
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

class EmailTemplate(db.Model):
    """E-posta şablonları"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    html_content = db.Column(db.Text, nullable=False)
    text_content = db.Column(db.Text)
    variables = db.Column(db.Text)  # JSON formatında değişkenler
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SMSTemplate(db.Model):
    """SMS şablonları"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    variables = db.Column(db.Text)  # JSON formatında değişkenler
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AutomationRule(db.Model):
    """Otomasyon kuralları"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    trigger_event = db.Column(db.String(50), nullable=False)  # appointment_created, appointment_reminder, etc.
    trigger_conditions = db.Column(db.Text)  # JSON formatında koşullar
    actions = db.Column(db.Text, nullable=False)  # JSON formatında aksiyonlar
    is_active = db.Column(db.Boolean, default=True)
    run_count = db.Column(db.Integer, default=0)
    last_run_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EmailLog(db.Model):
    """E-posta gönderim logları"""
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('email_template.id'))
    to_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed, bounced
    sent_at = db.Column(db.DateTime)
    opened_at = db.Column(db.DateTime)
    clicked_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    metadata = db.Column(db.Text)  # JSON formatında ek veriler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    template = db.relationship('EmailTemplate', backref='logs')

class SMSLog(db.Model):
    """SMS gönderim logları"""
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('sms_template.id'))
    to_phone = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed, delivered
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    metadata = db.Column(db.Text)  # JSON formatında ek veriler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    template = db.relationship('SMSTemplate', backref='logs')

class Campaign(db.Model):
    """Pazarlama kampanyaları"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # email, sms, push
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    target_audience = db.Column(db.Text)  # JSON formatında hedef kitle
    scheduled_at = db.Column(db.DateTime)
    sent_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, sending, sent, paused
    total_recipients = db.Column(db.Integer, default=0)
    sent_count = db.Column(db.Integer, default=0)
    opened_count = db.Column(db.Integer, default=0)
    clicked_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CampaignRecipient(db.Model):
    """Kampanya alıcıları"""
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed, opened, clicked
    sent_at = db.Column(db.DateTime)
    opened_at = db.Column(db.DateTime)
    clicked_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    campaign = db.relationship('Campaign', backref='recipients')
    customer = db.relationship('Customer', backref='campaign_recipients')

class NotificationPreference(db.Model):
    """Bildirim tercihleri"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    email_appointment_reminder = db.Column(db.Boolean, default=True)
    email_appointment_confirmation = db.Column(db.Boolean, default=True)
    email_marketing = db.Column(db.Boolean, default=False)
    sms_appointment_reminder = db.Column(db.Boolean, default=True)
    sms_appointment_confirmation = db.Column(db.Boolean, default=True)
    sms_marketing = db.Column(db.Boolean, default=False)
    push_appointment_reminder = db.Column(db.Boolean, default=True)
    push_marketing = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='notification_preferences')
