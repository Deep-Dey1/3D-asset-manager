@echo off
echo 🧪 3D Asset Manager API Testing Script
echo ======================================

set BASE_URL=http://127.0.0.1:5000
set API_BASE=%BASE_URL%/api

echo.
echo 📋 1. Testing API Models List
echo curl -X GET %API_BASE%/models
curl -X GET %API_BASE%/models
echo.

echo.
echo 🔐 2. Testing User Registration
echo curl -X POST %BASE_URL%/auth/register -d "username=testuser&email=test@example.com&password=testpass123"
curl -X POST %BASE_URL%/auth/register -d "username=testuser&email=test@example.com&password=testpass123"
echo.

echo.
echo 🔑 3. Testing User Login
echo curl -X POST %BASE_URL%/auth/login -d "username=testuser&password=testpass123" -c cookies.txt
curl -X POST %BASE_URL%/auth/login -d "username=testuser&password=testpass123" -c cookies.txt
echo.

echo.
echo 📥 4. Testing Model Download (ID: 1)
echo curl -X GET %API_BASE%/download/1 -b cookies.txt -o downloaded_model.glb
curl -X GET %API_BASE%/download/1 -b cookies.txt -o downloaded_model.glb
echo.

echo.
echo 👁️ 5. Testing Model View (ID: 1)  
echo curl -X GET %API_BASE%/view/1 -b cookies.txt -o preview_model.glb
curl -X GET %API_BASE%/view/1 -b cookies.txt -o preview_model.glb
echo.

echo.
echo 🎯 API Testing Complete!
echo Check the responses above for status codes and data.
echo Downloaded files: downloaded_model.glb, preview_model.glb
echo Session cookies saved in: cookies.txt

pause
