from flask import Blueprint, jsonify, current_app
from app import db
from app.models import User, Model3D
from sqlalchemy import text
import os

# Simple API test blueprint
test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/db')
def test_database():
    """Test database connectivity with simple queries"""
    try:
        # Test basic connection
        result = db.session.execute(text("SELECT 1 as test")).fetchone()
        
        # Test simple count queries
        user_count = db.session.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        model_count = db.session.execute(text("SELECT COUNT(*) FROM model3d")).scalar() or 0
        
        return jsonify({
            'status': 'success',
            'connection_test': result[0] if result else None,
            'user_count': user_count,
            'model_count': model_count,
            'database_url': 'Connected to PostgreSQL'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@test_bp.route('/models')
def test_models():
    """Test model queries specifically"""
    try:
        # Try basic Model3D query
        models = Model3D.query.limit(5).all()
        
        return jsonify({
            'status': 'success',
            'model_count': len(models),
            'models': [{
                'id': m.id,
                'name': m.name,
                'file_format': m.file_format,
                'is_public': m.is_public
            } for m in models]
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@test_bp.route('/simple')
def test_simple():
    """Test basic Flask functionality"""
    return jsonify({
        'status': 'success',
        'message': 'Flask app is working',
        'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'unknown')
    })
