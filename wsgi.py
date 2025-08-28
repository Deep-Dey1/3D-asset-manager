import os
from app import create_app, db
from app.models import User, Model3D

# Debug: Print environment variables
print(f"DATABASE_URL environment variable: {os.environ.get('DATABASE_URL', 'NOT SET')}")
print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")

# Create the Flask app
try:
    app = create_app()
    print(f"App created successfully")
    print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
    
    # Test database connection
    with app.app_context():
        try:
            # Test if we can connect to the database
            db.session.execute(db.text("SELECT 1"))
            print("Database connection successful")
            
            # Create tables
            db.create_all()
            print("Database tables created successfully")
            
            # Verify tables exist
            result = db.session.execute(db.text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print(f"Tables in database: {tables}")
            
        except Exception as db_error:
            print(f"Database error: {db_error}")
            # Try alternative table creation
            try:
                db.drop_all()
                db.create_all()
                print("Database tables recreated successfully")
            except Exception as recreate_error:
                print(f"Failed to recreate tables: {recreate_error}")
                
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
