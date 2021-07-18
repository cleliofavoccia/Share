"""Forms of users app"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from geolocalisation.models import Address

from .models import User


class UserMyCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'address',)


class UserMyChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'address',)


class CreateUserForm(UserCreationForm):
    """ Sign in forms to permit the users to register him"""
    class Meta:
        model = get_user_model()
        fields = ['email']


class ChangeUserForm(UserChangeForm):
    """ Sign in forms to permit the users to modify him"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'address', 'username', 'first_name', 'last_name']


class AddressUserForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code', 'country']
