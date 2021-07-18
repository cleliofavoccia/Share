"""Views of favorites app"""
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from .forms import GroupMemberVoteForm
from .models import Decision, Estimation
from group_member.models import GroupMember
from product.models import Product
from group.models import Group


class GroupMemberDeleteVoteGroup(LoginRequiredMixin, View):
    """Generic class-based view to change delete_vote_group
    attribute to True of Decision object per GroupMember"""

    def post(self, request):
        """Method POST Group and GroupMember instance
        to GroupeMemberVoteForm"""
        form = GroupMemberVoteForm(request.POST)
        if form.is_valid():
            form.save_delete_group_vote(request.user)
            # return redirect(f"/collective_decision/vote/{request.POST['group']}")
            return redirect("collective_decision:vote", pk=request.POST['group'])
        return redirect('collective_decision:fail')


class GroupMemberAgainstDeleteVoteGroup(LoginRequiredMixin, View):
    """Generic class-based view to change delete_vote_group
    attribute to False of Decision object per GroupMember"""

    def post(self, request):
        """Method POST Group and GroupMember instance
        to GroupeMemberVoteForm"""
        form = GroupMemberVoteForm(request.POST)
        if form.is_valid():
            form.save_against_delete_group_vote(request.user)
            # return redirect(f"/collective_decision/vote/{request.POST['group']}")
            return redirect("collective_decision:vote", pk=request.POST['group'])
        return redirect('collective_decision:fail')


class GroupMemberModifyVoteGroup(LoginRequiredMixin, View):
    """Generic class-based view to change modify_vote_group
    attribute to True of Decision object per GroupMember"""

    def post(self, request):
        """Method POST Group and GroupMember instance
        to GroupeMemberVoteForm"""
        form = GroupMemberVoteForm(request.POST)
        if form.is_valid():
            form.save_modify_group_vote(request.user)
            # return redirect(f"/collective_decision/vote/{request.POST['group']}")
            return redirect("collective_decision:vote", pk=request.POST['group'])
        return redirect('collective_decision:fail')


class GroupMemberAgainstModifyVoteGroup(LoginRequiredMixin, View):
    """Generic class-based view to change modify_vote_group
    attribute to False of Decision object per GroupMember"""

    def post(self, request):
        """Method POST Group and GroupMember instance
        to GroupeMemberVoteForm"""
        form = GroupMemberVoteForm(request.POST)
        if form.is_valid():
            form.save_against_modify_group_vote(request.user)
            # return redirect(f"/collective_decision/vote/{request.POST['group']}")
            return redirect("collective_decision:vote", pk=request.POST['group'])
        return redirect('collective_decision:fail')


class FailView(LoginRequiredMixin, View):
    """View to print vote not changed"""

    def get(self, request):
        """Method GET to print fail message"""
        context = {'msg_fail': "Oups ! Il a dû se produire une erreur. Réessayer ou bien,"
                               "en cas de persistence du problème, contactez l'administration"
                               "du site"}

        return render(request, 'collective_decision/fail.html', context)


class GroupVoteView(LoginRequiredMixin, DetailView):
    """Generic class-based Group detail view to print all votes
    about a community and to print modification community page or
    to execute community suppression"""
    model = Group
    template_name = 'collective_decision/vote.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        community = super().get_object()
        communities = Group.objects.all()

        group_products_list = Product.objects.filter(group=community)
        members_number = GroupMember.objects.filter(group=community).count()
        products_number = Product.objects.filter(group=community).count()

        context['group_products_list'] = group_products_list
        context['members_number'] = members_number
        context['products_number'] = products_number

        # Calculate communities's products cost, total products cost,
        # points per user, and group_members points posseded

        # Total products cost
        community.points = 0
        # Community's products cost
        for product in group_products_list:
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

        community_members = GroupMember.objects.filter(group=community)
        context['community_members'] = community_members

        for group_member in community_members:
            # Save points per community member for each user
            group_member.points_posseded = community.members_points
            group_member.save()

            # Create Decisions objects for group members who have made no decision
            try:
                Decision.objects.get(group=community, group_member=group_member)
            except Decision.DoesNotExist:
                Decision.objects.create(group=community, group_member=group_member)

        community.save()

        if user.is_authenticated:
            group_member_list = list()
            group_member = GroupMember.objects.filter(user=user)

            # Add communities in which user has suscribed in a list
            # that added to context to verify if user is in a displayed
            # community
            for community_inscription in group_member:
                group_member_list.append(community_inscription.group.name)
            context['group_member_list'] = group_member_list

        # Verify modification group decisions of community members
        verify_modify_votes = list()

        for member in community_members:
            decision = Decision.objects.get(group=community, group_member=member)
            verify_modify_votes.append(decision.modify_group_vote)

        if all(verify_modify_votes):
            context['modification_group_activate'] = True

        # Print votes
        modify_votes = list()
        for member in community_members:
            decision = Decision.objects.get(group=community, group_member=member)
            modify_votes.append(decision)

        context['modify_votes'] = modify_votes

        # Verify delete group decisions of community members
        verify_delete_votes = list()

        for member in community_members:
            decision = Decision.objects.get(group=community, group_member=member)
            verify_delete_votes.append(decision.delete_group_vote)

        if all(verify_delete_votes):
            community.delete()
            context['delete'] = 'La communauté a bien été supprimé'
            return context

        # Print votes
        delete_votes = list()
        for member in community_members:
            decision = Decision.objects.get(group=community, group_member=member)
            delete_votes.append(decision)

        context['delete_votes'] = delete_votes

        # Fetch the User votes
        group_member = GroupMember.objects.filter(user=user, group=community)[0]
        context['group_member'] = group_member
        delete_group_vote = Decision.objects.filter(group_member=group_member, group=community)
        delete_group_vote = delete_group_vote[0].delete_group_vote
        context['delete_group_vote'] = delete_group_vote

        modify_group_vote = Decision.objects.filter(group_member=group_member, group=community)
        modify_group_vote = modify_group_vote[0].modify_group_vote
        context['modify_group_vote'] = modify_group_vote

        return context
