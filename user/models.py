"""Manage user's app objects"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Class that represent custom Django User object """
    username = models.CharField(max_length=150, blank=True, unique=False)
    email = models.EmailField(unique=True)
    address = models.ForeignKey(
        'geolocalisation.Address',
        on_delete=models.CASCADE,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """Print attribute as title's object in Django admin"""
        return '%s' % self.email
