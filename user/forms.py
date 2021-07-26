"""Manage user app forms"""

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

from geolocalisation.models import Address

from .models import User


class UserMyCreationForm(UserCreationForm):
    """Form to create User object in django admin"""
    class Meta:
        model = User
        fields = ('email', 'address',)


class UserMyChangeForm(UserChangeForm):
    """Form to modify User object in django admin"""
    class Meta:
        model = User
        fields = ('email', 'address',)


class CreateUserForm(UserCreationForm):
    """Form to permit user to register him"""
    class Meta:
        model = get_user_model()
        fields = ['email']


class ChangeUserForm(UserChangeForm):
    """Form to permit user to modify him"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'first_name', 'last_name']


class AddressUserForm(forms.ModelForm):
    """Form to register a postal address"""
    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code', 'country']
