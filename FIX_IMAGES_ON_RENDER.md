# Fix: Images Not Showing on Render

## Problem
Your property images show as 404 errors on Render because:
- Render has an **ephemeral filesystem** - files are deleted when the app restarts/redeploys
- `/media/` folder is not persistent storage

## Solution Implemented ✅

We've configured **Cloudinary** (free cloud storage) for media files:

### Changes Made:

1. **Updated `settings.py`**:
   - Added `cloudinary` and `cloudinary_storage` to INSTALLED_APPS
   - Configured to use Cloudinary when `CLOUDINARY_URL` environment variable is set
   - Falls back to local storage for development

2. **Updated `requirements.txt`**:
   - Added `cloudinary>=1.36.0`
   - Added `django-cloudinary-storage>=0.3.0`

3. **Created Setup Guides**:
   - `MEDIA_STORAGE_SETUP.md` - Comprehensive setup guide
   - `setup-render.ps1` - Windows setup script
   - `setup-render.sh` - Linux/Mac setup script

## Quick Fix (3 Steps)

### Step 1: Create Cloudinary Account
- Go to https://cloudinary.com/users/register/free
- Sign up (free - 25GB storage included)
- Copy your **CLOUDINARY_URL** from the dashboard

### Step 2: Add Environment Variables to Render
In your Render dashboard:
1. Go to your Web Service
2. Click "Environment"
3. Add these variables:
   - `CLOUDINARY_URL=cloudinary://...` (from Step 1)
   - `DEBUG=False`
   - `SECRET_KEY=<strong-random-key>`
   - `ALLOWED_HOSTS=realestate-7sj9.onrender.com,www.realestate-7sj9.onrender.com`

### Step 3: Deploy
```bash
git add .
git commit -m "Configure Cloudinary for media storage"
git push
```

## Verify It Works

After deployment (2-3 minutes):
1. Visit your app
2. Upload a new property with images
3. Images should appear correctly
4. Old images from before setup won't show (lost due to ephemeral filesystem) - users must re-upload

## How It Works

```
Local Development:
  Upload Image → /media/ folder → Display locally

Production (Render):
  Upload Image → Cloudinary → CDN URL → Display from CDN
```

## Alternative Cloud Storage

If you want to use AWS S3, Google Cloud Storage, or Azure instead:
1. Install `django-storages[s3]` (or equivalent)
2. Update settings
3. Add provider credentials to environment variables
4. Same deployment process

## Troubleshooting

**Images still show 404?**
- Wait 2-3 minutes after deploying
- Refresh browser (hard refresh: Ctrl+Shift+R)
- Check Cloudinary account is not full (25GB free limit)

**Upload errors?**
- Check image file size < 100MB
- Check CLOUDINARY_URL is exact copy from Cloudinary dashboard
- Redeploy after changing environment variables

**Need help?**
- Check Cloudinary dashboard → Media Library to see uploaded files
- Read `MEDIA_STORAGE_SETUP.md` for detailed guide
