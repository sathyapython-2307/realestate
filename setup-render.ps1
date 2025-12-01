# PowerShell setup for Render deployment with Cloudinary
# Run: powershell -ExecutionPolicy Bypass -File setup-render.ps1

Write-Host "Real Estate App - Render Deployment Setup" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Get Cloudinary URL
Write-Host "Step 1: Set up Cloudinary" -ForegroundColor Yellow
Write-Host "1. Go to https://cloudinary.com/users/register/free"
Write-Host "2. Sign up for a free account"
Write-Host "3. Copy your CLOUDINARY_URL from the dashboard"
Write-Host ""
$CLOUDINARY_URL = Read-Host "Paste your CLOUDINARY_URL"

# Step 2: Generate SECRET_KEY
Write-Host ""
Write-Host "Step 2: Generating SECRET_KEY..." -ForegroundColor Yellow

# Generate a random secret key
$SECRET_KEY = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | ForEach-Object {[char]$_})
Write-Host "Generated SECRET_KEY: $SECRET_KEY" -ForegroundColor Green
Write-Host ""

# Step 3: Get deployment domain
Write-Host "Step 3: Enter your Render app domain" -ForegroundColor Yellow
$APP_DOMAIN = Read-Host "Enter your Render app URL (e.g., realestate-7sj9.onrender.com)"

# Step 4: Instructions
Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Setup Instructions for Render:" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to your Render Dashboard"
Write-Host "2. Click on your Web Service"
Write-Host "3. Go to Environment → Add Environment Variables"
Write-Host ""
Write-Host "Add these variables:" -ForegroundColor Yellow
Write-Host "---"
Write-Host "CLOUDINARY_URL=$CLOUDINARY_URL"
Write-Host "SECRET_KEY=$SECRET_KEY"
Write-Host "DEBUG=False"
Write-Host "ALLOWED_HOSTS=$APP_DOMAIN,www.$APP_DOMAIN"
Write-Host "---"
Write-Host ""
Write-Host "4. Save and your app will auto-redeploy"
Write-Host ""
Write-Host "5. After deployment completes:" -ForegroundColor Green
Write-Host "   - Visit your app URL"
Write-Host "   - Try uploading a new property with images"
Write-Host "   - Images should now appear correctly"
Write-Host ""
Write-Host "Done! Media files are now stored on Cloudinary." -ForegroundColor Green
