from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Property, PropertyImage, PropertyInquiry


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
    }))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name',
    }))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username or Email',
        'autofocus': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
        'autofocus': True,
    }))


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'listing_type', 'description',
            'location', 'city', 'state', 'postal_code',
            'bedrooms', 'bathrooms', 'area', 'price',
            'is_furnished', 'has_parking', 'has_balcony', 'has_garden',
            'has_pool', 'has_gym', 'condition',
            'contact_name', 'contact_phone', 'contact_email',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Property Title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detailed description of the property',
                'rows': 5,
            }),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal Code',
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area in sq. ft.',
                'min': 0,
                'step': 0.01,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price',
                'min': 0,
                'step': 0.01,
            }),
            'is_furnished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_garden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_gym': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Name (optional)',
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Phone (optional)',
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Email (optional)',
            }),
        }

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area and area <= 0:
            raise forms.ValidationError('Area must be greater than 0.')
        return area

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price


class PropertyInquiryForm(forms.ModelForm):
    class Meta:
        model = PropertyInquiry
        fields = ['name', 'email', 'phone', 'message', 'inquiry_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message / Inquiry',
                'rows': 5,
            }),
            'inquiry_type': forms.Select(attrs={'class': 'form-control'}),
        }


class PropertySearchForm(forms.Form):
    LISTING_TYPE_CHOICES = [('', 'All Types')] + list(Property.LISTING_TYPE_CHOICES)
    PROPERTY_TYPE_CHOICES = [('', 'All Property Types')] + list(Property.PROPERTY_TYPE_CHOICES)

    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search by location, title, or city',
    }))
    listing_type = forms.ChoiceField(choices=LISTING_TYPE_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    property_type = forms.ChoiceField(choices=PROPERTY_TYPE_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City',
    }))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Min Price',
        'step': 0.01,
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Max Price',
        'step': 0.01,
    }))
    bedrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Bedrooms',
        'min': 0,
    }))
    bathrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Bathrooms',
        'min': 0,
    }))
    is_furnished = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))
    has_parking = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
    }))


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
