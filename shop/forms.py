from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from shop.models import Customer, ShippingAddress

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"Your password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Repeat the password"
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username":forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Username"
            }),
            "email": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "E-Mail"
            })
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "palceholder":"Your username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "palceholder": "Your password"
    }))

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']
        widgets = {
            "name":forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':"Your name"
            }),
            "email": forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': "Your email"
            })
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['city', 'street', 'address']
        widgets = {
            "city":forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':"Your city"
            }),
            "street": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Your street"
            }),
            "address": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Your address"
            })
        }