from flask import Flask, render_template, render_template_string, request, jsonify, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Simple in-memory storage for demo (replace with database in production)
users = {}
models = []
current_user = None

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Asset Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center space-x-4">
                    <h1 class="text-2xl font-bold text-indigo-600">
                        <i class="fas fa-cube mr-2"></i>3D Asset Manager
                    </h1>
                </div>
                <div class="flex items-center space-x-6">
                    <a href="/browse" class="text-gray-700 hover:text-indigo-600">Browse</a>
                    <a href="/upload" class="text-gray-700 hover:text-indigo-600">Upload</a>
                    <a href="/login" class="text-gray-700 hover:text-indigo-600">Login</a>
                    <a href="/register" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">Register</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-20">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <h1 class="text-5xl font-bold mb-6">Professional 3D Asset Management</h1>
            <p class="text-xl mb-8 text-indigo-100">Upload, share, and download 3D models with ease. Deployed on Railway.</p>
            <div class="space-x-4">
                <a href="/register" class="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">Get Started</a>
                <a href="/browse" class="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-indigo-600">Browse Models</a>
            </div>
        </div>
    </section>

    <!-- Features -->
    <section class="py-16">
        <div class="max-w-7xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-center mb-12">Powerful Features</h2>
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div class="text-center">
                    <div class="bg-indigo-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-upload text-2xl text-indigo-600"></i>
                    </div>
                    <h3 class="text-lg font-semibold mb-2">Easy Upload</h3>
                    <p class="text-gray-600">Drag and drop your 3D models</p>
                </div>
                <div class="text-center">
                    <div class="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-download text-2xl text-green-600"></i>
                    </div>
                    <h3 class="text-lg font-semibold mb-2">Fast Download</h3>
                    <p class="text-gray-600">Download models instantly</p>
                </div>
                <div class="text-center">
                    <div class="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-code text-2xl text-purple-600"></i>
                    </div>
                    <h3 class="text-lg font-semibold mb-2">RESTful API</h3>
                    <p class="text-gray-600">Full API access for developers</p>
                </div>
                <div class="text-center">
                    <div class="bg-yellow-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-shield-alt text-2xl text-yellow-600"></i>
                    </div>
                    <h3 class="text-lg font-semibold mb-2">Secure Storage</h3>
                    <p class="text-gray-600">Railway PostgreSQL database</p>
                </div>
            </div>
        </div>
    </section>

    <!-- API Demo -->
    <section class="bg-gray-100 py-16">
        <div class="max-w-7xl mx-auto px-4">
            <div class="text-center mb-12">
                <h2 class="text-3xl font-bold mb-4">Developer Ready</h2>
                <p class="text-gray-600">Test the API endpoints below</p>
            </div>
            
            <div class="bg-white rounded-xl shadow-lg p-8">
                <div class="grid md:grid-cols-2 gap-8">
                    <div>
                        <h3 class="text-xl font-semibold mb-4">API Test</h3>
                        <button onclick="testAPI()" class="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700">
                            Test API Health
                        </button>
                        <div id="apiResult" class="mt-4 p-4 bg-gray-50 rounded-lg hidden">
                            <h4 class="font-semibold mb-2">API Response:</h4>
                            <pre id="apiOutput" class="text-sm text-gray-700"></pre>
                        </div>
                    </div>
                    <div>
                        <h3 class="text-xl font-semibold mb-4">Supported Formats</h3>
                        <div class="grid grid-cols-2 gap-3">
                            <div class="bg-gray-50 p-3 rounded-lg text-center">
                                <i class="fas fa-cube text-indigo-600 mb-1"></i>
                                <div class="text-sm font-mono">OBJ</div>
                            </div>
                            <div class="bg-gray-50 p-3 rounded-lg text-center">
                                <i class="fas fa-cube text-purple-600 mb-1"></i>
                                <div class="text-sm font-mono">FBX</div>
                            </div>
                            <div class="bg-gray-50 p-3 rounded-lg text-center">
                                <i class="fas fa-cube text-green-600 mb-1"></i>
                                <div class="text-sm font-mono">GLTF</div>
                            </div>
                            <div class="bg-gray-50 p-3 rounded-lg text-center">
                                <i class="fas fa-cube text-blue-600 mb-1"></i>
                                <div class="text-sm font-mono">GLB</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-8">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p>&copy; 2025 3D Asset Manager. Built with Flask & deployed on Railway.</p>
        </div>
    </footer>

    <script>
    async function testAPI() {
        const resultDiv = document.getElementById('apiResult');
        const outputDiv = document.getElementById('apiOutput');
        
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            outputDiv.textContent = JSON.stringify(data, null, 2);
            resultDiv.classList.remove('hidden');
        } catch (error) {
            outputDiv.textContent = 'Error: ' + error.message;
            resultDiv.classList.remove('hidden');
        }
    }
    </script>
</body>
</html>
    """, total_models=len(models), total_users=len(users))

@app.route('/api/health')
def api_health():
    return jsonify({
        'status': 'OK',
        'message': '3D Asset Manager API is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'deployed_on': 'Railway'
    })

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'total_models': len(models),
        'total_users': len(users),
        'total_downloads': sum(model.get('downloads', 0) for model in models),
        'supported_formats': ['obj', 'fbx', 'gltf', 'glb', 'dae', '3ds', 'ply', 'stl']
    })

@app.route('/register')
def register():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Register - 3D Asset Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <div class="min-h-screen flex items-center justify-center">
        <div class="max-w-md w-full bg-white p-8 rounded-xl shadow-lg">
            <h2 class="text-3xl font-bold text-center mb-8">Create Account</h2>
            <form method="POST" class="space-y-6">
                <input type="text" placeholder="Full Name" class="w-full px-3 py-3 border rounded-lg" required>
                <input type="text" placeholder="Username" class="w-full px-3 py-3 border rounded-lg" required>
                <input type="email" placeholder="Email" class="w-full px-3 py-3 border rounded-lg" required>
                <input type="password" placeholder="Password" class="w-full px-3 py-3 border rounded-lg" required>
                <button type="submit" class="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700">Create Account</button>
            </form>
            <p class="text-center mt-6"><a href="/" class="text-indigo-600">← Back to Home</a></p>
        </div>
    </div>
</body>
</html>
    """)

@app.route('/upload')
def upload():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Upload - 3D Asset Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 py-8">
        <div class="bg-white rounded-xl shadow-lg p-8">
            <h1 class="text-3xl font-bold mb-8">Upload 3D Model</h1>
            <form class="space-y-6">
                <input type="text" placeholder="Model Name" class="w-full px-3 py-3 border rounded-lg" required>
                <textarea placeholder="Description" rows="4" class="w-full px-3 py-3 border rounded-lg"></textarea>
                <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <i class="fas fa-cloud-upload-alt text-4xl text-gray-400 mb-4"></i>
                    <p class="text-gray-600 mb-2">Drag and drop your file here</p>
                    <input type="file" accept=".obj,.fbx,.gltf,.glb,.dae,.3ds,.ply,.stl" class="hidden">
                    <button type="button" class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">Choose File</button>
                    <p class="text-sm text-gray-500 mt-2">Supported: OBJ, FBX, GLTF, GLB, DAE, 3DS, PLY, STL</p>
                </div>
                <button type="submit" class="bg-indigo-600 text-white px-8 py-3 rounded-lg hover:bg-indigo-700">Upload Model</button>
            </form>
            <p class="text-center mt-6"><a href="/" class="text-indigo-600">← Back to Home</a></p>
        </div>
    </div>
</body>
</html>
    """)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
