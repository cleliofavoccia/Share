from django.db import models
from django.conf import settings


class Group(models.Model):
    """Class that represent a Community in which we can share
    products"""
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through='group_member.GroupMember'
                                     , related_name='members_in_group')
    points = models.IntegerField(null=True, blank=True)
    members_points = models.IntegerField(null=True, blank=True)
    address = models.ForeignKey('geolocalisation.Address',
                                on_delete=models.CASCADE,
                                related_name='address_of_group',
                                null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    decision_makers = models.ManyToManyField('group_member.GroupMember',
                                             through="collective_decision.Decision",
                                             related_name='vote_of_members_in_group')
    url = models.URLField(null=True, blank=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        """Print attribute as title's object in Django admin"""
        return '%s' % self.name
