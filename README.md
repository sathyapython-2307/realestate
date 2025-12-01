# RealEstate - OLX-Style Real Estate Buy & Sell Web Application

A comprehensive, fully-featured real estate marketplace web application built with Django, HTML, CSS, and Bootstrap. Users can post properties for sale, rent, or lease, browse listings with advanced filtering, and contact property owners directly.

## Features

### User Authentication
- User registration and signup with email validation
- Login/logout functionality with remember-me option
- Password reset via email
- User profile management

### Property Management
- Post properties with detailed information (price, location, bedrooms, bathrooms, area, etc.)
- Multiple image uploads per property (with primary image selection)
- Edit and delete your own properties
- Property details include amenities (parking, furnished, pool, gym, etc.)
- SEO-friendly URL slugs
- Property condition tracking (new, old, renovated)

### Property Browsing & Search
- Browse all active properties
- Advanced search filters:
  - Search by location, title, or description
  - Filter by listing type (sale, rent, lease)
  - Filter by property type (apartment, house, villa, etc.)
  - Filter by city
  - Price range filters
  - Bedroom/bathroom filters
  - Amenity filters (furnished, parking, etc.)
- Pagination with 12 properties per page
- Featured properties section on home page
- Similar properties recommendation on detail page

### Property Details
- Large gallery with thumbnail navigation
- Pricing section with clear display
- Quick details (bedrooms, bathrooms, area, photos)
- Full description and amenities listing
- Property owner information
- Contact form integration

### Contact & Inquiries
- Send inquiries to property owners
- Track inquiry status (pending, responded, completed, rejected)
- Inquiry types: general inquiry, booking request, schedule visit
- Update inquiry status as property owner
- View received and sent inquiries

### User Dashboard
- Dashboard with statistics (total properties, active, inquiries, pending)
- Manage posted properties (view, edit, delete)
- Manage received inquiries with status updates
- Quick access to all major features

### Favorites/Saved Properties
- Save properties to favorites
- View and manage saved properties
- Toggle favorite status with one click
- Pagination for saved properties

### Admin Panel
- Full Django admin interface
- Manage users, properties, inquiries, and favorites
- Property listing with filtering by type, status, city
- Inquiry management with status filtering
- Feature properties from admin panel

### Responsive Design
- Fully responsive Bootstrap-powered layouts
- Mobile-friendly navigation
- Optimized for all devices (desktop, tablet, mobile)
- Clean and modern UI with gradient headers
- Smooth transitions and hover effects

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Quick Start

1. **Navigate to project directory:**
   ```bash
   cd b:\intership-works\Realestate-v2
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   - Follow the prompts to enter username, email, and password

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Usage

### For Property Buyers/Renters:
1. Sign up for an account
2. Browse properties or use advanced filters
3. Save properties to favorites
4. Send inquiries to property owners
5. Track your inquiries in "My Inquiries"

### For Property Sellers/Landlords:
1. Sign up for an account
2. Click "Post Property" to list a property
3. Upload multiple images and fill in details
4. View inquiries in Dashboard or "Manage Inquiries"
5. Update inquiry status as needed
6. Edit or delete your properties anytime

### For Administrators:
1. Access admin panel at /admin/
2. Manage users, properties, and inquiries
3. Feature properties for homepage display
4. Monitor platform activity

## Project Structure

```
realestate/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── db.sqlite3               # SQLite database
├── realestate/              # Main project folder
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── properties/              # Main app folder
│   ├── migrations/          # Database migrations
│   ├── templates/
│   │   ├── base/
│   │   │   └── base.html    # Base template
│   │   ├── auth/            # Authentication templates
│   │   ├── properties/      # Property templates
│   │   └── errors/          # Error templates
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── admin.py             # Admin configuration
│   ├── apps.py
│   ├── forms.py             # Django forms
│   ├── models.py            # Database models
│   ├── urls.py              # App URL patterns
│   └── views.py             # View logic
└── media/                   # User uploaded files
    └── properties/
```

## Database Models

### User (Django built-in)
- Username, email, password
- First name, last name
- Date joined

### Property
- Title, description, slug
- Property type, listing type, condition
- Location details (address, city, state, postal code)
- Features (bedrooms, bathrooms, area, price)
- Amenities (furnished, parking, balcony, garden, pool, gym)
- Contact information (optional)
- Status (active, featured)
- Timestamps (created, updated)
- Relationship: owned by User

### PropertyImage
- Image file
- Primary flag (main image)
- Relationship: belongs to Property

### PropertyInquiry
- Sender, inquiry type, status
- Contact details (name, email, phone)
- Message
- Timestamps
- Relationship: Property and Sender (User)

### FavoriteProperty
- Relationship: User and Property
- Timestamp (added date)
- Unique together constraint

## Key URLs

| URL | Purpose |
|-----|---------|
| / | Home page |
| /properties/ | Browse properties |
| /property/<slug>/ | Property details |
| /signup/ | User registration |
| /login/ | User login |
| /logout/ | User logout |
| /password-reset/ | Password reset |
| /post-property/ | Create new property |
| /edit-property/<slug>/ | Edit property |
| /delete-property/<slug>/ | Delete property |
| /contact/<slug>/ | Send inquiry |
| /dashboard/ | User dashboard |
| /profile/ | User profile |
| /saved-properties/ | Saved/favorite properties |
| /my-inquiries/ | User's sent inquiries |
| /manage-inquiries/ | Received inquiries (for property owners) |
| /inquiry/<id>/ | View inquiry details |
| /admin/ | Django admin panel |

## Features Detailed

### Image Management
- Upload multiple images when posting a property
- Set any image as primary (cover image)
- Delete unwanted images
- All images displayed in detail page gallery

### Search & Filtering
- Real-time search by location, title, description
- Multiple filter combinations
- Price range selection
- Amenity-based filtering
- Property type filtering
- Listing type (sale/rent/lease) filtering

### Responsive UI
- Bootstrap 5 framework
- Mobile-first design
- Smooth animations and transitions
- Gradient headers and color-coded badges
- Sticky navigation
- Toast notifications for user feedback

### Admin Features
- Property management with bulk operations
- Inquiry status tracking
- User management
- Featured properties toggle
- Search and filtering across all models
- Read-only fields for timestamps

## Email Configuration

The application uses Django's email backend. By default, it's set to console output for development. To configure for production:

1. Update `EMAIL_BACKEND` in `settings.py`
2. Set up your email provider credentials:
   - EMAIL_HOST
   - EMAIL_PORT
   - EMAIL_USE_TLS
   - EMAIL_HOST_USER
   - EMAIL_HOST_PASSWORD

Example for Gmail:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## Static Files

To collect static files for production:
```bash
python manage.py collectstatic
```

## Database

The application uses SQLite by default. To switch to PostgreSQL or MySQL:

1. Install the database driver:
   ```bash
   pip install psycopg2-binary  # For PostgreSQL
   # or
   pip install mysqlclient      # For MySQL
   ```

2. Update DATABASES in settings.py

3. Run migrations

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Generate a new `SECRET_KEY`
4. Set up a production database
5. Configure email settings
6. Use a WSGI server (Gunicorn, uWSGI)
7. Set up static file serving (Nginx, Apache)
8. Enable HTTPS with SSL certificate

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Optimizations

- Database indexing on frequently queried fields
- Pagination for large property lists
- Image optimization with Pillow
- CSS and JS minification (Bootstrap CDN)
- Lazy loading for property images

## Security Features

- CSRF protection on all forms
- Password hashing with Django's built-in system
- SQL injection prevention through ORM
- XSS protection through template escaping
- User authentication required for sensitive operations
- Permission checks on property editing/deletion

## Troubleshooting

### Images not showing
- Ensure MEDIA_ROOT and MEDIA_URL are correctly configured
- Check that media directory exists and is writable
- Verify image file permissions

### Static files missing
- Run `python manage.py collectstatic`
- Check STATIC_ROOT and STATIC_URL settings

### Email not sending
- Verify email backend configuration
- Check EMAIL_HOST and credentials
- Enable less secure apps (if using Gmail)

### Database errors
- Run `python manage.py migrate`
- Check database file permissions
- Verify database connection string

## Contributing

This is a standalone educational project. For improvements or bug fixes, modify the source code directly.

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, refer to the Django documentation at https://docs.djangoproject.com/

## Future Enhancements

- Map integration (Google Maps)
- Messaging system between users
- Property reviews and ratings
- Video tours
- Virtual tours with 3D
- Payment integration
- Property comparison tool
- Advanced analytics for property owners
- Email notifications
- SMS notifications
- Mobile app

---

**Built with Django 4.2.7 | Bootstrap 5 | PostgreSQL Ready | Fully Responsive**

Last Updated: December 2025
