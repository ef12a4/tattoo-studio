#!/usr/bin/env python3
"""
Dövmeci Stüdyosu - Veritabanı Başlatma Script'i
Bu script veritabanını oluşturur ve başlangıç verilerini ekler.
"""

from app import app, db, User, Artist, Customer, Appointment, TattooDesign, StudioSettings
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def init_database():
    """Veritabanını başlat ve örnek verileri ekle"""
    
    with app.app_context():
        print("Veritabanı tabloları oluşturuluyor...")
        db.create_all()
        
        # Mevcut verileri temizle (isteğe bağlı)
        print("Mevcut veriler temizleniyor...")
        TattooDesign.query.delete()
        Appointment.query.delete()
        Customer.query.delete()
        Artist.query.delete()
        StudioSettings.query.delete()
        User.query.delete()
        
        # Admin kullanıcısı oluştur
        print("Admin kullanıcısı oluşturuluyor...")
        admin = User(
            username='admin',
            email='admin@tattoostudio.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        
        # Stüdyo ayarları
        print("Stüdyo ayarları oluşturuluyor...")
        settings = [
            StudioSettings(key='studio_name', value='İstanbul Dövme Stüdyosu', description='Stüdyonun adı'),
            StudioSettings(key='email', value='info@tattoostudio.com', description='İletişim e-postası'),
            StudioSettings(key='phone', value='+90 212 555 0123', description='İletişim telefonu'),
            StudioSettings(key='address', value='İstanbul, Beyoğlu, İstiklal Cad. No:123', description='Stüdyo adresi'),
            StudioSettings(key='working_hours', value='10:00 - 20:00', description='Çalışma saatleri'),
            StudioSettings(key='working_days', value='Salı - Pazar', description='Çalışma günleri'),
            StudioSettings(key='appointment_duration', value='120', description='Varsayılan randevu süresi (dakika)'),
            StudioSettings(key='deposit_percentage', value='20', description='Kapora oranı (%)'),
            StudioSettings(key='auto_reminders', value='true', description='Otomatik hatırlatmalar')
        ]
        
        for setting in settings:
            db.session.add(setting)
        
        # Örnek sanatçılar
        print("Örnek sanatçılar oluşturuluyor...")
        artists = [
            Artist(
                name='Ali Demir',
                email='ali@tattoostudio.com',
                phone='+90 532 111 2233',
                specialty='Realist Dövmeler, Portre',
                bio='10 yıllık deneyimle realist dövme sanatında uzmanlaştım. Özellikle portre çalışmaları konusunda iddialıyım.',
                experience_years=10,
                instagram='alidemirtattoo',
                portfolio_url='https://alidemirtattoo.com',
                is_active=True,
                user_id=admin.id
            ),
            Artist(
                name='Ayşe Yılmaz',
                email='ayse@tattoostudio.com',
                phone='+90 533 444 5566',
                specialty='Geometrik, Dotwork, Minimalist',
                bio='Minimalist ve geometrik tasarımlarla modern dövme sanatını yorumluyorum. Hassas detay çalışmaları benim uzmanlık alanım.',
                experience_years=7,
                instagram='ayseyilmaztattoo',
                portfolio_url='https://ayseyilmaztattoo.com',
                is_active=True,
                user_id=admin.id
            ),
            Artist(
                name='Mehmet Özkan',
                email='mehmet@tattoostudio.com',
                phone='+90 534 777 8899',
                specialty='Tribal, Geleneksel Japon',
                bio='Geleneksel tribal ve japon dövme stillerinde uzmanlaştım. Büyük ve kapsamlı projelerde tecrübeliyim.',
                experience_years=12,
                instagram='mehmetozkantattoo',
                portfolio_url='https://mehmetozkantattoo.com',
                is_active=True,
                user_id=admin.id
            )
        ]
        
        for artist in artists:
            db.session.add(artist)
        
        db.session.commit()
        
        # Örnek müşteriler
        print("Örnek müşteriler oluşturuluyor...")
        from datetime import date
        customers = [
            Customer(
                name='Can Kaya',
                email='can.kaya@email.com',
                phone='+90 555 111 2233',
                date_of_birth=date(1990, 5, 15),
                notes='İlk dövmesi olacak. Hafif endişeli.',
                user_id=admin.id
            ),
            Customer(
                name='Zeynep Ak',
                email='zeynep.ak@email.com',
                phone='+90 555 333 4455',
                date_of_birth=date(1995, 8, 22),
                notes='Daha önce 2 dövmesi oldu. Kolay müşteri.',
                user_id=admin.id
            ),
            Customer(
                name='Emir Polat',
                email='emir.polat@email.com',
                phone='+90 555 666 7788',
                date_of_birth=date(1988, 12, 3),
                notes='Sırt dövmesi planlıyor. Büyük proje.',
                user_id=admin.id
            ),
            Customer(
                name='Elif Çelik',
                email='elif.celik@email.com',
                phone='+90 555 999 0011',
                date_of_birth=date(1992, 3, 18),
                notes='Minimalist tarzı seviyor.',
                user_id=admin.id
            )
        ]
        
        for customer in customers:
            db.session.add(customer)
        
        db.session.commit()
        
        # Örnek randevular
        print("Örnek randevular oluşturuluyor...")
        appointments = [
            Appointment(
                customer_id=1,
                artist_id=1,
                date_time=datetime.now() + timedelta(days=2, hours=14),
                duration=180,
                status='scheduled',
                deposit_amount=500,
                total_price=2500,
                notes='Ön kol için portre dövmesi',
                design_description='Babaannesinin portresi, realist tarzda'
            ),
            Appointment(
                customer_id=2,
                artist_id=2,
                date_time=datetime.now() + timedelta(days=1, hours=16),
                duration=120,
                status='scheduled',
                deposit_amount=300,
                total_price=1500,
                notes='Dirsek içi geometrik tasarım',
                design_description='Minimalist geometrik şekiller, siyah mürekkep'
            ),
            Appointment(
                customer_id=3,
                artist_id=3,
                date_time=datetime.now() - timedelta(days=1, hours=10),
                duration=240,
                status='completed',
                deposit_amount=800,
                total_price=4000,
                notes='Sırt tribal dövmesi - tamamlandı',
                design_description='Polinezyan tribal tasarım, tüm sırt'
            ),
            Appointment(
                customer_id=4,
                artist_id=2,
                date_time=datetime.now() + timedelta(days=3, hours=15),
                duration=90,
                status='scheduled',
                deposit_amount=200,
                total_price=1000,
                notes='Bileklik tarzı dövme',
                design_description='İnce çizgilerden oluşan bileklik tasarımı'
            )
        ]
        
        for appointment in appointments:
            db.session.add(appointment)
        
        db.session.commit()
        
        # Örnek portfolyo tasarımları
        print("Örnek portfolyo tasarımları oluşturuluyor...")
        designs = [
            TattooDesign(
                title='Realist Aslan Portresi',
                description='Detaylı realist aslan portresi çalışması. Siyah ve gri tonlarda.',
                artist_id=1,
                image_url='https://picsum.photos/seed/lion1/400/300.jpg',
                category='realist',
                style='portre',
                estimated_price=3000,
                estimated_duration=240
            ),
            TattooDesign(
                title='Geometrik Mandalası',
                description='İnce çizgilerden oluşan geometrik mandala tasarımı.',
                artist_id=2,
                image_url='https://picsum.photos/seed/mandala1/400/300.jpg',
                category='geometrik',
                style='dotwork',
                estimated_price=1500,
                estimated_duration=180
            ),
            TattooDesign(
                title='Japon Ejderha',
                description='Geleneksel japon stilinde ejderha tasarımı. Renkli çalışma.',
                artist_id=3,
                image_url='https://picsum.photos/seed/dragon1/400/300.jpg',
                category='japon',
                style='traditional',
                estimated_price=5000,
                estimated_duration=300
            ),
            TattooDesign(
                title='Minimalist Dağ Manzarası',
                description='Basit çizgilerle çizilmiş dağ manzarası. Küçük boyutta.',
                artist_id=2,
                image_url='https://picsum.photos/seed/mountain1/400/300.jpg',
                category='minimalist',
                style='liner',
                estimated_price=800,
                estimated_duration=60
            ),
            TattooDesign(
                title='Tribal Kurt',
                description='Geleneksel tribal stilinde kurt tasarımı. Sırt için uygun.',
                artist_id=3,
                image_url='https://picsum.photos/seed/wolf1/400/300.jpg',
                category='tribal',
                style='blackwork',
                estimated_price=2500,
                estimated_duration=200
            ),
            TattooDesign(
                title='Kedi Portresi',
                description='Müşterinin kedisinin realist portresi. Ön kol için.',
                artist_id=1,
                image_url='https://picsum.photos/seed/cat1/400/300.jpg',
                category='realist',
                style='portre',
                estimated_price=2000,
                estimated_duration=180
            )
        ]
        
        for design in designs:
            db.session.add(design)
        
        db.session.commit()
        
        print("\nBasarili! Veritabani olusturuldu ve ornek veriler eklendi!")
        print("\nGiris Bilgileri:")
        print("   Kullanici Adi: admin")
        print("   Sifre: admin123")
        print("\nOlusturulan Veriler:")
        print(f"   • {len(artists)} sanatci")
        print(f"   • {len(customers)} musteri")
        print(f"   • {len(appointments)} randevu")
        print(f"   • {len(designs)} portfolyo tasarimi")
        print(f"   • {len(settings)} stüdyo ayari")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"Hata olustu: {e}")
        raise
