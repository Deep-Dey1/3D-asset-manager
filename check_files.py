#!/usr/bin/env python
"""
Migration script to handle file storage transition
Use this script if you need to migrate existing uploaded files
"""

import os
import sys
import sqlite3
from flask import Flask
from app import create_app, db
from app.models import Model3D

def migrate_files():
    """Check for missing files and report status"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking file storage status...")
        print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
        print(f"Railway environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'Not set')}")
        print()
        
        # Get all models from database
        models = Model3D.query.all()
        print(f"📊 Found {len(models)} models in database")
        
        if not models:
            print("ℹ️  No models found in database")
            return
        
        # Check upload folder
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            print(f"⚠️  Upload folder does not exist: {upload_folder}")
            print("Creating upload folder...")
            os.makedirs(upload_folder, exist_ok=True)
        
        # List files in upload folder
        files_on_disk = set()
        if os.path.exists(upload_folder):
            files_on_disk = set(os.listdir(upload_folder))
            print(f"📁 Files in upload folder: {len(files_on_disk)}")
        
        # Check each model
        missing_files = []
        present_files = []
        
        for model in models:
            file_path = os.path.join(upload_folder, model.filename)
            if os.path.exists(file_path):
                present_files.append(model)
                print(f"✅ {model.name} - File found: {model.filename}")
            else:
                missing_files.append(model)
                print(f"❌ {model.name} - File missing: {model.filename}")
        
        print()
        print(f"📈 Summary:")
        print(f"  - Models with files: {len(present_files)}")
        print(f"  - Models with missing files: {len(missing_files)}")
        
        if missing_files:
            print()
            print("🚨 Missing files detected!")
            print("This usually happens after Railway deployment without persistent storage.")
            print()
            print("📋 To fix this:")
            print("1. Set up Railway Volume (see README.md)")
            print("2. Re-upload missing models")
            print("3. Or remove database entries for missing files")
            print()
            
            # Ask if user wants to clean up missing entries
            if len(sys.argv) > 1 and sys.argv[1] == '--clean':
                print("🧹 Cleaning up database entries for missing files...")
                for model in missing_files:
                    print(f"Removing: {model.name}")
                    db.session.delete(model)
                db.session.commit()
                print(f"✅ Removed {len(missing_files)} models with missing files")
        else:
            print("🎉 All models have their files present!")

if __name__ == '__main__':
    migrate_files()
