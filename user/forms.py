from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from .models import User


class UserMyCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'address',)


class UserMyChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'address',)
