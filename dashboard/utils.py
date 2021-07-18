"""Function usefull for updated communities informations"""

from group.models import Group
from collective_decision.models import Estimation
from product.models import Product
from group_member.models import GroupMember


def update_communities_informations():
    """Calculate communities's products cost, total products cost, points per community member"""

    communities = Group.objects.all()

    for community in communities:
        # Total products cost
        community.points = 0
        # Communities's products cost
        for product in community.group_owns_product.all():
            cost_estimations = Estimation.objects.filter(product=product)
            estimation_numbers = cost_estimations.count()
            sum_product_cost = 0
            for estimation in cost_estimations:
                sum_product_cost += estimation.cost
            product.points = sum_product_cost // estimation_numbers
            product.save()
            # Increment total products cost
            community.points += sum_product_cost // estimation_numbers
        # Points per community member
        community.members_points = community.points // community.members.count()
        # Save points per community member for each user
        community_members = GroupMember.objects.filter(group=community)
        for group_member in community_members:
            group_member.points_posseded = community.members_points
            group_member.save()

        community.save()