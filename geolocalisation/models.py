from django.db import models


class Address(models.Model):
    """Class that represent a postal address"""
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=6)
    country = models.CharField(max_length=30)
