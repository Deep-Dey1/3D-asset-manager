from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Model3D, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get recent public models
    recent_models = Model3D.query.filter_by(is_public=True).order_by(Model3D.upload_date.desc()).limit(6).all()
    total_models = Model3D.query.filter_by(is_public=True).count()
    total_users = User.query.count()
    
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
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Model3D.query.filter_by(is_public=True)
    
    if search:
        query = query.filter(
            (Model3D.name.contains(search)) | 
            (Model3D.description.contains(search))
        )
    
    models = query.order_by(Model3D.upload_date.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('browse.html', models=models, search=search)

@main_bp.route('/model/<int:model_id>')
def model_detail(model_id):
    model = Model3D.query.get_or_404(model_id)
    
    # Check if model is public or belongs to current user
    if not model.is_public and (not current_user.is_authenticated or model.user_id != current_user.id):
        flash('Model not found.', 'error')
        return redirect(url_for('main.browse'))
    
    return render_template('model_detail.html', model=model)

@main_bp.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
