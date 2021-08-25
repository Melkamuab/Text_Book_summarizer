from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User_profile

class SignupForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class UpdateUserForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model=User_profile
        fields=['user']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=User_profile
        fields=['profile']
