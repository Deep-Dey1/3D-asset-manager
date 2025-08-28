"""
Cloud storage utilities for persistent file storage
Supports multiple cloud providers for Railway deployment
"""
import os
import tempfile
from flask import current_app

class CloudStorage:
    """Abstract base class for cloud storage providers"""
    
    def upload_file(self, file_path, filename):
        """Upload a file to cloud storage"""
        raise NotImplementedError
    
    def download_file(self, filename, local_path):
        """Download a file from cloud storage to local path"""
        raise NotImplementedError
    
    def delete_file(self, filename):
        """Delete a file from cloud storage"""
        raise NotImplementedError
    
    def file_exists(self, filename):
        """Check if a file exists in cloud storage"""
        raise NotImplementedError
    
    def get_file_url(self, filename):
        """Get a direct URL to the file (if supported)"""
        raise NotImplementedError

class LocalStorage(CloudStorage):
    """Local filesystem storage (development fallback)"""
    
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def upload_file(self, file_path, filename):
        """Copy file to upload folder"""
        import shutil
        destination = os.path.join(self.upload_folder, filename)
        shutil.copy2(file_path, destination)
        return destination
    
    def download_file(self, filename, local_path):
        """Copy file from upload folder to local path"""
        import shutil
        source = os.path.join(self.upload_folder, filename)
        if os.path.exists(source):
            shutil.copy2(source, local_path)
            return True
        return False
    
    def delete_file(self, filename):
        """Delete file from upload folder"""
        file_path = os.path.join(self.upload_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    def file_exists(self, filename):
        """Check if file exists in upload folder"""
        file_path = os.path.join(self.upload_folder, filename)
        return os.path.exists(file_path)
    
    def get_file_url(self, filename):
        """Return local file path"""
        return os.path.join(self.upload_folder, filename)

# Storage factory function
def get_storage_provider():
    """Get the appropriate storage provider based on configuration"""
    
    # Check for cloud storage environment variables
    if os.environ.get('CLOUDINARY_URL'):
        # Cloudinary is available and free for small usage
        try:
            from .cloudinary_storage import CloudinaryStorage
            return CloudinaryStorage()
        except ImportError:
            print("Cloudinary not available, falling back to local storage")
    
    # Check for AWS S3
    elif os.environ.get('AWS_S3_BUCKET'):
        try:
            from .s3_storage import S3Storage
            return S3Storage()
        except ImportError:
            print("AWS S3 not available, falling back to local storage")
    
    # Fallback to local storage
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return LocalStorage(upload_folder)

# Global storage instance
storage = None

def init_storage(app):
    """Initialize storage with Flask app context"""
    global storage
    with app.app_context():
        storage = get_storage_provider()
    return storage

def get_storage():
    """Get the current storage instance"""
    global storage
    if storage is None:
        storage = get_storage_provider()
    return storage
