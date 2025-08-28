import os
from dotenv import load_dotenv
import re

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Fix Railway DATABASE_URL format
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Railway sometimes provides postgres:// URLs which need to be postgresql://
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        # Handle malformed URLs - simple validation
        if '://port/' in DATABASE_URL or DATABASE_URL.count(':') < 2:
            # Fallback to SQLite if DATABASE_URL looks malformed
            SQLALCHEMY_DATABASE_URI = 'sqlite:///3d_asset_manager.db'
        else:
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///3d_asset_manager.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'obj', 'fbx', 'gltf', 'glb', 'dae', '3ds', 'ply', 'stl'}
    
    # Railway specific
    PORT = int(os.environ.get('PORT', 5000))
    
    @staticmethod
    def init_app(app):
        # Create upload directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
