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
            # Recover product estimations
            cost_estimations = Estimation.objects.filter(product=product)
            # Count there
            estimation_numbers = cost_estimations.count()
            # Add product estimations to product points (cost)
            sum_product_cost = 0
            for estimation in cost_estimations:
                sum_product_cost += estimation.cost
            try:
                # Save product cost
                product.points = sum_product_cost // estimation_numbers
            except ZeroDivisionError:
                product.points = 0
            product.save()

            # Increment total products cost to community
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
        community_members = GroupMember.objects.filter(
            group=community
        )
        for group_member in community_members:
            group_member.points_posseded = community.members_points
            # Substract points_penalty due to location from points_posseded
            group_member.points_posseded -= group_member.points_penalty
            group_member.save()

        community.save()
    return 'Update !'
