"""Manage admin views of group_member's app objects"""

from django.contrib import admin

from .models import GroupMember


class GroupMemberAdmin(admin.ModelAdmin):
    """Class that manage GroupMember objects in Django admin """


# Register the admin class with the associated model
admin.site.register(GroupMember, GroupMemberAdmin)
