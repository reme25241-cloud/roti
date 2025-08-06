from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class BootstrapFormMixin:
    """Mixin to add Bootstrap classes automatically."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = existing_class + ' form-control'

# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
class ProfileForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'contact', 'age', 'gender', 'address', 'profile_picture', 'qr_code_image']
        widgets = {
            'email': forms.EmailInput(),
            'contact': forms.TextInput(),
            'age': forms.NumberInput(),
            'gender': forms.Select(),
            'name': forms.TextInput(),
            'address': forms.Textarea(attrs={'rows': 3}),
            'profile_picture': forms.FileInput(),'qr_code_image': forms.FileInput(),
            
        }

# feedback

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your feedback here...'}),
        }
# myapp/forms.py
from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'image', 'description', 'cost', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the product'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your review here...'
            }),
        }

from django import forms
from .models import ReturnProduct

class ReturnForm(forms.ModelForm):
    class Meta:
        model = ReturnProduct
        fields = ['reason', 'image']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class CartQuantityUpdateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'style': 'width:100px'
            }),
        }
        
from django import forms
from .models import PendingPurchaseRequest

class PendingPurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PendingPurchaseRequest
        fields = ['user', 'cart', 'payment_proceeded', 'seller_confirmed', 'buyer_received']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'cart': forms.Select(attrs={'class': 'form-select'}),
            'payment_proceeded': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'seller_confirmed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'buyer_received': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Optional: Wishlist toggle form (if needed)
class WishlistToggleForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
