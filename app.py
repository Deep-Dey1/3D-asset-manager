import os
from app import create_app, db
from app.models import User, Model3D

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Shell context for flask shell"""
    return {'db': db, 'User': User, 'Model3D': Model3D}

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
