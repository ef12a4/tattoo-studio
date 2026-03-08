from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tattoo_studio_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tattoo_studio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Firebase Authentication fields
    firebase_uid = db.Column(db.String(128), unique=True)
    oauth_provider = db.Column(db.String(50))  # google, facebook, github, apple, twitter
    oauth_id = db.Column(db.String(128))
    profile_picture = db.Column(db.String(500))

class Studio(db.Model):
    """Stüdyo bilgileri"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    tagline = db.Column(db.String(500))
    description = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    website = db.Column(db.String(200))
    size = db.Column(db.String(20))  # small, medium, large
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='studio')

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    specialty = db.Column(db.String(200))
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    instagram = db.Column(db.String(100))
    portfolio_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointments = db.relationship('Appointment', backref='artist', lazy=True)
    
    user = db.relationship('User', backref='artist')

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointments = db.relationship('Appointment', backref='customer', lazy=True)
    
    user = db.relationship('User', backref='customer')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer) # dakika
    status = db.Column(db.String(20), default='scheduled') # scheduled, completed, cancelled
    deposit_amount = db.Column(db.Float)
    total_price = db.Column(db.Float)
    notes = db.Column(db.Text)
    design_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TattooDesign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    image_url = db.Column(db.String(300))
    category = db.Column(db.String(50))
    style = db.Column(db.String(50))
    estimated_price = db.Column(db.Float)
    estimated_duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudioSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.Text)

class ArtistWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'))
    subdomain = db.Column(db.String(50), unique=True, nullable=False)
    custom_domain = db.Column(db.String(100))
    theme = db.Column(db.String(50), default='default')
    primary_color = db.Column(db.String(7), default='#000000')
    secondary_color = db.Column(db.String(7), default='#ffffff')
    accent_color = db.Column(db.String(7), default='#ff6b6b')
    background_color = db.Column(db.String(7), default='#f8f9fa')
    primary_font = db.Column(db.String(50), default='Roboto')
    background_type = db.Column(db.String(20), default='solid') # solid, gradient, image, video, pattern
    background_url = db.Column(db.String(500))
    animations_enabled = db.Column(db.Boolean, default=True)
    animation_style = db.Column(db.String(20), default='fade')
    logo_url = db.Column(db.String(500))
    logo_size = db.Column(db.Integer, default=40)
    bio_title = db.Column(db.String(200))
    about_text = db.Column(db.Text)
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    instagram_url = db.Column(db.String(200))
    facebook_url = db.Column(db.String(200))
    twitter_url = db.Column(db.String(200))
    youtube_url = db.Column(db.String(200))
    google_analytics_id = db.Column(db.String(50))
    custom_css = db.Column(db.Text)
    page_components = db.Column(db.Text) # JSON formatında bileşenler
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    artist = db.relationship('Artist', backref=db.backref('website', uselist=False))
    studio = db.relationship('Studio', backref=db.backref('artist_website', uselist=False))

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    min_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    duration_minutes = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    artist = db.relationship('Artist', backref='services')

class PublicAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    preferred_date = db.Column(db.Date)
    design_description = db.Column(db.Text)
    budget = db.Column(db.Float)
    size = db.Column(db.String(50))
    placement = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    artist = db.relationship('Artist', backref='public_appointments')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication routes
@app.route('/')
def landing():
    """Ana landing sayfası"""
    return render_template('auth/landing.html')

@app.route('/register')
def register():
    """Kayıt sayfası"""
    return render_template('auth/register.html')

@app.route('/onboarding')
@login_required
def onboarding():
    """Onboarding süreci"""
    return render_template('auth/onboarding.html')

@app.route('/api/v1/register', methods=['POST'])
def api_register():
    """API kayıt endpoint'i"""
    try:
        data = request.get_json()
        
        # Veri validasyonu
        required_fields = ['accountType', 'firstName', 'lastName', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} alanı zorunludur'})
        
        # E-posta kontrolü
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Bu e-posta adresi zaten kullanılıyor'})
        
        # Şifre kontrolü
        if len(data['password']) < 8:
            return jsonify({'success': False, 'message': 'Şifre en az 8 karakter olmalıdır'})
        
        # Yeni kullanıcı oluştur
        user = User(
            username=data['email'].split('@')[0],  # E-postadan username oluştur
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=data['accountType']  # artist, studio, customer
        )
        
        db.session.add(user)
        db.session.flush()  # ID'yi almak için
        
        # Hesap tipine göre ilgili kayıtları oluştur
        if data['accountType'] == 'studio':
            # Stüdyo kaydı
            studio = Studio(
                name=data.get('studioName', f"{data['firstName']} {data['lastName']} Stüdyosu"),
                email=data['email'],
                phone=data.get('phone', ''),
                address=data.get('studioAddress', ''),
                city=data.get('studioCity', ''),
                country=data.get('studioCountry', ''),
                website=data.get('studioWebsite', ''),
                size=data.get('studioSize', 'small'),
                user_id=user.id
            )
            db.session.add(studio)
            
        elif data['accountType'] == 'artist':
            # Sanatçı kaydı
            artist = Artist(
                name=f"{data['firstName']} {data['lastName']}",
                email=data['email'],
                phone=data.get('phone', ''),
                specialty=data.get('specialty', ''),
                experience_years=data.get('experience', 0),
                instagram=data.get('portfolio', ''),
                portfolio_url=data.get('portfolio', ''),
                bio=data.get('bio', ''),
                user_id=user.id
            )
            db.session.add(artist)
            
        elif data['accountType'] == 'customer':
            # Müşteri kaydı
            customer = Customer(
                name=f"{data['firstName']} {data['lastName']}",
                email=data['email'],
                phone=data.get('phone', ''),
                user_id=user.id
            )
            db.session.add(customer)
        
        db.session.commit()
        
        # Otomatik giriş
        login_user(user)
        
        return jsonify({
            'success': True, 
            'message': 'Kayıt başarılı!',
            'redirect': '/onboarding' if data['accountType'] in ['studio', 'artist'] else '/dashboard'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Kayıt hatası: {str(e)}'})

@app.route('/api/v1/onboarding', methods=['POST'])
@login_required
def api_onboarding():
    """Onboarding verilerini kaydet"""
    try:
        data = request.get_json()
        
        # Kullanıcı bilgilerini güncelle
        user = current_user
        
        # Onboarding verilerini kaydet
        if data.get('plan'):
            user.selected_plan = data['plan']
        
        if data.get('studioInfo'):
            studio_info = data['studioInfo']
            # Stüdyo bilgilerini güncelle
            if hasattr(user, 'studio'):
                user.studio.name = studio_info.get('name', user.studio.name)
                user.studio.tagline = studio_info.get('tagline', user.studio.tagline)
                user.studio.description = studio_info.get('description', user.studio.description)
                user.studio.phone = studio_info.get('phone', user.studio.phone)
                user.studio.email = studio_info.get('email', user.studio.email)
                user.studio.address = studio_info.get('address', user.studio.address)
                user.studio.city = studio_info.get('city', user.studio.city)
                user.studio.country = studio_info.get('country', user.studio.country)
        
        if data.get('theme'):
            # Tema ayarlarını kaydet
            if hasattr(user, 'studio') and user.studio.website:
                user.studio.website.theme = data['theme']
        
        if data.get('services'):
            # Hizmetleri kaydet
            services = data['services']
            for service_data in services:
                service = Service(
                    title=service_data.get('name'),
                    description=service_data.get('description', ''),
                    min_price=service_data.get('price', 0),
                    duration_minutes=service_data.get('duration', 60),
                    artist_id=user.artist.id if hasattr(user, 'artist') else None
                )
                db.session.add(service)
        
        if data.get('workingHours'):
            # Çalışma saatlerini kaydet
            working_hours = data['workingHours']
            # Çalışma saatleri modeli oluşturulmalı
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Onboarding tamamlandı!',
            'redirect': '/dashboard'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Onboarding hatası: {str(e)}'})

@app.route('/auth/<provider>')
def auth_provider(provider):
    """OAuth sağlayıcı yönlendirmesi"""
    # Google, Facebook, Apple OAuth implementasyonu
    if provider == 'google':
        # Google OAuth
        return redirect(f"https://accounts.google.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri={request.url_root}auth/google/callback&scope=email profile&response_type=code")
    elif provider == 'facebook':
        # Facebook OAuth
        return redirect(f"https://www.facebook.com/v18.0/dialog/oauth?client_id=YOUR_CLIENT_ID&redirect_uri={request.url_root}auth/facebook/callback&scope=email&response_type=code")
    elif provider == 'apple':
        # Apple Sign In
        return redirect("https://appleid.apple.com/auth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri={request.url_root}auth/apple/callback&scope=name email&response_type=code")

@app.route('/auth/<provider>/callback')
def auth_callback(provider):
    """OAuth callback"""
    # OAuth callback implementasyonu
    # Access token alıp kullanıcı bilgilerini çekmeli
    # Kullanıcıyı sisteme kaydetmeli veya giriş yapmalı
    return redirect('/onboarding')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!')
    
    return render_template('login.html')

@app.route('/payment_gateway')
@login_required
def payment_gateway():
    return render_template('payment_gateway.html')

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics_dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Dashboard istatistikleri
    total_artists = Artist.query.count()
    total_customers = Customer.query.count()
    total_appointments = Appointment.query.count()
    today_appointments = Appointment.query.filter(
        Appointment.date_time >= datetime.now().date(),
        Appointment.date_time < datetime.now().date() + timedelta(days=1)
    ).count()
    
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_artists=total_artists,
                         total_customers=total_customers,
                         total_appointments=total_appointments,
                         today_appointments=today_appointments,
                         recent_appointments=recent_appointments)

@app.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.order_by(Appointment.date_time.desc()).all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def add_appointment():
    if request.method == 'POST':
        appointment = Appointment(
            customer_id=request.form.get('customer_id'),
            artist_id=request.form.get('artist_id'),
            date_time=datetime.strptime(request.form.get('date_time'), '%Y-%m-%d %H:%M'),
            duration=request.form.get('duration'),
            notes=request.form.get('notes'),
            design_description=request.form.get('design_description')
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Randevu başarıyla oluşturuldu!')
        return redirect(url_for('appointments'))
    
    customers = Customer.query.all()
    artists = Artist.query.all()
    return render_template('appointment_form.html', appointment=None, customers=customers, artists=artists)

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'sağlıklı',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/artists')
@login_required
def artists():
    artists = Artist.query.all()
    return render_template('artists.html', artists=artists)

@app.route('/artists/add', methods=['GET', 'POST'])
@login_required
def add_artist():
    if request.method == 'POST':
        artist = Artist(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            specialty=request.form.get('specialty'),
            bio=request.form.get('bio'),
            experience_years=request.form.get('experience_years'),
            instagram=request.form.get('instagram'),
            portfolio_url=request.form.get('portfolio_url')
        )
        db.session.add(artist)
        db.session.commit()
        flash('Sanatçı başarıyla eklendi!')
        return redirect(url_for('artists'))
    
    return render_template('artist_form.html', artist=None)

@app.route('/artists/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_artist(id):
    artist = Artist.query.get_or_404(id)
    
    if request.method == 'POST':
        artist.name = request.form.get('name')
        artist.email = request.form.get('email')
        artist.phone = request.form.get('phone')
        artist.specialty = request.form.get('specialty')
        artist.bio = request.form.get('bio')
        artist.experience_years = request.form.get('experience_years')
        artist.instagram = request.form.get('instagram')
        artist.portfolio_url = request.form.get('portfolio_url')
        artist.is_active = 'is_active' in request.form
        
        db.session.commit()
        flash('Sanatçı bilgileri güncellendi!')
        return redirect(url_for('artists'))
    
    return render_template('artist_form.html', artist=artist)

@app.route('/artists/delete/<int:id>')
@login_required
def delete_artist(id):
    artist = Artist.query.get_or_404(id)
    db.session.delete(artist)
    db.session.commit()
    flash('Sanatçı silindi!')
    return redirect(url_for('artists'))

@app.route('/customers')
@login_required
def customers():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        customer = Customer(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            date_of_birth=datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date() if request.form.get('date_of_birth') else None,
            notes=request.form.get('notes')
        )
        db.session.add(customer)
        db.session.commit()
        flash('Müşteri başarıyla eklendi!')
        return redirect(url_for('customers'))
    
    return render_template('customer_form.html', customer=None)

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date() if request.form.get('date_of_birth') else None
        customer.notes = request.form.get('notes')
        
        db.session.commit()
        flash('Müşteri bilgileri güncellendi!')
        return redirect(url_for('customers'))
    
    return render_template('customer_form.html', customer=customer)

@app.route('/customers/delete/<int:id>')
@login_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Müşteri silindi!')
    return redirect(url_for('customers'))

@app.route('/portfolio')
@login_required
def portfolio():
    designs = TattooDesign.query.order_by(TattooDesign.created_at.desc()).all()
    artists = Artist.query.filter_by(is_active=True).all()
    return render_template('portfolio.html', designs=designs, artists=artists)

@app.route('/portfolio/add', methods=['POST'])
@login_required
def add_design():
    design = TattooDesign(
        title=request.form.get('title'),
        description=request.form.get('description'),
        artist_id=request.form.get('artist_id'),
        image_url=request.form.get('image_url'),
        category=request.form.get('category'),
        style=request.form.get('style'),
        estimated_price=request.form.get('estimated_price'),
        estimated_duration=request.form.get('estimated_duration')
    )
    db.session.add(design)
    db.session.commit()
    flash('Tasarım başarıyla eklendi!')
    return redirect(url_for('portfolio'))

@app.route('/settings')
@login_required
def settings():
    settings = StudioSettings.query.all()
    return render_template('settings.html', settings=settings)

# Sanatçı Web Siteleri
@app.route('/websites')
@login_required
def websites():
    websites = ArtistWebsite.query.all()
    available_artists = Artist.query.filter(~Artist.id.in_([w.artist_id for w in websites])).all()
    return render_template('websites.html', websites=websites, available_artists=available_artists)

@app.route('/websites/builder/<int:id>')
@login_required
def website_builder(id):
    website = ArtistWebsite.query.get_or_404(id)
    return render_template('website_builder.html', website=website, artist=website.artist)

@app.route('/websites/create', methods=['POST'])
@login_required
def create_website():
    website = ArtistWebsite(
        artist_id=request.form.get('artist_id'),
        subdomain=request.form.get('subdomain'),
        custom_domain=request.form.get('custom_domain'),
        theme=request.form.get('theme'),
        primary_color=request.form.get('primary_color'),
        secondary_color=request.form.get('secondary_color'),
        accent_color=request.form.get('accent_color'),
        bio_title=request.form.get('bio_title'),
        about_text=request.form.get('about_text'),
        contact_email=request.form.get('contact_email'),
        contact_phone=request.form.get('contact_phone'),
        instagram_url=request.form.get('instagram_url'),
        facebook_url=request.form.get('facebook_url'),
        twitter_url=request.form.get('twitter_url'),
        google_analytics_id=request.form.get('google_analytics_id')
    )
    db.session.add(website)
    db.session.commit()
    flash('Web sitesi başarıyla oluşturuldu!')
    return redirect(url_for('websites'))

@app.route('/websites/update/<int:id>', methods=['POST'])
@login_required
def update_website(id):
    website = ArtistWebsite.query.get_or_404(id)
    
    # JSON veriyi al
    data = request.get_json()
    
    # Temel ayarları güncelle
    website.theme = data.get('theme', website.theme)
    website.primary_font = data.get('primary_font', website.primary_font)
    website.primary_color = data.get('primary_color', website.primary_color)
    website.secondary_color = data.get('secondary_color', website.secondary_color)
    website.accent_color = data.get('accent_color', website.accent_color)
    website.background_color = data.get('background_color', website.background_color)
    website.background_type = data.get('background_type', website.background_type)
    website.background_url = data.get('background_url', website.background_url)
    website.animations_enabled = data.get('animations_enabled', website.animations_enabled)
    website.animation_style = data.get('animation_style', website.animation_style)
    website.logo_url = data.get('logo_url', website.logo_url)
    website.logo_size = data.get('logo_size', website.logo_size)
    website.custom_css = data.get('custom_css', website.custom_css)
    website.page_components = json.dumps(data.get('components', []))
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Web sitesi güncellendi!'})

@app.route('/websites/toggle/<int:id>')
@login_required
def toggle_website(id):
    website = ArtistWebsite.query.get_or_404(id)
    website.is_active = not website.is_active
    db.session.commit()
    flash('Web sitesi durumu güncellendi!')
    return redirect(url_for('websites'))

# Public Sanatçı Sayfaları
@app.route('/<subdomain>')
def public_artist_page(subdomain):
    website = ArtistWebsite.query.filter_by(subdomain=subdomain, is_active=True).first()
    if not website:
        return "Web sitesi bulunamadı", 404
    
    artist = website.artist
    designs = TattooDesign.query.filter_by(artist_id=artist.id).all()
    services = Service.query.filter_by(artist_id=artist.id, is_active=True).all()
    
    return render_template('public/artist_home.html', 
                         artist=artist, 
                         website=website, 
                         designs=designs, 
                         services=services)

@app.route('/<subdomain>/appointment', methods=['POST'])
def public_appointment(subdomain):
    website = ArtistWebsite.query.filter_by(subdomain=subdomain, is_active=True).first()
    if not website:
        return "Web sitesi bulunamadı", 404
    
    appointment = PublicAppointment(
        artist_id=website.artist_id,
        name=request.form.get('name'),
        email=request.form.get('email'),
        phone=request.form.get('phone'),
        preferred_date=datetime.strptime(request.form.get('preferred_date'), '%Y-%m-%d').date() if request.form.get('preferred_date') else None,
        design_description=request.form.get('design_description'),
        budget=request.form.get('budget'),
        size=request.form.get('size'),
        placement=request.form.get('placement')
    )
    
    db.session.add(appointment)
    db.session.commit()
    
    flash('Randevu talebiniz başarıyla gönderildi! En kısa sürede size dönüş yapacağız.')
    return redirect(f'/{subdomain}#contact')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Varsayılan admin kullanıcısı oluştur
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@tattoostudio.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True)
