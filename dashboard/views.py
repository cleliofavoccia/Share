"""Manage dashboard app views"""
import json

from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.core import serializers

from group.models import Group
from product.models import Product
from group_member.models import GroupMember
from collective_decision.models import Estimation

from .forms import CommunityResearchForm


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
                group_member.points_posseded -= group_member.points_penalty
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

        # Calculate communities's products cost, total products cost,
        # points per community member
        for community in my_communities:
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
            community_members = GroupMember.objects.filter(
                group=community
            )
            for group_member in community_members:
                group_member.points_posseded = community.members_points
                group_member.points_posseded -= group_member.points_penalty
                group_member.save()

            community.save()

        return context


class CommunityResearchView(ListView):
    """Generic class-based GroupMember list view to print all communities
    where user has suscribed"""
    model = Group
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        """Method that return an enriched context"""
        context = super().get_context_data(**kwargs)
        research = self.request.GET.get('research')
        communities = Group.objects.filter(name__icontains=research)
        context['communities'] = communities

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
            community_members = GroupMember.objects.filter(
                group=community
            )
            for group_member in community_members:
                group_member.points_posseded = community.members_points
                group_member.points_posseded -= group_member.points_penalty
                group_member.save()

            community.save()

        return context
