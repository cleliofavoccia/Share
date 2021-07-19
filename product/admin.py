"""Manage admin views of product's app objects"""

from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    """Class that manage Product objects in Django admin """


# Register the admin class with the associated model
admin.site.register(Product, ProductAdmin)
