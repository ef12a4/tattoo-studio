#!/usr/bin/env python3
"""
Database migration script to fix missing user_id column in artist table
"""

import sqlite3
import sys
import os

def check_database():
    """Check database structure and fix missing columns"""
    
    db_path = 'tattoo_studio.db'
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if artist table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='artist'
        """)
        
        if not cursor.fetchone():
            print("Artist table not found")
            return False
        
        # Get current table structure
        cursor.execute("PRAGMA table_info(artist)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("Current artist table columns:")
        for col in columns:
            print(f"  {col[1]} - {col[2]}")
        
        # Check if user_id column exists
        if 'user_id' in column_names:
            print("user_id column already exists")
            return True
        
        # Add user_id column
        print("Adding user_id column to artist table...")
        
        try:
            cursor.execute("""
                ALTER TABLE artist 
                ADD COLUMN user_id INTEGER
            """)
            
            # Also add other missing columns if needed
            missing_columns = {
                'firebase_uid': 'TEXT',
                'oauth_provider': 'TEXT',
                'oauth_id': 'TEXT',
                'profile_picture': 'TEXT'
            }
            
            for col_name, col_type in missing_columns.items():
                if col_name not in column_names:
                    print(f"Adding {col_name} column...")
                    cursor.execute(f"""
                        ALTER TABLE artist 
                        ADD COLUMN {col_name} {col_type}
                    """)
            
            conn.commit()
            print("Database migration completed successfully!")
            
            # Show updated structure
            cursor.execute("PRAGMA table_info(artist)")
            updated_columns = cursor.fetchall()
            print("\n📋 Updated artist table columns:")
            for col in updated_columns:
                print(f"  • {col[1]} - {col[2]}")
            
            return True
            
        except sqlite3.Error as e:
            print(f"Error adding column: {e}")
            conn.rollback()
            return False
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()

def create_sample_data():
    """Create sample data if needed"""
    
    db_path = 'tattoo_studio.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if there are any artists
        cursor.execute("SELECT COUNT(*) FROM artist")
        artist_count = cursor.fetchone()[0]
        
        if artist_count > 0:
            print(f"Found {artist_count} artists in database")
            return True
        
        print("Creating sample artist data...")
        
        # First create a sample user
        cursor.execute("""
            INSERT OR IGNORE INTO user (username, email, password_hash, created_at)
            VALUES ('demo_artist', 'artist@tato.com', 'hashed_password', datetime('now'))
        """)
        
        # Get the user ID
        cursor.execute("SELECT id FROM user WHERE username = 'demo_artist'")
        user_result = cursor.fetchone()
        
        if user_result:
            user_id = user_result[0]
            
            # Create sample artist
            cursor.execute("""
                INSERT INTO artist (
                    name, email, phone, specialty, bio, 
                    experience_years, instagram, portfolio_url, 
                    is_active, user_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                'Demo Artist',
                'artist@tato.com', 
                '+90 555 123 4567',
                'Traditional & Realistic',
                'Professional tattoo artist with 10+ years of experience.',
                10,
                '@demo_artist',
                'https://instagram.com/demo_artist',
                1,
                user_id
            ))
            
            conn.commit()
            print("Sample artist data created successfully!")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Error creating sample data: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    """Main migration function"""
    
    print("Starting database migration...")
    print("=" * 50)
    
    # Step 1: Check and fix database structure
    if not check_database():
        print("Database migration failed!")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Step 2: Create sample data if needed
    if not create_sample_data():
        print("Sample data creation failed!")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Database migration completed successfully!")
    print("You can now restart the Flask application.")

if __name__ == "__main__":
    main()
