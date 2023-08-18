from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class SignUpForm(UserCreationForm):
    """Registration form"""
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='eg.yourmail@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2', 'email')


class EditUserForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-2"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-2"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        "class": "custom-file-label", 'required': False}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", 'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4", 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')


