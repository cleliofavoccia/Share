"""Manage geolocalisation's app objects"""

from django.db import models


class Address(models.Model):
    """Class that represent a postal address"""
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=6)
    country = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        """Print attribute as title's object in Django admin"""
        return '%s, %s' % (self.street, self.city)
