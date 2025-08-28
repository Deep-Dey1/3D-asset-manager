"""
Database migration script to add Cloudinary support to existing Model3D table
"""
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Model3D
from sqlalchemy import text

def migrate_database():
    """Add Cloudinary columns to existing Model3D table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if columns already exist
            result = db.session.execute(text("PRAGMA table_info(model3d)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'cloudinary_public_id' not in columns:
                print("Adding cloudinary_public_id column...")
                db.session.execute(text("ALTER TABLE model3d ADD COLUMN cloudinary_public_id VARCHAR(255)"))
            
            if 'cloudinary_url' not in columns:
                print("Adding cloudinary_url column...")
                db.session.execute(text("ALTER TABLE model3d ADD COLUMN cloudinary_url VARCHAR(500)"))
            
            if 'storage_type' not in columns:
                print("Adding storage_type column...")
                db.session.execute(text("ALTER TABLE model3d ADD COLUMN storage_type VARCHAR(20) DEFAULT 'local'"))
                
                # Set existing records to 'local' storage type
                db.session.execute(text("UPDATE model3d SET storage_type = 'local' WHERE storage_type IS NULL"))
            
            db.session.commit()
            print("✅ Database migration completed successfully!")
            
            # Print current table structure
            result = db.session.execute(text("PRAGMA table_info(model3d)"))
            print("\nCurrent Model3D table structure:")
            for row in result.fetchall():
                print(f"  {row[1]} ({row[2]})")
                
        except Exception as e:
            print(f"❌ Migration error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_database()
