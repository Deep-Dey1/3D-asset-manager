#!/usr/bin/env python3
"""
Database migration script for 3D Asset Manager

This script adds the file_missing column to existing Model3D tables
and runs a file integrity check.
"""

import os
import sys
from sqlalchemy import text
from app import create_app, db
from app.models import Model3D

def migrate_database():
    """Add the file_missing column if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if the column already exists
            result = db.engine.execute(text("PRAGMA table_info(model3_d)"))
            columns = [row[1] for row in result]
            
            if 'file_missing' not in columns:
                print("Adding file_missing column to Model3D table...")
                db.engine.execute(text("ALTER TABLE model3_d ADD COLUMN file_missing BOOLEAN DEFAULT 0"))
                print("✅ file_missing column added successfully!")
            else:
                print("✅ file_missing column already exists")
                
        except Exception as e:
            print(f"Error during migration: {e}")
            # For PostgreSQL, try a different approach
            try:
                print("Trying PostgreSQL syntax...")
                db.engine.execute(text("ALTER TABLE model3_d ADD COLUMN IF NOT EXISTS file_missing BOOLEAN DEFAULT FALSE"))
                print("✅ file_missing column added successfully (PostgreSQL)!")
            except Exception as e2:
                print(f"Migration failed: {e2}")
                print("The file_missing column may already exist or there may be a database issue.")
                return False
        
        # Run file integrity check after migration
        print("\nRunning file integrity check...")
        check_file_integrity()
        return True

def check_file_integrity():
    """Check if all model files exist and update database accordingly"""
    app = create_app()
    
    with app.app_context():
        upload_folder = app.config['UPLOAD_FOLDER']
        
        # Ensure upload folder exists
        if not os.path.exists(upload_folder):
            print(f"Creating upload folder: {upload_folder}")
            os.makedirs(upload_folder, exist_ok=True)
        
        # Get all models from database
        models = Model3D.query.all()
        total_models = len(models)
        missing_files = 0
        existing_files = 0
        
        print(f"Checking {total_models} models for file integrity...")
        print("-" * 60)
        
        for model in models:
            file_path = os.path.join(upload_folder, model.filename)
            file_exists = os.path.exists(file_path)
            
            if file_exists:
                existing_files += 1
                # Reset file_missing flag if file exists
                if hasattr(model, 'file_missing') and model.file_missing:
                    print(f"✅ RECOVERED: {model.name} (ID: {model.id}) - File found again")
                    model.file_missing = False
            else:
                missing_files += 1
                print(f"❌ MISSING: {model.name} (ID: {model.id}) - {model.original_filename}")
                if hasattr(model, 'file_missing'):
                    model.file_missing = True
        
        # Commit all changes
        try:
            db.session.commit()
            print("-" * 60)
            print(f"File integrity check completed:")
            print(f"  Total models: {total_models}")
            print(f"  Files found: {existing_files}")
            print(f"  Missing files: {missing_files}")
            
            if missing_files > 0:
                print(f"\n⚠️  {missing_files} model files are missing!")
                print("These files were likely lost during deployment.")
                print("Users will see appropriate error messages when trying to view these models.")
            else:
                print("\n✅ All model files are present and accounted for!")
                
        except Exception as e:
            print(f"Error updating database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    print("=" * 60)
    
    if migrate_database():
        print("\n✅ Migration completed successfully!")
        print("\nNext steps:")
        print("1. Restart your Flask application")
        print("2. Run 'python check_files.py' periodically to monitor file integrity")
        print("3. Users will see helpful error messages for missing files")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
