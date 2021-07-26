"""Manage product's app objects"""

from django.db import models


class Product(models.Model):
    """Class that represent a Product object"""
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    user_provider = models.ForeignKey(
        'group_member.GroupMember',
        on_delete=models.CASCADE,
        related_name='member_in_group_provider_of_product',
        blank=True, null=True
    )
    group_provider = models.ForeignKey(
        'group.Group',
        on_delete=models.CASCADE,
        related_name='group_provider_of_product',
        blank=True, null=True
    )
    tenant = models.ForeignKey(
        'group_member.GroupMember',
        on_delete=models.PROTECT,
        related_name='member_in_group_tenant_of_product',
        blank=True, null=True
    )
    group = models.ForeignKey('group.Group',
                              on_delete=models.CASCADE,
                              related_name='group_owns_product')
    image = models.ImageField(null=True, blank=True)
    estimator = models.ManyToManyField(
        'group_member.GroupMember',
        through="collective_decision.Estimation",
        related_name='product_cost_estimation_of_members_in_group'
    )

    points = models.IntegerField(null=True, blank=True)

    delivered = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=models.Q(user_provider=True) & models.Q(group_provider=False),
    #             name='if_user_provider_is_true_group_provider_is_false'),
    #         models.CheckConstraint(
    #             check=models.Q(user_provider=False) & models.Q(group_provider=True),
    #             name='if_group_provider_is_true_user_provider_is_false'),
    #     ]

    def __str__(self):
        """Print attribute as title's object in Django admin"""
        return '%s, %s, %s' % (
            self.name, self.group,
            self.user_provider or self.group_provider
        )
