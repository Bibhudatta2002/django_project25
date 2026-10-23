from django import forms
from django.contrib.auth.models import User
from app.models import Profile


class UserMF(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        help_texts = {'username': ''}
        widgets = {'password': forms.PasswordInput()}


class ProfileMF(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['username']

