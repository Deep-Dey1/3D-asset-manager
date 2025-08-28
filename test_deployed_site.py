import requests
import json

# Test the deployed Railway site APIs
BASE_URL = "https://3d-asset-manager.deepdey.me"
API_BASE = f"{BASE_URL}/api"

def test_deployed_apis():
    """Test the deployed site's API endpoints"""
    
    print("🚀 Testing Deployed 3D Asset Manager APIs")
    print("="*50)
    print(f"Site URL: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    print("="*50)
    
    # Test 1: Get models list
    print("\n📋 Testing GET /api/models")
    try:
        response = requests.get(f"{API_BASE}/models", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {data.get('total', 0)} models")
            if 'models' in data and data['models']:
                print(f"Sample model: {data['models'][0].get('name', 'Unknown')}")
            else:
                print("No models found in database")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test 2: Check if a specific model exists for download test
    print("\n📥 Testing GET /api/download/1")
    try:
        response = requests.get(f"{API_BASE}/download/1", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Download working! File size: {len(response.content)} bytes")
        elif response.status_code == 404:
            print("ℹ️ No model with ID 1 found (expected for new site)")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test 3: Check site health
    print("\n🏠 Testing Homepage")
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Homepage loading successfully")
            # Check for key features
            content = response.text.lower()
            features = ["upload", "download", "api", "3d model"]
            found_features = [f for f in features if f in content]
            print(f"Features found: {', '.join(found_features)}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test 4: Test registration page
    print("\n🔐 Testing Registration Page")
    try:
        response = requests.get(f"{BASE_URL}/auth/register", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Registration page accessible")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    print("\n🎯 Deployed Site Testing Complete!")
    print(f"Visit your site: {BASE_URL}")

if __name__ == "__main__":
    test_deployed_apis()
