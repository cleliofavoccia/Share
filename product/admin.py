from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    """Class that manage Estimation objects in Django admin """


admin.site.register(Product, ProductAdmin)
