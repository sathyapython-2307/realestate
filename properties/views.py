from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Property, PropertyImage, PropertyInquiry, FavoriteProperty
from .forms import (
    SignUpForm, LoginForm, PropertyForm, PropertyInquiryForm,
    PropertySearchForm, PropertyImageForm, CustomPasswordResetForm
)


# ============ Authentication Views ============

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    
    return render(request, 'auth/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with username first, then email
            user = authenticate(request, username=username_or_email, password=password)
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user:
                login(request, user)
                if form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(1209600)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ============ Home & Listing Views ============

def home(request):
    featured_properties = Property.objects.filter(is_active=True, is_featured=True)[:6]
    latest_properties = Property.objects.filter(is_active=True)[:12]
    
    context = {
        'featured_properties': featured_properties,
        'latest_properties': latest_properties,
        'listing_types': Property.LISTING_TYPE_CHOICES,
    }
    return render(request, 'properties/home.html', context)


def property_list(request):
    properties = Property.objects.filter(is_active=True)
    form = PropertySearchForm(request.GET)
    
    # Apply filters
    search_query = request.GET.get('search', '')
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    listing_type = request.GET.get('listing_type', '')
    if listing_type:
        properties = properties.filter(listing_type=listing_type)
    
    property_type = request.GET.get('property_type', '')
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    city = request.GET.get('city', '')
    if city:
        properties = properties.filter(city__icontains=city)
    
    min_price = request.GET.get('min_price')
    if min_price:
        try:
            min_price = float(min_price)
            properties = properties.filter(price__gte=min_price)
        except (ValueError, TypeError):
            pass
    
    max_price = request.GET.get('max_price')
    if max_price:
        try:
            max_price = float(max_price)
            properties = properties.filter(price__lte=max_price)
        except (ValueError, TypeError):
            pass
    
    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        try:
            bedrooms = int(bedrooms)
            properties = properties.filter(bedrooms__gte=bedrooms)
        except (ValueError, TypeError):
            pass
    
    bathrooms = request.GET.get('bathrooms')
    if bathrooms:
        try:
            bathrooms = int(bathrooms)
            properties = properties.filter(bathrooms__gte=bathrooms)
        except (ValueError, TypeError):
            pass
    
    is_furnished = request.GET.get('is_furnished')
    if is_furnished:
        properties = properties.filter(is_furnished=True)
    
    has_parking = request.GET.get('has_parking')
    if has_parking:
        properties = properties.filter(has_parking=True)
    
    # Pagination
    paginator = Paginator(properties.order_by('-created_at'), 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user favorites if logged in
    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(
            request.user.favorite_properties.values_list('property_id', flat=True)
        )
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'user_favorites': user_favorites,
        'total_count': properties.count(),
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    images = property_obj.images.all()
    inquiries_count = property_obj.inquiries.filter(status='pending').count()
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteProperty.objects.filter(
            user=request.user, property=property_obj
        ).exists()
    
    similar_properties = Property.objects.filter(
        is_active=True,
        city=property_obj.city,
        property_type=property_obj.property_type,
    ).exclude(id=property_obj.id)[:4]
    
    context = {
        'property': property_obj,
        'images': images,
        'is_favorite': is_favorite,
        'similar_properties': similar_properties,
        'inquiries_count': inquiries_count,
    }
    return render(request, 'properties/property_detail.html', context)


# ============ Property Management Views ============

@login_required(login_url='login')
def post_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for index, image in enumerate(images):
                is_primary = index == 0  # First image is primary
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                    is_primary=is_primary
                )
            
            messages.success(request, 'Property posted successfully!')
            return redirect('property-detail', slug=property_obj.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PropertyForm()
    
    context = {'form': form, 'action': 'Post'}
    return render(request, 'properties/post_property.html', context)


@login_required(login_url='login')
def edit_property(request, slug):
    property_obj = get_object_or_404(Property, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            property_obj = form.save()
            
            # Handle new image uploads
            images = request.FILES.getlist('images')
            for index, image in enumerate(images):
                PropertyImage.objects.create(
                    property=property_obj,
                    image=image,
                    is_primary=False
                )
            
            messages.success(request, 'Property updated successfully!')
            return redirect('property-detail', slug=property_obj.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PropertyForm(instance=property_obj)
    
    context = {
        'form': form,
        'property': property_obj,
        'action': 'Edit',
        'images': property_obj.images.all(),
    }
    return render(request, 'properties/edit_property.html', context)


@login_required(login_url='login')
def delete_property(request, slug):
    property_obj = get_object_or_404(Property, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('dashboard')
    
    context = {'property': property_obj}
    return render(request, 'properties/delete_property.html', context)


@login_required(login_url='login')
def delete_property_image(request, image_id):
    image = get_object_or_404(PropertyImage, id=image_id, property__owner=request.user)
    property_obj = image.property
    image.delete()
    messages.success(request, 'Image deleted successfully!')
    return redirect('edit-property', slug=property_obj.slug)


# ============ Inquiry Views ============

@login_required(login_url='login')
def contact_property(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    
    # Check if inquiry already exists
    existing_inquiry = PropertyInquiry.objects.filter(
        property=property_obj,
        sender=request.user
    ).first()
    
    if request.method == 'POST':
        form = PropertyInquiryForm(request.POST, instance=existing_inquiry)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property_obj
            inquiry.sender = request.user
            inquiry.save()
            messages.success(request, 'Your inquiry has been sent to the property owner!')
            return redirect('property-detail', slug=property_obj.slug)
    else:
        initial_data = {}
        if existing_inquiry:
            form = PropertyInquiryForm(instance=existing_inquiry)
        else:
            if request.user.first_name and request.user.last_name:
                initial_data['name'] = f"{request.user.first_name} {request.user.last_name}"
            initial_data['email'] = request.user.email
            form = PropertyInquiryForm(initial=initial_data)
    
    context = {
        'form': form,
        'property': property_obj,
        'existing_inquiry': existing_inquiry,
    }
    return render(request, 'properties/contact_property.html', context)


# ============ Dashboard Views ============

@login_required(login_url='login')
def dashboard(request):
    user_properties = request.user.properties.all()
    all_inquiries = PropertyInquiry.objects.filter(
        property__owner=request.user
    ).select_related('sender', 'property').order_by('-created_at')
    recent_inquiries = all_inquiries[:10]
    
    stats = {
        'total_properties': user_properties.count(),
        'active_properties': user_properties.filter(is_active=True).count(),
        'total_inquiries': all_inquiries.count(),
        'pending_inquiries': all_inquiries.filter(status='pending').count(),
    }
    
    context = {
        'user_properties': user_properties,
        'recent_inquiries': recent_inquiries,
        'stats': stats,
    }
    return render(request, 'properties/dashboard.html', context)


@login_required(login_url='login')
def manage_inquiries(request):
    inquiries = PropertyInquiry.objects.filter(
        property__owner=request.user
    ).select_related('sender', 'property').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(inquiries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'properties/manage_inquiries.html', context)


@login_required(login_url='login')
def inquiry_detail(request, inquiry_id):
    inquiry = get_object_or_404(PropertyInquiry, id=inquiry_id, property__owner=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(PropertyInquiry.STATUS_CHOICES):
            inquiry.status = status
            inquiry.save()
            messages.success(request, 'Inquiry status updated!')
            return redirect('manage-inquiries')
    
    context = {'inquiry': inquiry}
    return render(request, 'properties/inquiry_detail.html', context)


@login_required(login_url='login')
def my_inquiries(request):
    inquiries = PropertyInquiry.objects.filter(sender=request.user).select_related(
        'property', 'property__owner'
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(inquiries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'properties/my_inquiries.html', context)


# ============ Favorites Views ============

@login_required(login_url='login')
def saved_properties(request):
    favorites = FavoriteProperty.objects.filter(user=request.user).select_related(
        'property'
    ).order_by('-added_at')
    
    # Pagination
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'properties/saved_properties.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def toggle_favorite(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    favorite, created = FavoriteProperty.objects.get_or_create(
        user=request.user,
        property=property_obj
    )
    
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed', 'is_favorite': False})
    
    return JsonResponse({'status': 'added', 'is_favorite': True})


# ============ Profile Views ============

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {'user': request.user}
    return render(request, 'properties/profile.html', context)


# ============ Error Views ============

def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)
