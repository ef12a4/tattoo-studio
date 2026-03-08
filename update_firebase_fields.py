"""Firebase Authentication alanlarını veritabanına ekle"""
from app import app, db
from sqlalchemy import text

def add_firebase_fields():
    """Firebase alanlarını User tablosuna ekle"""
    with app.app_context():
        try:
            # Firebase alanlarını ekle
            db.session.execute(text("""
                ALTER TABLE user ADD COLUMN firebase_uid VARCHAR(128)
            """))
            
            db.session.execute(text("""
                ALTER TABLE user ADD COLUMN oauth_provider VARCHAR(50)
            """))
            
            db.session.execute(text("""
                ALTER TABLE user ADD COLUMN oauth_id VARCHAR(128)
            """))
            
            db.session.execute(text("""
                ALTER TABLE user ADD COLUMN profile_picture VARCHAR(500)
            """))
            
            db.session.commit()
            print("Firebase alanlari basariyla eklendi!")
            
        except Exception as e:
            if "duplicate column name" not in str(e) and "no such table" not in str(e):
                print(f"Hata: {e}")
            else:
                print("Firebase alanlari zaten mevcut!")
            db.session.rollback()

if __name__ == '__main__':
    add_firebase_fields()
