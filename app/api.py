import os
import uuid
from flask import Blueprint, request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Model3D, User

api_bp = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

@api_bp.route('/upload', methods=['POST'])
@login_required
def upload_model():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        is_public = request.form.get('is_public', 'true').lower() == 'true'
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        if not name:
            name = file.filename.rsplit('.', 1)[0]
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = get_file_extension(original_filename)
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Ensure upload folder exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_folder, unique_filename)
        
        print(f"Saving file to: {file_path}")
        print(f"Upload folder: {upload_folder}")
        print(f"Railway environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'development')}")
        
        file.save(file_path)
        
        # Verify file was saved
        if not os.path.exists(file_path):
            return jsonify({'error': 'Failed to save file to server'}), 500
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create database record
        model = Model3D(
            name=name,
            description=description,
            filename=unique_filename,
            original_filename=original_filename,
            file_size=file_size,
            file_extension=file_extension,
            is_public=is_public,
            user_id=current_user.id
        )
        
        db.session.add(model)
        db.session.commit()
        
        return jsonify({
            'message': 'File uploaded successfully',
            'model': model.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/download/<int:model_id>')
def download_model(model_id):
    try:
        model = Model3D.query.get(model_id)
        
        if not model:
            return jsonify({'error': 'Model not found'}), 404
        
        # Check if model is public or belongs to current user
        if not model.is_public:
            if not current_user.is_authenticated or model.user_id != current_user.id:
                return jsonify({'error': 'Access denied'}), 403
        
        # Ensure upload folder exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, model.filename)
        
        if not os.path.exists(file_path):
            print(f"Download: File not found at path: {file_path}")
            print(f"Upload folder: {upload_folder}")
            print(f"Model filename: {model.filename}")
            print(f"Files in upload folder: {os.listdir(upload_folder) if os.path.exists(upload_folder) else 'Upload folder does not exist'}")
            return jsonify({'error': 'File not found on server - may have been lost during deployment'}), 404
        
        # Increment download count
        model.downloads += 1
        db.session.commit()
        
        return send_file(file_path, 
                        download_name=model.original_filename,
                        as_attachment=True)
        
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@api_bp.route('/view/<int:model_id>')
def view_model(model_id):
    """Serve model file for 3D viewing (not as download)"""
    try:
        model = Model3D.query.get(model_id)
        
        if not model:
            return jsonify({'error': 'Model not found'}), 404
        
        # Check if model is public or belongs to current user
        if not model.is_public:
            if not current_user.is_authenticated or model.user_id != current_user.id:
                return jsonify({'error': 'Access denied'}), 403
        
        # Ensure upload folder exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            return jsonify({'error': 'Upload folder not found'}), 404
        
        file_path = os.path.join(upload_folder, model.filename)
        
        if not os.path.exists(file_path):
            print(f"View: File not found at path: {file_path}")
            print(f"Upload folder: {upload_folder}")
            print(f"Model filename: {model.filename}")
            print(f"Files in upload folder: {os.listdir(upload_folder) if os.path.exists(upload_folder) else 'Upload folder does not exist'}")
            return jsonify({'error': 'File not found on server - may have been lost during deployment'}), 404
        
        # Determine MIME type based on file extension
        file_extension = model.file_extension.lower()
        mime_types = {
            'glb': 'model/gltf-binary',
            'gltf': 'application/json',
            'obj': 'text/plain',
            'fbx': 'application/octet-stream',
            'dae': 'application/xml',
            '3ds': 'application/octet-stream',
            'ply': 'application/octet-stream',
            'stl': 'application/octet-stream'
        }
        
        mimetype = mime_types.get(file_extension, 'application/octet-stream')
        
        # Serve file for viewing (not download) with proper headers
        return send_file(file_path, 
                        as_attachment=False,
                        mimetype=mimetype,
                        download_name=model.original_filename)
        
    except Exception as e:
        print(f"View error: {e}")
        return jsonify({'error': f'View failed: {str(e)}'}), 500

@api_bp.route('/models')
def list_models():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        user_only = request.args.get('user_only', 'false').lower() == 'true'
        
        query = Model3D.query
        
        if user_only and current_user.is_authenticated:
            query = query.filter_by(user_id=current_user.id)
        else:
            query = query.filter_by(is_public=True)
        
        if search:
            query = query.filter(
                (Model3D.name.contains(search)) | 
                (Model3D.description.contains(search))
            )
        
        models = query.order_by(Model3D.upload_date.desc()).paginate(
            page=page, per_page=min(per_page, 100), error_out=False
        )
        
        return jsonify({
            'models': [model.to_dict() for model in models.items],
            'total': models.total,
            'page': models.page,
            'pages': models.pages,
            'per_page': models.per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/model/<int:model_id>')
def get_model(model_id):
    try:
        model = Model3D.query.get_or_404(model_id)
        
        # Check if model is public or belongs to current user
        if not model.is_public and (not current_user.is_authenticated or model.user_id != current_user.id):
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'model': model.to_dict()})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/model/<int:model_id>', methods=['DELETE'])
@login_required
def delete_model(model_id):
    try:
        model = Model3D.query.get_or_404(model_id)
        
        # Check if model belongs to current user
        if model.user_id != current_user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Delete file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], model.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete database record
        db.session.delete(model)
        db.session.commit()
        
        return jsonify({'message': 'Model deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stats')
def get_stats():
    try:
        total_models = Model3D.query.filter_by(is_public=True).count()
        total_users = User.query.count()
        total_downloads = db.session.query(db.func.sum(Model3D.downloads)).scalar() or 0
        
        return jsonify({
            'total_models': total_models,
            'total_users': total_users,
            'total_downloads': total_downloads
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
