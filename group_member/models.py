from django.db import models
from django.conf import settings


class GroupMember(models.Model):
    """Association class that associate a
    User and a community (a Group object)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    group = models.ForeignKey('group.Group',
                              on_delete=models.CASCADE)
    points_posseded = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """Print attribute as title's object in Django admin"""
        return '%s, %s, %s' % (
            self.user, self.group,
            self.points_posseded
        )

