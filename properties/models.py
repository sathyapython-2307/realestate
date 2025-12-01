
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, URLValidator
from django.urls import reverse
import uuid


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('penthouse', 'Penthouse'),
        ('townhouse', 'Townhouse'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
        ('other', 'Other'),
    ]
    
    LISTING_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('old', 'Old'),
        ('renovated', 'Renovated'),
    ]

    # Basic Info
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    
    # Location
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Details
    bedrooms = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    bathrooms = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    area = models.FloatField(validators=[MinValueValidator(0)], help_text='Area in sq. ft.')
    
    # Pricing
    price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Features
    is_furnished = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_garden = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='old')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Contact Info (optional, can override owner contact)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['city', 'listing_type']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('property-detail', kwargs={'slug': self.slug})

    @property
    def image_count(self):
        return self.images.count()

    @property
    def primary_image(self):
        return self.images.first()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/%Y/%m/%d/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']

    def __str__(self):
        return f"Image for {self.property.title}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            PropertyImage.objects.filter(property=self.property, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class PropertyInquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('responded', 'Responded'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    inquiry_type = models.CharField(max_length=20, choices=[
        ('inquiry', 'General Inquiry'),
        ('booking', 'Booking Request'),
        ('visit', 'Schedule Visit'),
    ], default='inquiry')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('property', 'sender')

    def __str__(self):
        return f"Inquiry for {self.property.title} by {self.sender.get_full_name() or self.sender.username}"


class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} favorited {self.property.title}"
