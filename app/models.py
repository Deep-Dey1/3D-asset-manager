from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with models
    models = db.relationship('Model3D', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'model_count': len(self.models)
        }

class Model3D(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    file_extension = db.Column(db.String(10), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    downloads = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    
    # Cloudinary integration
    cloudinary_public_id = db.Column(db.String(255), nullable=True)  # Cloudinary public ID
    cloudinary_url = db.Column(db.String(500), nullable=True)  # Cloudinary secure URL
    storage_type = db.Column(db.String(20), default='local')  # 'local' or 'cloudinary'
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def file_format(self):
        """Return file extension as file_format for template compatibility"""
        return self.file_extension
    
    @property  
    def user(self):
        """Return the owner for template compatibility"""
        return self.owner
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_extension': self.file_extension,
            'file_format': self.file_format,  # Include both for compatibility
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'downloads': self.downloads,
            'is_public': self.is_public,
            'storage_type': self.storage_type,
            'cloudinary_public_id': self.cloudinary_public_id,
            'cloudinary_url': self.cloudinary_url,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'full_name': self.user.full_name
            } if self.user else None
        }
    
    def get_file_size_formatted(self):
        """Return human readable file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
