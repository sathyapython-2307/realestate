# Media Storage Setup for Render Deployment

## Problem
Render has an **ephemeral filesystem** - files uploaded to `/media/` are deleted when the app restarts or redeploys. This is why property images (and other media) disappear.

## Solution: Cloudinary

We've configured **Cloudinary** (free tier with 25GB storage) for media file storage.

## Setup Steps

### 1. Create Cloudinary Account
- Go to https://cloudinary.com/users/register/free
- Sign up (free account)
- Copy your **CLOUDINARY_URL** from the dashboard

### 2. Set Environment Variables on Render
In your Render dashboard:

1. Go to your Web Service
2. Click "Environment" → "Add Environment Variable"
3. Add these variables:

```
CLOUDINARY_URL=cloudinary://your-api-key:your-api-secret@your-cloud-name
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=your-app.onrender.com,www.your-app.com
```

### 3. Deploy
```bash
git add .
git commit -m "Configure Cloudinary for media storage"
git push
```

Render will automatically:
- Install `django-cloudinary-storage` and `cloudinary`
- Configure media uploads to go to Cloudinary
- Regenerate static files

## Verification

After deployment:
1. Go to your app
2. Upload a new property with images
3. Images should now appear correctly
4. Check Cloudinary dashboard → Media Library to see uploaded files

## How It Works

- **Local Development**: Files saved to `/media/` folder (unchanged)
- **Production (Render)**: Files automatically uploaded to Cloudinary via CLOUDINARY_URL
- **Static Files**: Still served by WhiteNoise locally or Cloudinary URL in production

## Features

✅ Free tier: 25GB storage  
✅ Automatic image optimization  
✅ CDN delivery (fast worldwide)  
✅ Image transformation (resize, crop, compress)  
✅ Automatic cleanup of old versions  
✅ Works with all major hosting platforms  

## Optional: Advanced Cloudinary Features

Once images are working, you can enable:

1. **Auto image optimization** - Automatically compress and optimize images
2. **Responsive images** - Serve different sizes for different devices
3. **Image transformations** - Crop, resize, apply filters in templates

Example in template:
```html
<!-- Optimize image on the fly -->
<img src="{{ image.image.url }}/c_fill,w_400,h_300,q_auto:best" alt="Property">
```

## Troubleshooting

### Images still not showing (404 errors)
- Verify CLOUDINARY_URL is set correctly
- Check no special characters are escaped incorrectly
- Redeploy after changing environment variables
- Wait 2-3 minutes for cache to clear

### Old images from before setup don't show
- These were saved locally and are lost (Render ephemeral filesystem)
- Users need to re-upload images
- Or migrate images to Cloudinary separately

### Upload errors
- Check Cloudinary free tier storage limit (25GB)
- Verify image file size < 100MB
- Check CLOUDINARY_URL format

## Switching Away from Cloudinary

If you want to use AWS S3, Google Cloud Storage, or Azure:

1. Install appropriate package: `django-storages[s3]` or equivalent
2. Update `settings.py` with credentials
3. Update environment variables
4. Re-deploy

All code is already structured to support this.
