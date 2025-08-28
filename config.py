import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Railway DATABASE_URL handling
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        print(f"Original DATABASE_URL: {DATABASE_URL}")
        
        # Railway provides postgresql:// URLs which need to be postgresql://
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
            print(f"Converted DATABASE_URL: {DATABASE_URL}")
        
        # Validate the URL format
        if '://port/' in DATABASE_URL or not DATABASE_URL.startswith('postgresql://'):
            print(f"Invalid DATABASE_URL format, falling back to SQLite")
            SQLALCHEMY_DATABASE_URI = 'sqlite:///3d_asset_manager.db'
        else:
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
            print(f"Using PostgreSQL database")
    else:
        print("No DATABASE_URL found, using SQLite")
        SQLALCHEMY_DATABASE_URI = 'sqlite:///3d_asset_manager.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # File upload settings
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    
    # Use Railway Volume for persistent storage in production, local uploads for development
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        # Production: Use Railway Volume mount point
        UPLOAD_FOLDER = os.environ.get('UPLOAD_PATH', '/app/uploads')
    else:
        # Development: Use local uploads folder
        UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    ALLOWED_EXTENSIONS = {'obj', 'fbx', 'gltf', 'glb', 'dae', '3ds', 'ply', 'stl'}
    
    # Railway specific
    PORT = int(os.environ.get('PORT', 5000))
    
    @staticmethod
    def init_app(app):
        # Create upload directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
