from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# automatycznie obsługuje hashowanie hasła i walidacje
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

# formularz logowania, PasswordInput ukrywa hasło w przeglądarce
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)