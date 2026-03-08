#!/usr/bin/env python3
"""
SQLite migration script to add user_id column to artist table
"""

import sqlite3
import os

def migrate_artist_table():
    """Add user_id column to artist table"""
    
    db_path = 'tattoo_studio.db'
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if user_id column already exists
        cursor.execute("PRAGMA table_info(artist)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("Adding user_id column to artist table...")
            
            # Add user_id column
            cursor.execute("ALTER TABLE artist ADD COLUMN user_id INTEGER")
            
            # Add foreign key constraint manually (SQLite doesn't support ALTER TABLE ADD CONSTRAINT)
            # We'll handle this at the application level
            
            # Update existing records to set user_id to 1 (admin user)
            cursor.execute("UPDATE artist SET user_id = 1 WHERE user_id IS NULL")
            
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("user_id column already exists in artist table")
            
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_artist_table()
