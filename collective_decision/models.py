"""Manage collective_decision app objects"""

from django.db import models


class Estimation(models.Model):
    """Class that represent an estimation
    concerning a cost of a Product object"""
    cost = models.IntegerField()
    group_member = models.ForeignKey(
        'group_member.GroupMember',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group_member', 'product'], name='user_product_uniq'
            )
        ]

    def __str__(self):
        """Print attribute as title's object in Django admin"""
        return f'{self.group_member} a estimé {self.product} ' \
               f'à {self.cost} points'


class Decision(models.Model):
    """Class that represent a decision
    concerning a group modification"""
    delete_group_vote = models.BooleanField(default=False)
    modify_group_vote = models.BooleanField(default=False)
    delete_member_vote = models.BooleanField(default=False)
    group_member = models.ForeignKey(
        'group_member.GroupMember',
        on_delete=models.CASCADE
    )
    group = models.ForeignKey("group.Group", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group_member', 'group'], name='user_group_uniq'
            )
        ]

    def __str__(self):
        """Print attribute as title's object in Django admin"""
        return f'{self.group_member} a voté ' \
               f'{self.delete_group_vote} pour supprimer {self.group},' \
               f'{self.modify_group_vote} pour modifier {self.group}'
