from django.db import models


class Product(models.Model):
    """Class that represent a Product object"""
    name = models.CharField(max_length=30)
    description = models.TextField()
    user_provider = models.ForeignKey('group_member.GroupMember',
                                      on_delete=models.CASCADE,
                                      related_name='member_in_group_provider_of_product')
    group_provider = models.ForeignKey('group.Group',
                                       on_delete=models.CASCADE,
                                       related_name='group_provider_of_product')
    tenant = models.ForeignKey('group_member.GroupMember',
                               on_delete=models.PROTECT,
                               related_name='member_in_group_tenant_of_product')
    group = models.ForeignKey('group.Group',
                              on_delete=models.CASCADE,
                              related_name='group_owns_product')
    image = models.ImageField()
    estimator = models.ManyToManyField('group_member.GroupMember',
                                       through="collective_decision.Estimation",
                                       related_name=
                                       'product_cost_estimation_of_members_in_group')
