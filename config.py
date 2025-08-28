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
    
    # Railway persistent volume storage
    # Use /app/data for Railway volume mount, fallback to local for development
    UPLOAD_FOLDER = os.environ.get('UPLOAD_PATH', '/app/data/uploads') if os.environ.get('RAILWAY_ENVIRONMENT') else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    ALLOWED_EXTENSIONS = {'obj', 'fbx', 'gltf', 'glb', 'dae', '3ds', 'ply', 'stl'}
    
    # Railway specific
    PORT = int(os.environ.get('PORT', 5000))
    RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT')
    
    @staticmethod
    def init_app(app):
        # Create upload directory if it doesn't exist
        upload_path = app.config['UPLOAD_FOLDER']
        
        try:
            os.makedirs(upload_path, exist_ok=True)
            print(f"✅ Upload directory created/verified: {upload_path}")
            
            # Test write permissions
            test_file = os.path.join(upload_path, '.write_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print(f"✅ Write permissions verified for: {upload_path}")
            
        except Exception as e:
            print(f"❌ Error setting up upload directory: {e}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Upload path: {upload_path}")
            
            # Fallback to current directory if volume mount fails
            fallback_path = os.path.join(os.getcwd(), 'uploads')
            try:
                os.makedirs(fallback_path, exist_ok=True)
                app.config['UPLOAD_FOLDER'] = fallback_path
                print(f"⚠️ Using fallback upload directory: {fallback_path}")
            except Exception as fallback_error:
                print(f"❌ Fallback directory creation failed: {fallback_error}")
                raise Exception("Cannot create upload directory")
