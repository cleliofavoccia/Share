from django.db import models
from django.conf import settings


class Group(models.Model):
    """Class that represent a Community in which we can share
    products"""
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through='group_member.GroupMember'
                                     , related_name='members_in_group')
    points = models.IntegerField()
    address = models.ForeignKey('geolocalisation.Address',
                                on_delete=models.CASCADE,
                                related_name='address_of_group')
    image = models.ImageField()
    decision_makers = models.ManyToManyField('group_member.GroupMember',
                                             through="collective_decision.Decision",
                                             related_name='vote_of_members_in_group')
