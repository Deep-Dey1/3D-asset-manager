"""
Simple test script to verify the deployment works
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def test_deployment():
    """Test basic deployment functionality"""
    try:
        print("🚀 Testing 3D Asset Manager Deployment...")
        
        # Create the app
        app = create_app()
        print("✅ Flask app created successfully")
        
        with app.app_context():
            # Test database connection
            try:
                db.session.execute(db.text("SELECT 1"))
                print("✅ Database connection successful")
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                return False
            
            # Test Cloudinary configuration
            try:
                cloud_name = app.config.get('CLOUDINARY_CLOUD_NAME')
                api_key = app.config.get('CLOUDINARY_API_KEY')
                if cloud_name and api_key:
                    print(f"✅ Cloudinary configured (Cloud: {cloud_name})")
                else:
                    print("⚠️ Cloudinary configuration missing")
            except Exception as e:
                print(f"⚠️ Cloudinary check failed: {e}")
            
            # Test database tables
            try:
                from app.models import User, Model3D
                
                # Check if tables exist
                users_count = User.query.count()
                models_count = Model3D.query.count()
                print(f"✅ Database tables accessible (Users: {users_count}, Models: {models_count})")
                
            except Exception as e:
                print(f"❌ Database tables error: {e}")
                return False
        
        print("\n🎉 Deployment test completed successfully!")
        print("Your 3D Asset Manager should be working properly.")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment test failed: {e}")
        return False

if __name__ == "__main__":
    test_deployment()
