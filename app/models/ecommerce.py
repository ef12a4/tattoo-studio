"""
E-commerce System
Online dövme ürün satışı için modeller
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Product(db.Model):
    """Ürünler (dövme kitleri, aletler, mürekkep vb.)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(500))
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    compare_price = db.Column(db.Float)
    cost_price = db.Column(db.Float)
    weight = db.Column(db.Float)
    dimensions = db.Column(db.String(100))  # "10x5x2 cm"
    track_inventory = db.Column(db.Boolean, default=True)
    inventory_quantity = db.Column(db.Integer, default=0)
    inventory_policy = db.Column(db.String(20), default='deny')  # deny, continue
    requires_shipping = db.Column(db.Boolean, default=True)
    taxable = db.Column(db.Boolean, default=True)
    tax_rate = db.Column(db.Float, default=0.18)  # %18 KDV
    status = db.Column(db.String(20), default='active')  # active, draft, archived
    featured = db.Column(db.Boolean, default=False)
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    
    category = db.relationship('ProductCategory', backref='products')
    artist = db.relationship('Artist', backref='products')
    vendor = db.relationship('Vendor', backref='products')
    images = db.relationship('ProductImage', backref='product', lazy='dynamic')
    variants = db.relationship('ProductVariant', backref='product', lazy='dynamic')

class ProductCategory(db.Model):
    """Ürün kategorileri"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.String(500))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    parent = db.relationship('ProductCategory', remote_side=[id], backref='children')

class ProductImage(db.Model):
    """Ürün resimleri"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProductVariant(db.Model):
    """Ürün varyasyonları (renk, boyut vb.)"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)  # "Siyah - Küçük"
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    compare_price = db.Column(db.Float)
    inventory_quantity = db.Column(db.Integer, default=0)
    requires_shipping = db.Column(db.Boolean, default=True)
    taxable = db.Column(db.Boolean, default=True)
    weight = db.Column(db.Float)
    option1 = db.Column(db.String(50))  # Renk
    option2 = db.Column(db.String(50))  # Boyut
    option3 = db.Column(db.String(50))  # Malzeme
    position = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Vendor(db.Model):
    """Tedarikçiler"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(500))
    address = db.Column(db.Text)
    commission_rate = db.Column(db.Float, default=0.10)  # %10 komisyon
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    """Siparişler"""
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, processing, shipped, delivered, cancelled
    financial_status = db.Column(db.String(20), default='pending')  # pending, paid, partially_paid, refunded
    fulfillment_status = db.Column(db.String(20), default='unfulfilled')  # unfulfilled, partial, fulfilled
    currency = db.Column(db.String(3), default='TRY')
    subtotal_price = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0)
    shipping_amount = db.Column(db.Float, default=0)
    total_price = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    shipping_address = db.Column(db.Text)  # JSON formatında
    billing_address = db.Column(db.Text)   # JSON formatında
    tracking_number = db.Column(db.String(100))
    tracking_url = db.Column(db.String(500))
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

class OrderItem(db.Model):
    """Sipariş kalemleri"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    product_title = db.Column(db.String(200), nullable=False)
    variant_title = db.Column(db.String(200))
    sku = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product')
    variant = db.relationship('ProductVariant')

class Cart(db.Model):
    """Sepet"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    session_id = db.Column(db.String(100))  # Misafir kullanıcılar için
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='carts')
    items = db.relationship('CartItem', backref='cart', lazy='dynamic')

class CartItem(db.Model):
    """Sepet kalemleri"""
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product')
    variant = db.relationship('ProductVariant')

class Coupon(db.Model):
    """Kupon kodları"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    type = db.Column(db.String(20), default='percentage')  # percentage, fixed_amount
    value = db.Column(db.Float, nullable=False)
    minimum_amount = db.Column(db.Float)
    usage_limit = db.Column(db.Integer)
    used_count = db.Column(db.Integer, default=0)
    starts_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    """Ödemeler"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    gateway = db.Column(db.String(50), nullable=False)  # stripe, paypal, iyzico
    transaction_id = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='TRY')
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    gateway_response = db.Column(db.Text)  # JSON formatında gateway yanıtı
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order = db.relationship('Order', backref='payments')
