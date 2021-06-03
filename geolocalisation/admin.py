from django.contrib import admin

from .models import Address


class AddressAdmin(admin.ModelAdmin):
    """Class that manage Address objects in Django admin """


admin.site.register(Address, AddressAdmin)
