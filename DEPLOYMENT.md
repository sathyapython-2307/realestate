# Deployment Guide

This Real Estate application is ready for deployment on Heroku, Railway, Render, or similar platforms.

## Deployment Files

- **Procfile** - Specifies how to run the application and perform migrations
- **runtime.txt** - Specifies Python version for the platform
- **requirements.txt** - All Python dependencies with pinned versions

## Pre-Deployment Checklist

### 1. Environment Variables
Create a `.env` file with these variables (or set them in your platform's dashboard):

```
SECRET_KEY=<generate-a-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app.herokuapp.com,www.your-app.com
DATABASE_URL=<your-database-url>
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Generate a strong SECRET_KEY using:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. Static Files
- WhiteNoise middleware is configured in `settings.py`
- Static files are automatically collected during deployment
- No separate static file service needed

### 3. Database Setup
For PostgreSQL deployment:
```bash
pip install psycopg2-binary
```

Update `settings.py` database configuration:
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}
```

## Deployment Steps

### For Heroku:
```bash
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
git push heroku main
```

### For Railway:
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Set the start command to: `gunicorn realestate.wsgi:application`

### For Render:
1. Create new Web Service
2. Connect GitHub repository
3. Set environment variables
4. Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
5. Start command: `gunicorn realestate.wsgi:application`

## Post-Deployment

1. Create a superuser:
```bash
python manage.py createsuperuser
```

2. Access admin panel at `/admin`

3. Configure email settings for password reset functionality

## Media Files
For production, configure a cloud storage service:
- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Cloudinary

Update `settings.py` to use django-storages for production.

## Troubleshooting

### Static files not loading:
- Ensure `DEBUG=False` and `ALLOWED_HOSTS` includes your domain
- WhiteNoise middleware must be first in MIDDLEWARE list
- Run `python manage.py collectstatic --noinput` locally to test

### Database connection errors:
- Verify DATABASE_URL format
- Ensure database is created and accessible
- Check firewall/security group settings

### Email not working:
- Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- For Gmail: use an App Password, not your regular password
- Check email backend configuration

## Security Recommendations

1. Always use HTTPS in production
2. Set `SECURE_SSL_REDIRECT = True` when using HTTPS
3. Use strong SECRET_KEY (minimum 50 characters)
4. Never commit `.env` files to git
5. Use environment variables for all sensitive data
6. Set `CSRF_COOKIE_SECURE = True` for HTTPS
7. Set `SESSION_COOKIE_SECURE = True` for HTTPS
