import os
from dotenv import load_dotenv

# Try to import cloudinary, handle gracefully if not available
try:
    import cloudinary
    CLOUDINARY_AVAILABLE = True
except ImportError:
    print("Warning: Cloudinary package not available. Install with: pip install cloudinary")
    CLOUDINARY_AVAILABLE = False

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
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or 'dhktf9m25'
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or '159532712964974'
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or 'DssDwgjlFynfrU2V8sFZzt3ixF8'
    
    # Configure Cloudinary if available
    if CLOUDINARY_AVAILABLE:
        try:
            cloudinary.config(
                cloud_name=CLOUDINARY_CLOUD_NAME,
                api_key=CLOUDINARY_API_KEY,
                api_secret=CLOUDINARY_API_SECRET,
                secure=True
            )
            print("Cloudinary configured successfully")
        except Exception as e:
            print(f"Cloudinary configuration error: {e}")
    else:
        print("Cloudinary not available - file upload will use local storage")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
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
