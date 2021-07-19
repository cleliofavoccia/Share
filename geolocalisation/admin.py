"""Manage admin views of geolocalisation's app objects"""

from django.contrib import admin

from .models import Address


class AddressAdmin(admin.ModelAdmin):
    """Class that manage Address objects in Django admin """


# Register the admin class with the associated model
admin.site.register(Address, AddressAdmin)
