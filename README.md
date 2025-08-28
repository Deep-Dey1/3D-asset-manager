# 3D Asset Manager

A professional Python Flask web application for managing 3D models with upload/download capabilities, user authentication, and RESTful API. Designed for Railway deployment with PostgreSQL database.

## 🚀 Features

- **User Authentication**: Register/login with username or email (no OTP required)
- **3D Model Upload**: Support for multiple formats (OBJ, FBX, GLTF, GLB, DAE, 3DS, PLY, STL)
- **File Management**: Public/private model sharing with download tracking
- **RESTful API**: Complete API for developers and integrations
- **Professional UI**: Modern, responsive design with Tailwind CSS
- **Railway Ready**: Configured for easy Railway deployment

## 📋 Supported File Formats

- **OBJ** - Wavefront OBJ files
- **FBX** - Autodesk FBX files
- **GLTF/GLB** - GL Transmission Format
- **DAE** - COLLADA files
- **3DS** - 3D Studio Max files
- **PLY** - Stanford Triangle Format
- **STL** - Stereolithography files

## 🛠 Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL (Railway)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Authentication**: Flask-Login
- **File Handling**: Werkzeug, Python-Magic
- **Deployment**: Railway, Gunicorn

## 🚀 Railway Deployment

### Prerequisites
1. Railway account
2. GitHub repository with this code

### Deployment Steps

1. **Connect to Railway**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Initialize project
   railway init
   ```

2. **Add PostgreSQL Database**:
   - Go to Railway dashboard
   - Add PostgreSQL service to your project
   - Copy the DATABASE_URL from the PostgreSQL service

3. **Set Environment Variables**:
   ```bash
   railway variables set SECRET_KEY=your-secret-key-here
   railway variables set FLASK_ENV=production
   railway variables set DATABASE_URL=your-postgresql-url
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

### Railway Configuration Files

- `Procfile`: Defines how to run the app
- `runtime.txt`: Specifies Python version
- `requirements.txt`: Lists all dependencies

## 🔧 Local Development

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd 3d-asset-manager
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

Visit `http://localhost:5000` to access the application.

## 📚 API Documentation

### Authentication Endpoints

- `POST /auth/register` - Create new user account
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Model Management API

- `GET /api/models` - List all public models
- `POST /api/upload` - Upload new 3D model (requires authentication)
- `GET /api/download/{id}` - Download model file
- `GET /api/model/{id}` - Get model details
- `DELETE /api/model/{id}` - Delete model (owner only)
- `GET /api/stats` - Platform statistics

### API Usage Examples

**Upload a model**:
```bash
curl -X POST http://your-app.railway.app/api/upload \
  -F "file=@model.obj" \
  -F "name=My 3D Model" \
  -F "description=A beautiful 3D model" \
  -F "is_public=true"
```

**List models**:
```bash
curl http://your-app.railway.app/api/models?page=1&per_page=10
```

**Download a model**:
```bash
curl -O http://your-app.railway.app/api/download/1
```

## 🗂 Project Structure

```
3d-asset-manager/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── auth.py              # Authentication routes
│   ├── main.py              # Main application routes
│   ├── api.py               # RESTful API endpoints
│   └── templates/           # HTML templates
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       ├── dashboard.html   # User dashboard
│       ├── upload.html      # File upload page
│       └── auth/            # Authentication templates
├── uploads/                 # File storage directory
├── app.py                   # Application entry point
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway deployment config
├── runtime.txt              # Python version specification
└── .env.example             # Environment variables template
```

## 🔐 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- File type validation
- CSRF protection ready
- Secure file uploads

## 📱 User Interface

- **Responsive Design**: Works on desktop and mobile
- **Modern UI**: Clean, professional interface
- **Drag & Drop**: Easy file upload experience
- **Real-time Feedback**: Upload progress and status updates
- **Professional Navigation**: Intuitive user experience

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For deployment issues or questions:
- Check Railway documentation
- Review the logs: `railway logs`
- Ensure all environment variables are set correctly

---

**Built with ❤️ for the 3D community**
