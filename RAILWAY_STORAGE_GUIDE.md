# Railway Deployment Guide with Persistent Storage

## 🚀 Railway Deployment Steps

### 1. **Deploy to Railway**
```bash
# Connect your GitHub repo to Railway
# Railway will auto-detect the Python app
```

### 2. **Add Railway Volume Storage**

In your Railway project dashboard:

1. Go to **Settings** → **Volumes**
2. Click **"Add Volume"**
3. Configure:
   - **Name**: `3d-assets-storage`
   - **Mount Path**: `/app/data`
   - **Size**: `5GB` (or more based on your needs)

### 3. **Set Environment Variables**

In Railway dashboard → **Variables**:
```
UPLOAD_PATH=/app/data/uploads
DATABASE_URL=[Auto-set by Railway PostgreSQL]
SECRET_KEY=your-production-secret-key
RAILWAY_ENVIRONMENT=production
```

### 4. **Enable PostgreSQL**

1. Go to **Add Service** → **Database** → **PostgreSQL**
2. Railway will automatically set `DATABASE_URL`

## 📁 **File Storage Architecture**

### **Before (Ephemeral)**
```
/app/uploads/  ❌ Lost on redeploy
```

### **After (Persistent)**
```
/app/data/uploads/  ✅ Persists across redeploys
```

## 🔧 **Volume Configuration**

The `railway.toml` file configures:
- **Volume Mount**: `/app/data` → Persistent storage
- **Environment**: `UPLOAD_PATH=/app/data/uploads`
- **Auto-scaling**: Enabled for high traffic

## 🧪 **Testing Persistent Storage**

1. Upload a 3D model
2. Redeploy your application
3. Check if the model is still viewable/downloadable
4. ✅ Should work with persistent volume!

## 💡 **Alternative Solutions**

If Railway volumes don't work, consider:

1. **AWS S3** - Cloud object storage
2. **Cloudinary** - Media management API
3. **Google Cloud Storage** - Google's cloud storage
4. **Azure Blob Storage** - Microsoft's cloud storage

## 🐛 **Troubleshooting**

### **Check Volume Status**
```python
# In your app logs
print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
print(f"Directory exists: {os.path.exists(app.config['UPLOAD_FOLDER'])}")
```

### **Common Issues**
- **Volume not mounted**: Check Railway volume configuration
- **Permission denied**: Ensure proper volume permissions
- **Path not found**: Verify `UPLOAD_PATH` environment variable

## 📊 **Storage Monitoring**

Monitor your volume usage:
- Railway Dashboard → **Metrics** → **Storage**
- Set up alerts for storage limits
- Consider cleanup policies for old files
