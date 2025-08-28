from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
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
    """Simplified dashboard route"""
    try:
        user_models = Model3D.query.filter_by(user_id=current_user.id).order_by(Model3D.upload_date.desc()).all()
        total_downloads = sum(model.downloads for model in user_models) if user_models else 0
        
        return render_template('dashboard.html', 
                             user_models=user_models,
                             total_downloads=total_downloads)
    except Exception as e:
        print(f"Dashboard error: {e}")
        return render_template('dashboard.html', 
                             user_models=[],
                             total_downloads=0,
                             error=str(e))

@main_bp.route('/browse')
def browse():
    """Simplified browse route with minimal complexity"""
    try:
        # Get search parameter
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)
        
        # Very simple query without complex filtering
        models_query = Model3D.query.filter_by(is_public=True)
        
        # Apply search only if provided and not empty
        if search and search.strip():
            search_term = f'%{search}%'
            models_query = models_query.filter(
                Model3D.name.ilike(search_term)
            )
        
        # Get models with simple pagination
        models = models_query.order_by(Model3D.upload_date.desc()).paginate(
            page=page, 
            per_page=12, 
            error_out=False
        )
        
        # Render template with error handling
        return render_template('browse.html', models=models, search=search)
        
    except Exception as e:
        # If anything fails, show empty browse page
        print(f"Browse error: {e}")
        # Create empty pagination manually
        class EmptyPagination:
            items = []
            pages = 0
            page = 1
            total = 0
            has_prev = False
            has_next = False
            per_page = 12
            
        empty_models = EmptyPagination()
        return render_template('browse.html', models=empty_models, search='', error=f"Database error: {str(e)}")

@main_bp.route('/model/<int:model_id>')
def model_detail(model_id):
    """Simplified model detail route"""
    try:
        # Simple model query
        model = Model3D.query.get(model_id)
        
        if not model:
            flash('Model not found.', 'error')
            return redirect(url_for('main.browse'))
        
        # Check visibility
        if not model.is_public:
            if not current_user.is_authenticated or model.user_id != current_user.id:
                flash('Model not found.', 'error')
                return redirect(url_for('main.browse'))
        
        return render_template('model_detail.html', model=model)
        
    except Exception as e:
        print(f"Model detail error: {e}")
        flash(f'Error loading model: {str(e)}', 'error')
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
