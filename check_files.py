#!/usr/bin/env python3
"""
File integrity checker for 3D Asset Manager

This script checks if all uploaded model files still exist on the filesystem
and marks missing files in the database. Run this after deployment to identify
files that were lost during the deployment process.
"""

import os
from app import create_app, db
from app.models import Model3D

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
                if model.file_missing:
                    print(f"✅ RECOVERED: {model.name} (ID: {model.id}) - File found again")
                    model.file_missing = False
                # else:
                #     print(f"✅ OK: {model.name} (ID: {model.id})")
            else:
                missing_files += 1
                print(f"❌ MISSING: {model.name} (ID: {model.id}) - {model.original_filename}")
                print(f"   Expected path: {file_path}")
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
                print("Missing models are marked in the database and can be re-uploaded.")
            else:
                print("\n✅ All model files are present and accounted for!")
                
        except Exception as e:
            print(f"Error updating database: {e}")
            db.session.rollback()

def list_missing_models():
    """List all models with missing files"""
    app = create_app()
    
    with app.app_context():
        missing_models = Model3D.query.filter_by(file_missing=True).all()
        
        if not missing_models:
            print("✅ No models have missing files!")
            return
        
        print(f"📋 Models with missing files ({len(missing_models)}):")
        print("-" * 80)
        
        for model in missing_models:
            print(f"ID: {model.id:4d} | {model.name:30s} | {model.original_filename:30s} | Owner: {model.owner.username}")

def reset_missing_flags():
    """Reset all file_missing flags (use with caution)"""
    app = create_app()
    
    with app.app_context():
        count = Model3D.query.filter_by(file_missing=True).count()
        
        if count == 0:
            print("No models are marked as having missing files.")
            return
        
        response = input(f"This will reset missing file flags for {count} models. Continue? (y/N): ")
        
        if response.lower() == 'y':
            Model3D.query.filter_by(file_missing=True).update({'file_missing': False})
            db.session.commit()
            print(f"✅ Reset missing file flags for {count} models.")
        else:
            print("Operation cancelled.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            check_file_integrity()
        elif command == "list":
            list_missing_models()
        elif command == "reset":
            reset_missing_flags()
        else:
            print("Usage:")
            print("  python check_files.py check  - Check file integrity and update database")
            print("  python check_files.py list   - List models with missing files")
            print("  python check_files.py reset  - Reset all missing file flags")
    else:
        # Default action
        check_file_integrity()
