from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models import Model3D, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    try:
        # Get recent public models with error handling
        recent_models = Model3D.query.filter_by(is_public=True).order_by(Model3D.upload_date.desc()).limit(6).all()
        total_models = Model3D.query.filter_by(is_public=True).count()
        total_users = User.query.count()
    except Exception as e:
        print(f"Index page error: {e}")
        # Fallback values if database query fails
        recent_models = []
        total_models = 0
        total_users = 0
    
    return render_template('index.html', 
                         recent_models=recent_models,
                         total_models=total_models,
                         total_users=total_users)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    user_models = Model3D.query.filter_by(user_id=current_user.id).order_by(Model3D.upload_date.desc()).all()
    total_downloads = sum(model.downloads for model in user_models)
    
    return render_template('dashboard.html', 
                         user_models=user_models,
                         total_downloads=total_downloads)

@main_bp.route('/browse')
def browse():
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')
        
        # Start with all public models
        query = Model3D.query.filter_by(is_public=True)
        
        if search:
            query = query.filter(
                or_(
                    Model3D.name.ilike(f'%{search}%'),
                    Model3D.description.ilike(f'%{search}%')
                )
            )
        
        # Get paginated results with error handling
        try:
            models = query.order_by(Model3D.upload_date.desc()).paginate(
                page=page, per_page=12, error_out=False
            )
        except Exception as e:
            # If pagination fails, create empty pagination object
            from flask_sqlalchemy import Pagination
            models = Pagination(query, page, 12, 0, [])
        
        return render_template('browse.html', models=models, search=search)
        
    except Exception as e:
        # Log the error and show a user-friendly message
        print(f"Browse page error: {e}")
        # Create empty pagination for template
        from flask_sqlalchemy import Pagination  
        models = Pagination(Model3D.query, 1, 12, 0, [])
        return render_template('browse.html', models=models, search='', error=str(e))

@main_bp.route('/model/<int:model_id>')
def model_detail(model_id):
    try:
        model = Model3D.query.get_or_404(model_id)
        
        # Check if model is public or belongs to current user
        if not model.is_public and (not current_user.is_authenticated or model.user_id != current_user.id):
            flash('Model not found.', 'error')
            return redirect(url_for('main.browse'))
        
        return render_template('model_detail.html', model=model)
    except Exception as e:
        print(f"Model detail error: {e}")
        flash('Model not found or an error occurred.', 'error')
        return redirect(url_for('main.browse'))

@main_bp.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@main_bp.route('/debug')
def debug():
    """Debug route to test database connectivity"""
    try:
        # Test basic database queries
        user_count = db.session.execute(db.text("SELECT COUNT(*) FROM users")).scalar()
        model_count = db.session.execute(db.text("SELECT COUNT(*) FROM model3d")).scalar()
        
        return {
            'status': 'ok',
            'users': user_count,
            'models': model_count,
            'database_uri': 'Connected successfully'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'database_uri': 'Connection failed'
        }

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
