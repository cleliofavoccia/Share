from django.contrib import admin

from .models import Group


class GroupAdmin(admin.ModelAdmin):
    """Class that manage Group objects in Django admin """


admin.site.register(Group, GroupAdmin)
