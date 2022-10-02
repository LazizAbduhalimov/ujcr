from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
forms.fields.Field.default_error_messages = {'required': _('No dots here'),}

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={
        "class": "form-input",
        "type": "text",
        "name": "givenName",
        "id": "givenName",
        "maxlength": "255",
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "type": "password",
        "name": "password",
        "id": "password",
        "password": "true",
        "maxlength": "32",
    }))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "type": "password",
        "name": "password2",
        "id": "password2",
        "password": "true",
        "maxlength": "32",
    }))
    email = forms.CharField(label="E-mail", widget=forms.EmailInput(attrs={
        "class": "form-input",
        "type": "email",
        "name": "email",
        "id": "email",
        "maxlength": "90",
    }))
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

