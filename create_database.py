#!/usr/bin/env python3
"""
Database creation script for Tattoo Studio
"""

import sqlite3
import sys
import os
from datetime import datetime

def create_database():
    """Create database with all required tables"""
    
    db_path = 'tattoo_studio.db'
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Create user table
        cursor.execute("""
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                firebase_uid VARCHAR(255),
                oauth_provider VARCHAR(50),
                oauth_id VARCHAR(255),
                profile_picture TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create artist table
        cursor.execute("""
            CREATE TABLE artist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120) NOT NULL,
                phone VARCHAR(20),
                specialty VARCHAR(100),
                bio TEXT,
                experience_years INTEGER DEFAULT 0,
                instagram VARCHAR(100),
                portfolio_url TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        
        # Create customer table
        cursor.execute("""
            CREATE TABLE customer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120) NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        
        # Create studio table
        cursor.execute("""
            CREATE TABLE studio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120) NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        
        # Create appointment table
        cursor.execute("""
            CREATE TABLE appointment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                service_id INTEGER,
                appointment_date DATETIME NOT NULL,
                duration INTEGER,
                notes TEXT,
                status VARCHAR(20) DEFAULT 'scheduled',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artist (id),
                FOREIGN KEY (customer_id) REFERENCES customer (id)
            )
        """)
        
        # Create service table
        cursor.execute("""
            CREATE TABLE service (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist_id INTEGER NOT NULL,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2),
                duration INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artist (id)
            )
        """)
        
        # Create artist_website table
        cursor.execute("""
            CREATE TABLE artist_website (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist_id INTEGER NOT NULL,
                studio_id INTEGER,
                name VARCHAR(100) NOT NULL,
                subdomain VARCHAR(50) UNIQUE NOT NULL,
                url VARCHAR(255),
                theme VARCHAR(50) DEFAULT 'modern',
                primary_color VARCHAR(7) DEFAULT '#000000',
                secondary_color VARCHAR(7) DEFAULT '#ffffff',
                accent_color VARCHAR(7) DEFAULT '#ff6b6b',
                background_color VARCHAR(7) DEFAULT '#f8f9fa',
                primary_font VARCHAR(50) DEFAULT 'Inter',
                background_type VARCHAR(20) DEFAULT 'solid',
                background_url TEXT,
                animations_enabled BOOLEAN DEFAULT 1,
                animation_style VARCHAR(20) DEFAULT 'fade',
                logo_url TEXT,
                logo_size INTEGER DEFAULT 40,
                custom_css TEXT,
                page_components TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artist (id),
                FOREIGN KEY (studio_id) REFERENCES studio (id)
            )
        """)
        
        # Create studio_settings table
        cursor.execute("""
            CREATE TABLE studio_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                studio_id INTEGER NOT NULL,
                setting_key VARCHAR(100) NOT NULL,
                setting_value TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (studio_id) REFERENCES studio (id)
            )
        """)
        
        conn.commit()
        print("Database tables created successfully!")
        
        # Create sample data
        create_sample_data(cursor, conn)
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()

def create_sample_data(cursor, conn):
    """Create sample data for testing"""
    
    print("Creating sample data...")
    
    # Create sample users
    users = [
        ('admin', 'admin@tato.com', 'hashed_password'),
        ('demo_artist', 'artist@tato.com', 'hashed_password'),
        ('demo_customer', 'customer@tato.com', 'hashed_password'),
        ('demo_studio', 'studio@tato.com', 'hashed_password')
    ]
    
    for username, email, password in users:
        cursor.execute("""
            INSERT INTO user (username, email, password_hash)
            VALUES (?, ?, ?)
        """, (username, email, password))
    
    # Get user IDs
    cursor.execute("SELECT id, username FROM user")
    users_data = {row[1]: row[0] for row in cursor.fetchall()}
    
    # Create sample artist
    cursor.execute("""
        INSERT INTO artist (
            user_id, name, email, phone, specialty, bio, experience_years, 
            instagram, portfolio_url, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        users_data['demo_artist'],
        'Demo Artist',
        'artist@tato.com',
        '+90 555 123 4567',
        'Traditional & Realistic',
        'Professional tattoo artist with 10+ years of experience.',
        10,
        '@demo_artist',
        'https://instagram.com/demo_artist',
        1
    ))
    
    # Create sample customer
    cursor.execute("""
        INSERT INTO customer (
            user_id, name, email, phone, address
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        users_data['demo_customer'],
        'Demo Customer',
        'customer@tato.com',
        '+90 555 987 6543',
        'Istanbul, Turkey'
    ))
    
    # Create sample studio
    cursor.execute("""
        INSERT INTO studio (
            user_id, name, email, phone, address, description, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        users_data['demo_studio'],
        'Demo Tattoo Studio',
        'studio@tato.com',
        '+90 555 111 2222',
        'Istanbul, Turkey',
        'Professional tattoo studio with experienced artists.',
        1
    ))
    
    # Get IDs for relationships
    cursor.execute("SELECT id FROM artist WHERE name = 'Demo Artist'")
    artist_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM customer WHERE name = 'Demo Customer'")
    customer_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM studio WHERE name = 'Demo Tattoo Studio'")
    studio_id = cursor.fetchone()[0]
    
    # Create sample services
    services = [
        ('Traditional Tattoo', 'Classic traditional tattoo style', 500.00, 120),
        ('Realistic Portrait', 'Photorealistic portrait tattoos', 800.00, 180),
        ('Japanese Style', 'Traditional Japanese tattoo art', 600.00, 150),
        ('Geometric Design', 'Modern geometric patterns', 400.00, 90),
        ('Small Tattoo', 'Small and simple designs', 200.00, 60)
    ]
    
    for service_name, description, price, duration in services:
        cursor.execute("""
            INSERT INTO service (
                artist_id, name, description, price, duration
            ) VALUES (?, ?, ?, ?, ?)
        """, (artist_id, service_name, description, price, duration))
    
    # Create sample appointment
    cursor.execute("""
        INSERT INTO appointment (
            artist_id, customer_id, appointment_date, duration, notes, status
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        artist_id,
        customer_id,
        datetime.now().replace(hour=14, minute=0, second=0, microsecond=0),
        120,
        'First tattoo session',
        'scheduled'
    ))
    
    # Create sample website
    cursor.execute("""
        INSERT INTO artist_website (
            artist_id, studio_id, name, subdomain, url, theme, 
            primary_color, secondary_color, accent_color, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        artist_id,
        studio_id,
        'Demo Artist Website',
        'demo_artist',
        'https://demo_artist.tato.com',
        'modern',
        '#ff6b35',
        '#4ecdc4',
        '#667eea',
        1
    ))
    
    conn.commit()
    print("Sample data created successfully!")

def main():
    """Main function"""
    
    print("Creating Tattoo Studio database...")
    print("=" * 50)
    
    if create_database():
        print("=" * 50)
        print("Database created successfully!")
        print("You can now start the Flask application.")
        
        # Show created tables
        conn = sqlite3.connect('tattoo_studio.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\nCreated tables:")
        for table in tables:
            print(f"  • {table[0]}")
        
        conn.close()
        
    else:
        print("=" * 50)
        print("Database creation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
