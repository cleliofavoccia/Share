"""Manage admin views of group's app objects"""

from django.contrib import admin

from .models import Group


class GroupAdmin(admin.ModelAdmin):
    """Class that manage Group objects in Django admin """


# Register the admin class with the associated model
admin.site.register(Group, GroupAdmin)
