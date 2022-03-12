from django import forms
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm

# attrs={"class":"form-control","type":"email","id":"exampleInputEmail1","placeholder":"Email"}


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = "account.CustomUserModel"
        fields = ["email","password1","password2"]


class LoginForm(forms.Form):
    email = forms.CharField(required=True,widget=forms.EmailInput())
    password = forms.CharField(required=True,widget=forms.PasswordInput())
