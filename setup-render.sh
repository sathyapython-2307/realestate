#!/bin/bash
# Quick setup for Render deployment with Cloudinary

echo "Real Estate App - Render Deployment Setup"
echo "==========================================="
echo ""

# Step 1: Get Cloudinary URL
echo "Step 1: Set up Cloudinary"
echo "1. Go to https://cloudinary.com/users/register/free"
echo "2. Sign up for a free account"
echo "3. Copy your CLOUDINARY_URL from the dashboard"
echo ""
read -p "Paste your CLOUDINARY_URL: " CLOUDINARY_URL

# Step 2: Generate SECRET_KEY
echo ""
echo "Step 2: Generating SECRET_KEY..."
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
echo "Generated SECRET_KEY: $SECRET_KEY"
echo ""

# Step 3: Get deployment domain
echo "Step 3: Enter your Render app domain"
read -p "Enter your Render app URL (e.g., realestate-7sj9.onrender.com): " APP_DOMAIN

# Step 4: Instructions
echo ""
echo "==========================================="
echo "Setup Instructions for Render:"
echo "==========================================="
echo ""
echo "1. Go to your Render Dashboard"
echo "2. Click on your Web Service"
echo "3. Go to Environment → Add Environment Variables"
echo ""
echo "Add these variables:"
echo "---"
echo "CLOUDINARY_URL=$CLOUDINARY_URL"
echo "SECRET_KEY=$SECRET_KEY"
echo "DEBUG=False"
echo "ALLOWED_HOSTS=$APP_DOMAIN,www.$APP_DOMAIN"
echo "---"
echo ""
echo "4. Save and your app will auto-redeploy"
echo ""
echo "5. After deployment completes:"
echo "   - Visit your app URL"
echo "   - Try uploading a new property with images"
echo "   - Images should now appear correctly"
echo ""
echo "Done! Media files are now stored on Cloudinary."
