from django.contrib import admin
from .models import Property, PropertyImage, PropertyInquiry, FavoriteProperty


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'listing_type', 'city', 'price', 'is_active', 'is_featured', 'created_at']
    list_filter = ['listing_type', 'property_type', 'is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'location', 'city', 'owner__username']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'title', 'slug', 'description', 'property_type', 'listing_type')
        }),
        ('Location', {
            'fields': ('location', 'city', 'state', 'postal_code', 'latitude', 'longitude')
        }),
        ('Details', {
            'fields': ('bedrooms', 'bathrooms', 'area', 'price', 'condition')
        }),
        ('Features', {
            'fields': ('is_furnished', 'has_parking', 'has_balcony', 'has_garden', 'has_pool', 'has_gym')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'contact_phone', 'contact_email'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['property__title']
    readonly_fields = ['uploaded_at']


@admin.register(PropertyInquiry)
class PropertyInquiryAdmin(admin.ModelAdmin):
    list_display = ['property', 'sender', 'inquiry_type', 'status', 'created_at']
    list_filter = ['status', 'inquiry_type', 'created_at']
    search_fields = ['property__title', 'sender__username', 'name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Inquiry Details', {
            'fields': ('property', 'sender', 'inquiry_type', 'status')
        }),
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FavoriteProperty)
class FavoritePropertyAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'property__title']
    readonly_fields = ['added_at']
