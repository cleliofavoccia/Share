from django.contrib import admin

from .models import GroupMember


class GroupMemberAdmin(admin.ModelAdmin):
    """Class that manage Estimation objects in Django admin """


admin.site.register(GroupMember, GroupMemberAdmin)
