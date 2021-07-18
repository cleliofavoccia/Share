
from django.views.generic import ListView, TemplateView
from group.models import Group
from product.models import Product
from group_member.models import GroupMember
from collective_decision.models import Estimation
from django.db.models import Count


class Explorer(ListView):

    model = Group
    context_object_name = 'communities'
    template_name = 'dashboard/explorer.html'

    def get_queryset(self):
        return super().get_queryset().annotate(products_number=Count('group_owns_product', distinct=True),)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        communities = self.get_queryset()

        # Calculate communities's products cost, total products cost,
        # points per community member
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

        # Add communities in which user has suscribed in a list
        # that added to context to verify if user is in a displayed
        # community
        if user.is_authenticated:
            group_member_list = list()
            group_member = GroupMember.objects.filter(user=user)
            for community in group_member:
                group_member_list.append(community.group.name)
            context['group_member_list'] = group_member_list
        else:
            pass

        return context


class MyCommunities(TemplateView):

    template_name = 'dashboard/my_communities.html'

    def get_context_data(self, **kwargs):
        # user = self.request.user
        # active_community = self.request.current_community
        context = super().get_context_data(**kwargs)
        # my_communities = GroupMember.objects.filter(user=user)
        communities = Group.objects.all()
        # communities_products = Product.objects.filter(group=active_community)

        context['communities'] = communities
        # context['communities_products'] = communities_products
        return context


