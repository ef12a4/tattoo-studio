#!/usr/bin/env python3
"""
Veritabanı şemasını güncelleme script'i
Yeni alanları mevcut tablolara ekler
"""

from app import app, db
from datetime import datetime

def update_artist_website_table():
    """ArtistWebsite tablosunu güncelle"""
    print("ArtistWebsite tablosu güncelleniyor...")
    
    try:
        # Yeni alanları ekle
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN background_color VARCHAR(7) DEFAULT '#f8f9fa'
        """)
        print("✓ background_color alanı eklendi")
    except Exception as e:
        print(f"- background_color zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN primary_font VARCHAR(50) DEFAULT 'Roboto'
        """)
        print("✓ primary_font alanı eklendi")
    except Exception as e:
        print(f"- primary_font zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN background_type VARCHAR(20) DEFAULT 'solid'
        """)
        print("✓ background_type alanı eklendi")
    except Exception as e:
        print(f"- background_type zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN background_url VARCHAR(500)
        """)
        print("✓ background_url alanı eklendi")
    except Exception as e:
        print(f"- background_url zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN animations_enabled BOOLEAN DEFAULT 1
        """)
        print("✓ animations_enabled alanı eklendi")
    except Exception as e:
        print(f"- animations_enabled zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN animation_style VARCHAR(20) DEFAULT 'fade'
        """)
        print("✓ animation_style alanı eklendi")
    except Exception as e:
        print(f"- animation_style zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN logo_url VARCHAR(500)
        """)
        print("✓ logo_url alanı eklendi")
    except Exception as e:
        print(f"- logo_url zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN logo_size INTEGER DEFAULT 40
        """)
        print("✓ logo_size alanı eklendi")
    except Exception as e:
        print(f"- logo_size zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN custom_css TEXT
        """)
        print("✓ custom_css alanı eklendi")
    except Exception as e:
        print(f"- custom_css zaten mevcut: {e}")
    
    try:
        db.session.execute("""
            ALTER TABLE artist_website 
            ADD COLUMN page_components TEXT
        """)
        print("✓ page_components alanı eklendi")
    except Exception as e:
        print(f"- page_components zaten mevcut: {e}")
    
    db.session.commit()
    print("ArtistWebsite tablosu basariyla guncellendi!")

def create_new_tables():
    """Yeni tabloları oluştur"""
    print("Yeni tablolar olusturuluyor...")
    
    # Language tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS language (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code VARCHAR(5) UNIQUE NOT NULL,
                name VARCHAR(50) NOT NULL,
                flag VARCHAR(10),
                is_active BOOLEAN DEFAULT 1,
                is_default BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ language tablosu olusturuldu")
    except Exception as e:
        print(f"- language tablosu zaten mevcut: {e}")
    
    # Translation tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS translation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key VARCHAR(200) NOT NULL,
                language_code VARCHAR(5) NOT NULL,
                value TEXT NOT NULL,
                context VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (language_code) REFERENCES language (code)
            )
        """)
        print("+ translation tablosu olusturuldu")
    except Exception as e:
        print(f"- translation tablosu zaten mevcut: {e}")
    
    # Product tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                slug VARCHAR(200) UNIQUE NOT NULL,
                description TEXT,
                short_description VARCHAR(500),
                sku VARCHAR(50) UNIQUE NOT NULL,
                price REAL NOT NULL,
                compare_price REAL,
                cost_price REAL,
                weight REAL,
                dimensions VARCHAR(100),
                track_inventory BOOLEAN DEFAULT 1,
                inventory_quantity INTEGER DEFAULT 0,
                inventory_policy VARCHAR(20) DEFAULT 'deny',
                requires_shipping BOOLEAN DEFAULT 1,
                taxable BOOLEAN DEFAULT 1,
                tax_rate REAL DEFAULT 0.18,
                status VARCHAR(20) DEFAULT 'active',
                featured BOOLEAN DEFAULT 0,
                seo_title VARCHAR(200),
                seo_description VARCHAR(500),
                category_id INTEGER,
                artist_id INTEGER,
                vendor_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artist (id)
            )
        """)
        print("+ product tablosu olusturuldu")
    except Exception as e:
        print(f"- product tablosu zaten mevcut: {e}")
    
    # ProductCategory tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS product_category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                slug VARCHAR(100) UNIQUE NOT NULL,
                description TEXT,
                image_url VARCHAR(500),
                seo_title VARCHAR(200),
                seo_description VARCHAR(500),
                sort_order INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                parent_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES product_category (id)
            )
        """)
        print("+ product_category tablosu olusturuldu")
    except Exception as e:
        print(f"- product_category tablosu zaten mevcut: {e}")
    
    # ProductImage tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS product_image (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                image_url VARCHAR(500) NOT NULL,
                alt_text VARCHAR(200),
                sort_order INTEGER DEFAULT 0,
                is_featured BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES product (id)
            )
        """)
        print("+ product_image tablosu olusturuldu")
    except Exception as e:
        print(f"- product_image tablosu zaten mevcut: {e}")
    
    # Order tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS "order" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number VARCHAR(50) UNIQUE NOT NULL,
                customer_id INTEGER NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                financial_status VARCHAR(20) DEFAULT 'pending',
                fulfillment_status VARCHAR(20) DEFAULT 'unfulfilled',
                currency VARCHAR(3) DEFAULT 'TRY',
                subtotal_price REAL NOT NULL,
                tax_amount REAL DEFAULT 0,
                shipping_amount REAL DEFAULT 0,
                total_price REAL NOT NULL,
                discount_amount REAL DEFAULT 0,
                notes TEXT,
                shipping_address TEXT,
                billing_address TEXT,
                tracking_number VARCHAR(100),
                tracking_url VARCHAR(500),
                shipped_at DATETIME,
                delivered_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customer (id)
            )
        """)
        print("+ order tablosu olusturuldu")
    except Exception as e:
        print(f"- order tablosu zaten mevcut: {e}")
    
    # OrderItem tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS order_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                variant_id INTEGER,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,
                product_title VARCHAR(200) NOT NULL,
                variant_title VARCHAR(200),
                sku VARCHAR(50) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES "order" (id),
                FOREIGN KEY (product_id) REFERENCES product (id)
            )
        """)
        print("+ order_item tablosu olusturuldu")
    except Exception as e:
        print(f"- order_item tablosu zaten mevcut: {e}")
    
    # EmailTemplate tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS email_template (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                subject VARCHAR(200) NOT NULL,
                html_content TEXT NOT NULL,
                text_content TEXT,
                variables TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ email_template tablosu olusturuldu")
    except Exception as e:
        print(f"- email_template tablosu zaten mevcut: {e}")
    
    # SMSTemplate tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS sms_template (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                content VARCHAR(500) NOT NULL,
                variables TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ sms_template tablosu olusturuldu")
    except Exception as e:
        print(f"- sms_template tablosu zaten mevcut: {e}")
    
    # AutomationRule tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS automation_rule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                trigger_event VARCHAR(50) NOT NULL,
                trigger_conditions TEXT,
                actions TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                run_count INTEGER DEFAULT 0,
                last_run_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ automation_rule tablosu olusturuldu")
    except Exception as e:
        print(f"- automation_rule tablosu zaten mevcut: {e}")
    
    # EmailLog tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS email_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id INTEGER,
                to_email VARCHAR(120) NOT NULL,
                subject VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                sent_at DATETIME,
                opened_at DATETIME,
                clicked_at DATETIME,
                error_message TEXT,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (template_id) REFERENCES email_template (id)
            )
        """)
        print("+ email_log tablosu olusturuldu")
    except Exception as e:
        print(f"- email_log tablosu zaten mevcut: {e}")
    
    # SMSLog tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS sms_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id INTEGER,
                to_phone VARCHAR(20) NOT NULL,
                content VARCHAR(500) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                sent_at DATETIME,
                delivered_at DATETIME,
                error_message TEXT,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (template_id) REFERENCES sms_template (id)
            )
        """)
        print("+ sms_log tablosu olusturuldu")
    except Exception as e:
        print(f"- sms_log tablosu zaten mevcut: {e}")
    
    # Campaign tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS campaign (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(20) NOT NULL,
                subject VARCHAR(200),
                content TEXT NOT NULL,
                target_audience TEXT,
                scheduled_at DATETIME,
                sent_at DATETIME,
                status VARCHAR(20) DEFAULT 'draft',
                total_recipients INTEGER DEFAULT 0,
                sent_count INTEGER DEFAULT 0,
                opened_count INTEGER DEFAULT 0,
                clicked_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ campaign tablosu olusturuldu")
    except Exception as e:
        print(f"- campaign tablosu zaten mevcut: {e}")
    
    # CampaignRecipient tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS campaign_recipient (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                email VARCHAR(120),
                phone VARCHAR(20),
                status VARCHAR(20) DEFAULT 'pending',
                sent_at DATETIME,
                opened_at DATETIME,
                clicked_at DATETIME,
                error_message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaign (id),
                FOREIGN KEY (customer_id) REFERENCES customer (id)
            )
        """)
        print("+ campaign_recipient tablosu olusturuldu")
    except Exception as e:
        print(f"- campaign_recipient tablosu zaten mevcut: {e}")
    
    # NotificationPreference tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS notification_preference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                email_appointment_reminder BOOLEAN DEFAULT 1,
                email_appointment_confirmation BOOLEAN DEFAULT 1,
                email_marketing BOOLEAN DEFAULT 0,
                sms_appointment_reminder BOOLEAN DEFAULT 1,
                sms_appointment_confirmation BOOLEAN DEFAULT 1,
                sms_marketing BOOLEAN DEFAULT 0,
                push_appointment_reminder BOOLEAN DEFAULT 1,
                push_marketing BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customer (id)
            )
        """)
        print("+ notification_preference tablosu olusturuldu")
    except Exception as e:
        print(f"- notification_preference tablosu zaten mevcut: {e}")
    
    # RevenueReport tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS revenue_report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                period_type VARCHAR(10) NOT NULL,
                total_revenue REAL DEFAULT 0,
                appointment_revenue REAL DEFAULT 0,
                product_revenue REAL DEFAULT 0,
                service_revenue REAL DEFAULT 0,
                commission_amount REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                net_revenue REAL DEFAULT 0,
                appointment_count INTEGER DEFAULT 0,
                product_count INTEGER DEFAULT 0,
                customer_count INTEGER DEFAULT 0,
                new_customer_count INTEGER DEFAULT 0,
                average_order_value REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ revenue_report tablosu olusturuldu")
    except Exception as e:
        print(f"- revenue_report tablosu zaten mevcut: {e}")
    
    # ArtistPerformance tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS artist_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist_id INTEGER NOT NULL,
                date DATE NOT NULL,
                period_type VARCHAR(10) NOT NULL,
                total_revenue REAL DEFAULT 0,
                appointment_count INTEGER DEFAULT 0,
                completed_appointments INTEGER DEFAULT 0,
                cancelled_appointments INTEGER DEFAULT 0,
                no_show_rate REAL DEFAULT 0,
                average_session_price REAL DEFAULT 0,
                average_session_duration REAL DEFAULT 0,
                customer_satisfaction REAL,
                new_customers INTEGER DEFAULT 0,
                returning_customers INTEGER DEFAULT 0,
                utilization_rate REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artist (id)
            )
        """)
        print("+ artist_performance tablosu olusturuldu")
    except Exception as e:
        print(f"- artist_performance tablosu zaten mevcut: {e}")
    
    # CustomerAnalytics tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS customer_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                first_visit_date DATE,
                last_visit_date DATE,
                total_visits INTEGER DEFAULT 0,
                total_revenue REAL DEFAULT 0,
                average_visit_value REAL DEFAULT 0,
                favorite_artist_id INTEGER,
                preferred_services TEXT,
                visit_frequency VARCHAR(20),
                loyalty_score REAL DEFAULT 0,
                churn_risk VARCHAR(10),
                lifetime_value REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customer (id),
                FOREIGN KEY (favorite_artist_id) REFERENCES artist (id)
            )
        """)
        print("+ customer_analytics tablosu olusturuldu")
    except Exception as e:
        print(f"- customer_analytics tablosu zaten mevcut: {e}")
    
    # WebsiteAnalytics tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS website_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_id INTEGER NOT NULL,
                date DATE NOT NULL,
                page_views INTEGER DEFAULT 0,
                unique_visitors INTEGER DEFAULT 0,
                sessions INTEGER DEFAULT 0,
                bounce_rate REAL DEFAULT 0,
                average_session_duration REAL DEFAULT 0,
                appointment_requests INTEGER DEFAULT 0,
                contact_form_submissions INTEGER DEFAULT 0,
                conversion_rate REAL DEFAULT 0,
                top_pages TEXT,
                traffic_sources TEXT,
                device_breakdown TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (website_id) REFERENCES artist_website (id)
            )
        """)
        print("+ website_analytics tablosu olusturuldu")
    except Exception as e:
        print(f"- website_analytics tablosu zaten mevcut: {e}")
    
    # FinancialMetrics tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS financial_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                period_type VARCHAR(10) NOT NULL,
                gross_revenue REAL DEFAULT 0,
                net_revenue REAL DEFAULT 0,
                gross_profit REAL DEFAULT 0,
                net_profit REAL DEFAULT 0,
                profit_margin REAL DEFAULT 0,
                operating_expenses REAL DEFAULT 0,
                marketing_expenses REAL DEFAULT 0,
                staff_expenses REAL DEFAULT 0,
                rent_expenses REAL DEFAULT 0,
                other_expenses REAL DEFAULT 0,
                cash_flow REAL DEFAULT 0,
                accounts_receivable REAL DEFAULT 0,
                accounts_payable REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ financial_metrics tablosu olusturuldu")
    except Exception as e:
        print(f"- financial_metrics tablosu zaten mevcut: {e}")
    
    # ConversionFunnel tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS conversion_funnel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                website_visitors INTEGER DEFAULT 0,
                portfolio_views INTEGER DEFAULT 0,
                contact_form_views INTEGER DEFAULT 0,
                contact_submissions INTEGER DEFAULT 0,
                appointment_requests INTEGER DEFAULT 0,
                confirmed_appointments INTEGER DEFAULT 0,
                completed_appointments INTEGER DEFAULT 0,
                visitor_to_lead_rate REAL DEFAULT 0,
                lead_to_appointment_rate REAL DEFAULT 0,
                appointment_to_completion_rate REAL DEFAULT 0,
                overall_conversion_rate REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ conversion_funnel tablosu olusturuldu")
    except Exception as e:
        print(f"- conversion_funnel tablosu zaten mevcut: {e}")
    
    # PopularServices tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS popular_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_id INTEGER NOT NULL,
                date DATE NOT NULL,
                period_type VARCHAR(10) NOT NULL,
                booking_count INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0,
                average_price REAL DEFAULT 0,
                completion_rate REAL DEFAULT 0,
                customer_satisfaction REAL DEFAULT 0,
                popularity_score REAL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (service_id) REFERENCES service (id)
            )
        """)
        print("+ popular_services tablosu olusturuldu")
    except Exception as e:
        print(f"- popular_services tablosu zaten mevcut: {e}")
    
    # TrendAnalysis tablosu
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS trend_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name VARCHAR(50) NOT NULL,
                date DATE NOT NULL,
                value REAL NOT NULL,
                change_percentage REAL DEFAULT 0,
                trend_direction VARCHAR(10),
                forecast_value REAL,
                confidence_level REAL,
                seasonality_factor REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("+ trend_analysis tablosu olusturuldu")
    except Exception as e:
        print(f"- trend_analysis tablosu zaten mevcut: {e}")
    
    db.session.commit()
    print("Yeni tablolar basariyla olusturuldu!")

def insert_sample_data():
    """Örnek veriler ekle"""
    print("Ornek veriler ekleniyor...")
    
    # Dil verileri
    try:
        db.session.execute("""
            INSERT OR IGNORE INTO language (code, name, flag, is_default) VALUES 
            ('tr', 'Türkçe', '🇹🇷', 1),
            ('en', 'English', '🇬🇧', 0),
            ('de', 'Deutsch', '🇩🇪', 0)
        """)
        print("+ Dil verileri eklendi")
    except Exception as e:
        print(f"- Dil verileri zaten mevcut: {e}")
    
    # Çeviri verileri
    try:
        translations = [
            ('tr', 'dashboard', 'Dashboard', 'navigation'),
            ('tr', 'artists', 'Sanatçılar', 'navigation'),
            ('tr', 'appointments', 'Randevular', 'navigation'),
            ('tr', 'customers', 'Müşteriler', 'navigation'),
            ('tr', 'portfolio', 'Portfolyo', 'navigation'),
            ('tr', 'websites', 'Web Siteleri', 'navigation'),
            ('tr', 'settings', 'Ayarlar', 'navigation'),
            ('en', 'dashboard', 'Dashboard', 'navigation'),
            ('en', 'artists', 'Artists', 'navigation'),
            ('en', 'appointments', 'Appointments', 'navigation'),
            ('en', 'customers', 'Customers', 'navigation'),
            ('en', 'portfolio', 'Portfolio', 'navigation'),
            ('en', 'websites', 'Websites', 'navigation'),
            ('en', 'settings', 'Settings', 'navigation')
        ]
        
        for lang_code, key, value, context in translations:
            db.session.execute("""
                INSERT OR IGNORE INTO translation (language_code, key, value, context) 
                VALUES (?, ?, ?, ?)
            """, (lang_code, key, value, context))
        
        print("+ Çeviri verileri eklendi")
    except Exception as e:
        print(f"- Çeviri verileri zaten mevcut: {e}")
    
    # E-posta şablonları
    try:
        email_templates = [
            ('appointment_confirmation', 'Randevu Onayı', '<h3>Randevunuz Onaylandı</h3><p>Merhaba {customer_name},</p><p>{artist_name} ile {date} tarihindeki randevunuz onaylandı.</p>', 'appointment'),
            ('appointment_reminder', 'Randevu Hatırlatması', '<h3>Randevu Hatırlatması</h3><p>Merhaba {customer_name},</p><p>{artist_name} ile {date} tarihindeki randevunuz yaklaşıyor.</p>', 'appointment'),
            ('welcome_email', 'Hoş Geldiniz', '<h3>Hoş Geldiniz!</h3><p>Merhaba {customer_name},</p><p>Stüdyomuza hoş geldiniz. İlk randevunuzu almak için web sitemizi ziyaret edin.</p>', 'marketing')
        ]
        
        for name, subject, content, context in email_templates:
            db.session.execute("""
                INSERT OR IGNORE INTO email_template (name, subject, html_content, is_active) 
                VALUES (?, ?, ?, 1)
            """, (name, subject, content))
        
        print("+ E-posta şablonları eklendi")
    except Exception as e:
        print(f"- E-posta şablonları zaten mevcut: {e}")
    
    # SMS şablonları
    try:
        sms_templates = [
            ('appointment_confirmation', 'Randevunuz onaylandı: {artist_name} - {date}', 'appointment'),
            ('appointment_reminder', 'Hatırlatma: {artist_name} ile randevunuz {date}', 'appointment'),
            ('welcome_sms', 'Stüdyomuza hoş geldiniz! İlk randevunuzu almak için web sitemizi ziyaret edin.', 'marketing')
        ]
        
        for name, content, context in sms_templates:
            db.session.execute("""
                INSERT OR IGNORE INTO sms_template (name, content, is_active) 
                VALUES (?, ?, 1)
            """, (name, content))
        
        print("+ SMS şablonları eklendi")
    except Exception as e:
        print(f"- SMS şablonları zaten mevcut: {e}")
    
    # Otomasyon kuralları
    try:
        automation_rules = [
            ('Appointment Confirmation', 'appointment_created', '{"send_email": true, "send_sms": true}', '{"email_template": "appointment_confirmation", "sms_template": "appointment_confirmation"}', 1),
            ('Appointment Reminder', 'appointment_reminder', '{"hours_before": 24}', '{"email_template": "appointment_reminder", "sms_template": "appointment_reminder"}', 1),
            ('Welcome Email', 'customer_created', '{"delay_hours": 1}', '{"email_template": "welcome_email"}', 1)
        ]
        
        for name, trigger, conditions, actions, is_active in automation_rules:
            db.session.execute("""
                INSERT OR IGNORE INTO automation_rule (name, trigger_event, trigger_conditions, actions, is_active) 
                VALUES (?, ?, ?, ?, ?)
            """, (name, trigger, conditions, actions, is_active))
        
        print("+ Otomasyon kuralları eklendi")
    except Exception as e:
        print(f"- Otomasyon kuralları zaten mevcut: {e}")
    
    # Ürün kategorileri
    try:
        categories = [
            ('dövme-kitleri', 'tattoo-kits', 'Profesyonel dövme kitleri', 'https://picsum.photos/seed/kits/200/200.jpg'),
            ('dövme-aletleri', 'tattoo-machines', 'Dövme makineleri ve ekipmanlar', 'https://picsum.photos/seed/machines/200/200.jpg'),
            ('mürekkepler', 'tattoo-ink', 'Kaliteli dövme mürekkepleri', 'https://picsum.photos/seed/ink/200/200.jpg'),
            ('iğneler', 'tattoo-needles', 'Steril dövme iğneleri', 'https://picsum.photos/seed/needles/200/200.jpg'),
            ('bakım', 'aftercare', 'Dövme bakım ürünleri', 'https://picsum.photos/seed/aftercare/200/200.jpg')
        ]
        
        for name, slug, description, image in categories:
            db.session.execute("""
                INSERT OR IGNORE INTO product_category (name, slug, description, image_url, is_active) 
                VALUES (?, ?, ?, ?, 1)
            """, (name, slug, description, image))
        
        print("+ Ürün kategorileri eklendi")
    except Exception as e:
        print(f"- Ürün kategorileri zaten mevcut: {e}")
    
    db.session.commit()
    print("Ornek veriler basariyla eklendi!")

def main():
    """Ana fonksiyon"""
    with app.app_context():
        print("Veritabani guncelleniyor...")
        
        # Mevcut tabloları güncelle
        update_artist_website_table()
        
        # Yeni tabloları oluştur
        create_new_tables()
        
        # Örnek verileri ekle
        insert_sample_data()
        
        print("\nVeritabani basariyla guncellendi!")
        print("\nEklenen yeni ozellikler:")
        print("   • Multi-language destegi")
        print("   • E-ticaret sistemi")
        print("   • Otomasyon sistemi")
        print("   • Analitik ve raporlama")
        print("   • Advanced website builder ozellikleri")
        print("\nSistem kullanima hazır!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Hata olustu: {e}")
        raise
