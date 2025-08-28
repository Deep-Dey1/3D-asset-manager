"""
Cloudinary service for handling 3D model file uploads and management
"""
import os
import tempfile
from typing import Dict, Optional, Tuple
import cloudinary
import cloudinary.uploader
import cloudinary.api
from werkzeug.utils import secure_filename
from flask import current_app

class CloudinaryService:
    """Service for managing 3D model files in Cloudinary"""
    
    def __init__(self):
        """Initialize Cloudinary configuration"""
        # Configure Cloudinary (done in config.py but ensuring it's set)
        cloudinary.config(
            cloud_name=current_app.config.get('CLOUDINARY_CLOUD_NAME', 'dhktf9m25'),
            api_key=current_app.config.get('CLOUDINARY_API_KEY', '159532712964974'),
            api_secret=current_app.config.get('CLOUDINARY_API_SECRET', 'DssDwgjlFynfrU2V8sFZzt3ixF8'),
            secure=True
        )
    
    def upload_model(self, file_obj, original_filename: str, model_id: int) -> Dict:
        """
        Upload a 3D model file to Cloudinary
        
        Args:
            file_obj: File object to upload
            original_filename: Original filename
            model_id: Database model ID for organization
            
        Returns:
            Dict with upload result including public_id and secure_url
        """
        try:
            # Create a secure filename
            secure_name = secure_filename(original_filename)
            file_extension = os.path.splitext(secure_name)[1].lower()
            
            # Create public_id with model organization
            public_id = f"3d-models/model_{model_id}_{secure_name}"
            
            # Determine resource type and format
            resource_type = "raw"  # For 3D model files
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file_obj,
                public_id=public_id,
                resource_type=resource_type,
                folder="3d-asset-manager",
                overwrite=True,
                invalidate=True,
                use_filename=True,
                unique_filename=False,
                tags=[f"model_{model_id}", "3d-model", file_extension.replace(".", "")]
            )
            
            return {
                'success': True,
                'public_id': upload_result['public_id'],
                'secure_url': upload_result['secure_url'],
                'url': upload_result['url'],
                'bytes': upload_result['bytes'],
                'format': upload_result.get('format', file_extension.replace(".", "")),
                'resource_type': upload_result['resource_type'],
                'cloudinary_id': upload_result['public_id']
            }
            
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_model_url(self, public_id: str) -> Optional[str]:
        """
        Get the secure URL for a model file
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            Secure URL or None if not found
        """
        try:
            # Generate secure URL
            url = cloudinary.utils.cloudinary_url(
                public_id,
                resource_type="raw",
                secure=True
            )[0]
            return url
        except Exception as e:
            print(f"Error getting model URL: {e}")
            return None
    
    def delete_model(self, public_id: str) -> bool:
        """
        Delete a model file from Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = cloudinary.uploader.destroy(
                public_id,
                resource_type="raw",
                invalidate=True
            )
            return result.get('result') == 'ok'
        except Exception as e:
            print(f"Error deleting model: {e}")
            return False
    
    def check_model_exists(self, public_id: str) -> bool:
        """
        Check if a model file exists in Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            True if exists, False otherwise
        """
        try:
            cloudinary.api.resource(public_id, resource_type="raw")
            return True
        except cloudinary.exceptions.NotFound:
            return False
        except Exception as e:
            print(f"Error checking model existence: {e}")
            return False
    
    def get_model_info(self, public_id: str) -> Optional[Dict]:
        """
        Get detailed information about a model file
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            Dict with file information or None
        """
        try:
            resource = cloudinary.api.resource(public_id, resource_type="raw")
            return {
                'public_id': resource['public_id'],
                'secure_url': resource['secure_url'],
                'url': resource['url'],
                'bytes': resource['bytes'],
                'format': resource.get('format', ''),
                'created_at': resource['created_at'],
                'resource_type': resource['resource_type']
            }
        except Exception as e:
            print(f"Error getting model info: {e}")
            return None
    
    def list_user_models(self, user_id: int, max_results: int = 100) -> list:
        """
        List all models for a specific user
        
        Args:
            user_id: User ID
            max_results: Maximum number of results
            
        Returns:
            List of model information
        """
        try:
            result = cloudinary.api.resources(
                resource_type="raw",
                prefix="3d-asset-manager/3d-models/",
                tags=f"user_{user_id}",
                max_results=max_results
            )
            return result.get('resources', [])
        except Exception as e:
            print(f"Error listing user models: {e}")
            return []

# Global service instance
cloudinary_service = CloudinaryService()
