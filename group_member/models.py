"""Manage group_member's app objects"""

from django.db import models

from django.conf import settings


class GroupMember(models.Model):
    """Association model that associate a
    User and a community (a Group object)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    group = models.ForeignKey('group.Group',
                              on_delete=models.CASCADE)
    points_posseded = models.IntegerField(blank=True, null=True)
    points_penalty = models.IntegerField(default=0)

    def __str__(self):
        """Print attribute as title's object in Django admin"""
        return '%s, %s' % (
            self.user, self.group,
        )
