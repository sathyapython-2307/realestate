from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and listing
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property-list'),
    path('property/<slug:slug>/', views.property_detail, name='property-detail'),
    
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html',
        form_class=views.CustomPasswordResetForm,
        email_template_name='auth/password_reset_email.html',
        subject_template_name='auth/password_reset_subject.txt',
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Property Management
    path('post-property/', views.post_property, name='post-property'),
    path('edit-property/<slug:slug>/', views.edit_property, name='edit-property'),
    path('delete-property/<slug:slug>/', views.delete_property, name='delete-property'),
    path('delete-image/<int:image_id>/', views.delete_property_image, name='delete-image'),
    
    # Inquiries
    path('contact/<slug:slug>/', views.contact_property, name='contact-property'),
    path('my-inquiries/', views.my_inquiries, name='my-inquiries'),
    path('manage-inquiries/', views.manage_inquiries, name='manage-inquiries'),
    path('inquiry/<int:inquiry_id>/', views.inquiry_detail, name='inquiry-detail'),
    
    # Favorites
    path('saved-properties/', views.saved_properties, name='saved-properties'),
    path('toggle-favorite/<slug:slug>/', views.toggle_favorite, name='toggle-favorite'),
    
    # Dashboard and Profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]
