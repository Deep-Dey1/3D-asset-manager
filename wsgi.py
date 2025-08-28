import os
from app import create_app, db
from app.models import User, Model3D

# Create the Flask app
try:
    app = create_app()
    print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
except Exception as e:
    print(f"Error creating app: {e}")
    # Create a minimal app for debugging
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fallback.db'
    app.config['SECRET_KEY'] = 'fallback-key'

@app.shell_context_processor
def make_shell_context():
    """Shell context for flask shell"""
    return {'db': db, 'User': User, 'Model3D': Model3D}

# Create database tables with error handling
try:
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
