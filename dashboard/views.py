"""Manage dashboard app views"""

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from group.utils import update_communities_informations
from group.models import Group
from group_member.models import GroupMember


class Explorer(ListView):
    """Generic class-based Group list view to print all public communities"""
    model = Group
    template_name = 'dashboard/dashboard.html'

    def get_queryset(self):
        """Method that return supplementary attributes for Group objects"""
        return super().get_queryset().annotate(
            products_number=Count('group_owns_product', distinct=True),
        )

    def get_context_data(self, **kwargs):
        """Method that return an enriched context"""
        user = self.request.user
        context = super().get_context_data(**kwargs)
        communities = self.get_queryset().filter(private=False)
        context['communities'] = communities

        # Calculate communities's products cost, total products cost,
        # points per community member
        update_communities_informations()

        # Add communities in which user has suscribed in a list
        # that added to context to verify if user is in a displayed
        # community
        if user.is_authenticated:
            group_member_list = list()
            group_member = GroupMember.objects.filter(user=user)
            for community in group_member:
                group_member_list.append(community.group.name)
            context['group_member_list'] = group_member_list

        return context


class MyCommunities(LoginRequiredMixin, ListView):
    """Generic class-based GroupMember list view to print all communities
    where user has suscribed"""
    model = GroupMember
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        """Method that return an enriched context"""
        user = self.request.user
        context = super().get_context_data(**kwargs)
        my_communities = Group.objects.filter(members=user)
        context['communities'] = my_communities

        # To not permit user to join many times
        group_member_list = list()
        group_member = GroupMember.objects.filter(user=user)
        for community in group_member:
            group_member_list.append(community.group.name)
        context['group_member_list'] = group_member_list

        # Calculate communities's products cost, total products cost,
        # points per community member
        update_communities_informations()

        return context


class CommunityResearchView(ListView):
    """Generic class-based GroupMember list view to print all communities
    where user has suscribed"""
    model = Group
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        """Method that return an enriched context"""
        user = self.request.user
        context = super().get_context_data(**kwargs)
        research = self.request.GET.get('research')
        communities = Group.objects.filter(name__icontains=research)
        context['communities'] = communities

        # Calculate communities's products cost, total products cost,
        # points per community member
        update_communities_informations()

        if user.is_authenticated:
            # To not permit user to join many times
            group_member_list = list()
            group_member = GroupMember.objects.filter(user=user)
            for community in group_member:
                group_member_list.append(community.group.name)
            context['group_member_list'] = group_member_list

        return context
