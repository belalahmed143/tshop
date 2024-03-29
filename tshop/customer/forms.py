from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()


    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'username', 'email', 'password1', 'password2']
