import requests
import json
import os
from pathlib import Path

# API Configuration
BASE_URL = "http://127.0.0.1:5000"
API_BASE = f"{BASE_URL}/api"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_data = {
            "username": "testuser_api",
            "email": "testuser@example.com", 
            "password": "testpassword123"
        }
        
    def print_response(self, response, title):
        """Helper to print formatted API responses"""
        print(f"\n{'='*50}")
        print(f"🧪 {title}")
        print(f"{'='*50}")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            json_data = response.json()
            print(f"Response JSON:\n{json.dumps(json_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
        print(f"{'='*50}")
        
    def test_registration(self):
        """Test user registration"""
        print("🔐 Testing User Registration...")
        
        response = self.session.post(
            f"{BASE_URL}/auth/register",
            data=self.user_data,
            allow_redirects=False
        )
        
        self.print_response(response, "User Registration")
        return response.status_code in [200, 302]  # Success or redirect
        
    def test_login(self):
        """Test user login"""
        print("🔑 Testing User Login...")
        
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }
        
        response = self.session.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            allow_redirects=False
        )
        
        self.print_response(response, "User Login")
        
        # Check if login was successful (redirect to dashboard)
        if response.status_code == 302:
            print("✅ Login successful (redirected)")
            return True
        return False
        
    def test_api_models_list(self):
        """Test GET /api/models endpoint"""
        print("📋 Testing API Models List...")
        
        response = self.session.get(f"{API_BASE}/models")
        self.print_response(response, "API Models List")
        
        return response.status_code == 200
        
    def test_file_upload(self):
        """Test model file upload"""
        print("📤 Testing Model Upload...")
        
        # Create a simple test GLB file (minimal valid GLB)
        test_file_path = "test_model.glb"
        
        # Create a minimal GLB file for testing
        glb_content = self.create_minimal_glb()
        
        with open(test_file_path, 'wb') as f:
            f.write(glb_content)
            
        # Upload the file
        upload_data = {
            'name': 'Test API Model',
            'description': 'A test model uploaded via API',
            'is_public': 'true',
            'file_format': 'glb'
        }
        
        files = {
            'file': (test_file_path, open(test_file_path, 'rb'), 'model/gltf-binary')
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/upload",
                data=upload_data,
                files=files,
                allow_redirects=False
            )
            
            self.print_response(response, "Model Upload")
            
            # Clean up test file
            os.remove(test_file_path)
            
            return response.status_code in [200, 302]
            
        except Exception as e:
            print(f"❌ Upload error: {e}")
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
            return False
            
    def create_minimal_glb(self):
        """Create a minimal valid GLB file for testing"""
        # GLB file header (minimal valid structure)
        glb_header = bytearray([
            0x67, 0x6C, 0x54, 0x46,  # magic: "glTF"
            0x02, 0x00, 0x00, 0x00,  # version: 2
            0x4C, 0x00, 0x00, 0x00,  # length: 76 bytes
            0x2C, 0x00, 0x00, 0x00,  # JSON chunk length: 44 bytes
            0x4A, 0x53, 0x4F, 0x4E   # chunk type: "JSON"
        ])
        
        # Minimal JSON content
        json_content = '{"asset":{"version":"2.0"},"scenes":[{}]}'
        json_bytes = json_content.encode('utf-8')
        
        # Pad JSON to 4-byte boundary
        while len(json_bytes) % 4 != 0:
            json_bytes += b' '
            
        return glb_header + json_bytes
        
    def test_model_download(self, model_id=1):
        """Test model download"""
        print(f"📥 Testing Model Download (ID: {model_id})...")
        
        response = self.session.get(
            f"{API_BASE}/download/{model_id}",
            allow_redirects=False
        )
        
        self.print_response(response, f"Model Download (ID: {model_id})")
        
        if response.status_code == 200:
            print(f"✅ Download successful - File size: {len(response.content)} bytes")
            
            # Save downloaded file for verification
            with open(f"downloaded_model_{model_id}.glb", 'wb') as f:
                f.write(response.content)
            print(f"💾 Downloaded file saved as: downloaded_model_{model_id}.glb")
            
        return response.status_code == 200
        
    def test_model_view(self, model_id=1):
        """Test model view/preview"""
        print(f"👁️ Testing Model View (ID: {model_id})...")
        
        response = self.session.get(
            f"{API_BASE}/view/{model_id}",
            allow_redirects=False
        )
        
        self.print_response(response, f"Model View (ID: {model_id})")
        return response.status_code == 200
        
    def run_all_tests(self):
        """Run comprehensive API tests"""
        print("🚀 Starting 3D Asset Manager API Tests")
        print("="*60)
        
        results = {}
        
        # Test registration
        results['registration'] = self.test_registration()
        
        # Test login  
        results['login'] = self.test_login()
        
        # Test API endpoints
        results['models_list'] = self.test_api_models_list()
        
        # Test file upload
        results['upload'] = self.test_file_upload()
        
        # Test download (try model ID 1)
        results['download'] = self.test_model_download(1)
        
        # Test view/preview
        results['view'] = self.test_model_view(1)
        
        # Print summary
        print("\n🎯 TEST RESULTS SUMMARY")
        print("="*40)
        for test_name, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED" 
            print(f"{test_name.upper()}: {status}")
            
        total_tests = len(results)
        passed_tests = sum(results.values())
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
        
        return results

if __name__ == "__main__":
    # Run the API tests
    tester = APITester()
    results = tester.run_all_tests()
    
    print(f"\n🎉 API Testing Complete!")
    print(f"Server running at: {BASE_URL}")
    print(f"API endpoints: {API_BASE}")
