"""Function usefull for updated communities informations"""

from group.models import Group
from collective_decision.models import Estimation
from product.models import Product
from group_member.models import GroupMember


def update_communities_informations():
    """Calculate communities's products cost,
    total products cost, points per community member"""

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
            try:
                product.points = sum_product_cost // estimation_numbers
            except ZeroDivisionError:
                product.points = 0
            product.save()

            # Increment total products cost
            try:
                community.points += (
                        sum_product_cost // estimation_numbers
                )
            except ZeroDivisionError:
                community.points = 0
        # Points per community member
        try:
            community.members_points = (
                    community.points // community.members.count()
            )
        except ZeroDivisionError:
            community.members_points = 0

        # Save points per community member for each user
        community_members = GroupMember.objects.filter(group=community)
        for group_member in community_members:
            group_member.points_posseded = community.members_points
            group_member.save()

        community.save()
