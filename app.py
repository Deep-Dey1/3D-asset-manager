from app import create_app, db
from app.models import User, Model3D

app = create_app()

@app.before_first_request
def create_tables():
    """Create database tables"""
    db.create_all()

@app.shell_context_processor
def make_shell_context():
    """Shell context for flask shell"""
    return {'db': db, 'User': User, 'Model3D': Model3D}

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=app.config['PORT'])
