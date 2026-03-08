#!/usr/bin/env python3
"""
Web Siteleri için Örnek Veri Oluşturma Script'i
"""

from app import app, db, ArtistWebsite, Artist
from datetime import datetime

def create_sample_websites():
    """Örnek sanatçı web siteleri oluştur"""
    
    with app.app_context():
        print("Örnek web siteleri oluşturuluyor...")
        
        # Mevcut sanatçıları al
        artists = Artist.query.all()
        
        for artist in artists:
            # Her sanatçı için web sitesi kontrol et
            existing_website = ArtistWebsite.query.filter_by(artist_id=artist.id).first()
            
            if not existing_website:
                # Subdomain oluştur
                subdomain = artist.name.lower().replace(' ', '').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
                
                website = ArtistWebsite(
                    artist_id=artist.id,
                    subdomain=subdomain,
                    theme='default',
                    primary_color='#000000',
                    secondary_color='#ffffff',
                    accent_color='#ff6b6b',
                    bio_title=f'{artist.name} - Profesyonel Dövme Sanatçısı',
                    about_text=artist.bio or f'{artist.name} profesyonel dövme sanatçısıyım. {artist.specialty or "Özel dövme tasarımları"} konusunda uzmanlaştım.',
                    contact_email=artist.email,
                    contact_phone=artist.phone,
                    instagram_url=f'https://instagram.com/{artist.instagram}' if artist.instagram else None,
                    is_active=True
                )
                
                db.session.add(website)
                print(f"+ {artist.name} için web sitesi oluşturuldu: {subdomain}.tattoostudio.com")
            else:
                print(f"i {artist.name} için web sitesi zaten mevcut")
        
        try:
            db.session.commit()
            print("\nTum web siteleri basariyla olusturuldu!")
            print("\nTest Edebileceginiz Adresler:")
            
            websites = ArtistWebsite.query.filter_by(is_active=True).all()
            for website in websites:
                print(f"   • http://localhost:5000/{website.subdomain}")
                
        except Exception as e:
            print(f"Hata olustu: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_sample_websites()
