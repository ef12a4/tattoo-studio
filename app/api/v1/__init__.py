"""
API v1 Module
RESTful API endpoints
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import *

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Authentication decorator
def api_key_required(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        # API key validation (basit örnek)
        if api_key != 'tattoo_studio_api_key_2024':
            return jsonify({'error': 'Invalid API key'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@api_v1.route('/artists')
@api_key_required
def get_artists():
    """Tüm sanatçıları getir"""
    artists = Artist.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': artist.id,
        'name': artist.name,
        'email': artist.email,
        'specialty': artist.specialty,
        'experience_years': artist.experience_years,
        'instagram': artist.instagram,
        'portfolio_url': artist.portfolio_url
    } for artist in artists])

@api_v1.route('/artists/<int:id>')
@api_key_required
def get_artist(id):
    """Tek sanatçı bilgileri"""
    artist = Artist.query.get_or_404(id)
    return jsonify({
        'id': artist.id,
        'name': artist.name,
        'email': artist.email,
        'phone': artist.phone,
        'specialty': artist.specialty,
        'bio': artist.bio,
        'experience_years': artist.experience_years,
        'instagram': artist.instagram,
        'portfolio_url': artist.portfolio_url,
        'is_active': artist.is_active
    })

@api_v1.route('/appointments')
@api_key_required
def get_appointments():
    """Randevuları getir"""
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    artist_id = request.args.get('artist_id', type=int)
    
    query = Appointment.query
    
    if date_from:
        query = query.filter(Appointment.date_time >= date_from)
    if date_to:
        query = query.filter(Appointment.date_time <= date_to)
    if artist_id:
        query = query.filter(Appointment.artist_id == artist_id)
    
    appointments = query.all()
    return jsonify([{
        'id': apt.id,
        'customer_name': apt.customer.name,
        'artist_name': apt.artist.name,
        'date_time': apt.date_time.isoformat(),
        'duration': apt.duration,
        'status': apt.status,
        'total_price': apt.total_price
    } for apt in appointments])

@api_v1.route('/appointments', methods=['POST'])
@api_key_required
def create_appointment():
    """Yeni randevu oluştur"""
    data = request.get_json()
    
    appointment = Appointment(
        customer_id=data['customer_id'],
        artist_id=data['artist_id'],
        date_time=datetime.fromisoformat(data['date_time']),
        duration=data.get('duration', 120),
        total_price=data.get('total_price'),
        notes=data.get('notes'),
        design_description=data.get('design_description')
    )
    
    db.session.add(appointment)
    db.session.commit()
    
    return jsonify({
        'id': appointment.id,
        'message': 'Appointment created successfully'
    }), 201

@api_v1.route('/customers')
@api_key_required
def get_customers():
    """Müşterileri getir"""
    customers = Customer.query.all()
    return jsonify([{
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'date_of_birth': customer.date_of_birth.isoformat() if customer.date_of_birth else None,
        'created_at': customer.created_at.isoformat()
    } for customer in customers])

@api_v1.route('/customers', methods=['POST'])
@api_key_required
def create_customer():
    """Yeni müşteri oluştur"""
    data = request.get_json()
    
    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        date_of_birth=datetime.fromisoformat(data['date_of_birth']).date() if data.get('date_of_birth') else None,
        notes=data.get('notes')
    )
    
    db.session.add(customer)
    db.session.commit()
    
    return jsonify({
        'id': customer.id,
        'message': 'Customer created successfully'
    }), 201

@api_v1.route('/portfolio')
@api_key_required
def get_portfolio():
    """Portfolyo getir"""
    artist_id = request.args.get('artist_id', type=int)
    
    query = TattooDesign.query
    if artist_id:
        query = query.filter(TattooDesign.artist_id == artist_id)
    
    designs = query.all()
    return jsonify([{
        'id': design.id,
        'title': design.title,
        'description': design.description,
        'artist_name': design.artist.name,
        'category': design.category,
        'style': design.style,
        'estimated_price': design.estimated_price,
        'image_url': design.image_url
    } for design in designs])

@api_v1.route('/revenue')
@api_key_required
def get_revenue():
    """Gelir raporu"""
    period = request.args.get('period', 'monthly')  # daily, weekly, monthly, yearly
    
    # Basit gelir hesaplama
    appointments = Appointment.query.filter_by(status='completed').all()
    total_revenue = sum([apt.total_price or 0 for apt in appointments])
    
    return jsonify({
        'period': period,
        'total_revenue': total_revenue,
        'appointment_count': len(appointments),
        'average_revenue': total_revenue / len(appointments) if appointments else 0
    })

@api_v1.route('/analytics/dashboard')
@api_key_required
def get_dashboard_analytics():
    """Dashboard analitikleri"""
    # Temel istatistikler
    total_artists = Artist.query.count()
    total_customers = Customer.query.count()
    total_appointments = Appointment.query.count()
    completed_appointments = Appointment.query.filter_by(status='completed').count()
    
    # Gelir hesaplama
    revenue = sum([apt.total_price or 0 for apt in Appointment.query.filter_by(status='completed').all()])
    
    return jsonify({
        'total_artists': total_artists,
        'total_customers': total_customers,
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'completion_rate': (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0,
        'total_revenue': revenue,
        'average_appointment_value': revenue / completed_appointments if completed_appointments > 0 else 0
    })

@api_v1.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    """Stripe webhook endpoint"""
    # Stripe webhook işleme
    event = request.get_json()
    
    # Event tipine göre işlem yap
    if event['type'] == 'payment_intent.succeeded':
        # Ödeme başarılı - siparişi güncelle
        pass
    elif event['type'] == 'payment_intent.payment_failed':
        # Ödeme başarısız - siparişi iptal et
        pass
    
    return jsonify({'status': 'success'})

@api_v1.route('/webhooks/iyzico', methods=['POST'])
def iyzico_webhook():
    """Iyzico webhook endpoint"""
    # Iyzico webhook işleme
    event = request.get_json()
    
    # Event tipine göre işlem yap
    if event['eventType'] == 'PAYMENT_SUCCESS':
        # Ödeme başarılı
        pass
    elif event['eventType'] == 'PAYMENT_FAILED':
        # Ödeme başarısız
        pass
    
    return jsonify({'status': 'success'})
