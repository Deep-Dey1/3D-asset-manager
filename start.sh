#!/bin/bash

# Railway startup script for 3D Asset Manager
echo "🚀 Starting 3D Asset Manager on Railway..."

# Print environment info
echo "📊 Environment Variables:"
echo "  - PORT: ${PORT:-5000}"
echo "  - DATABASE_URL: ${DATABASE_URL:0:20}..." 
echo "  - UPLOAD_PATH: ${UPLOAD_PATH:-/app/data/uploads}"
echo "  - RAILWAY_ENVIRONMENT: ${RAILWAY_ENVIRONMENT:-development}"

# Create upload directory
echo "📁 Setting up upload directory..."
mkdir -p "${UPLOAD_PATH:-/app/data/uploads}"
chmod 755 "${UPLOAD_PATH:-/app/data/uploads}"

# Verify directory exists
if [ -d "${UPLOAD_PATH:-/app/data/uploads}" ]; then
    echo "✅ Upload directory created: ${UPLOAD_PATH:-/app/data/uploads}"
else
    echo "❌ Failed to create upload directory"
    exit 1
fi

# Start the Flask application
echo "🎯 Starting Flask application..."
exec python wsgi.py
