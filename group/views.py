"""Views of group app"""

from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages

from group.utils import update_communities_informations
from product.models import Product
from group_member.models import GroupMember
from collective_decision.models import Decision

from .models import Group
from .forms import GroupInscriptionForm, AddressForm


class CommunityDetailView(DetailView):
    """Generic class-based Group detail view to print all
    informations about a community and all actions the
    user can do with it"""

    model = Group

    def get_context_data(self, **kwargs):
        """Method that return an enriched context
        to template"""

        # Calculate communities's products cost, total products cost,
        # points per community member
        update_communities_informations()

        user = self.request.user
        context = super().get_context_data(**kwargs)
        community = super().get_object()

        group_products_list = Product.objects.filter(group=community)
        members_number = GroupMember.objects.filter(group=community).count()
        products_number = Product.objects.filter(group=community).count()
        community_members = GroupMember.objects.filter(
            group=community
        )

        context['group_products_list'] = group_products_list
        context['members_number'] = members_number
        context['products_number'] = products_number

        if user.is_authenticated:
            group_member_list = list()
            group_member = GroupMember.objects.filter(user=user)

            # Add communities in which user has suscribed in a list
            # that added to context to verify if user is in a displayed
            # community
            for community_inscription in group_member:
                group_member_list.append(community_inscription.group.name)
            context['group_member_list'] = group_member_list

            # Create Decisions objects for group members
            # who have made no decision
            for member in community_members:
                try:
                    Decision.objects.get(
                        group=community, group_member=member
                    )
                except Decision.DoesNotExist:
                    Decision.objects.create(
                        group=community, group_member=member
                    )

            community_member = GroupMember.objects.filter(
                user=user, group=community
            )
            # Fetch the User votes
            if community_member:
                group_member = GroupMember.objects.filter(
                    user=user, group=community
                )[0]
                context['group_member'] = group_member
                delete_group_vote = Decision.objects.filter(
                    group_member=group_member, group=community
                )
                delete_group_vote = delete_group_vote[0].delete_group_vote
                context['delete_group_vote'] = delete_group_vote

                modify_group_vote = Decision.objects.filter(
                    group_member=group_member, group=community
                )
                modify_group_vote = modify_group_vote[0].modify_group_vote
                context['modify_group_vote'] = modify_group_vote

        return context


class GroupInscriptionView(LoginRequiredMixin, View):
    """Generic class-based view that permit to user
    to add a community (Group object)"""

    def get(self, request):
        """Method GET to print all inputs that user
        must fill to add a community"""
        group_form = GroupInscriptionForm(request.POST)
        address_form = AddressForm(request.POST)

        return render(request, 'group/group_inscription.html',
                      {'group_form': group_form,
                       'address_form': address_form},
                      )

    def post(self, request):
        """Method POST to send datas input by user
        and register a Group object (community)"""
        if request.method == 'POST':

            group_form = GroupInscriptionForm(
                request.POST,
                request.FILES,
            )
            address_form = AddressForm(request.POST)

            if group_form.is_valid() and address_form.is_valid():
                group_form.save()
                address = address_form.save()
                group = Group.objects.get(
                    name=request.POST['name']
                )
                # Add an address to group
                group.address = address
                group.save()

                # Atomatically add creator
                # as a group member
                GroupMember.objects.create(
                    user=request.user, group=group
                )
                messages.success(
                    request,
                    "Vous avez ajouté une nouvelle communauté !"
                )
                return redirect('group:community', group.pk)

            else:
                messages.error(
                    request,
                    "Une erreur est survenue, réessayez de remplir"
                    "le formulaire ou contactez un administrateur"
                )
                return render(request, 'group/group_inscription.html',
                              {'product_form': group_form,
                               'address_form': address_form}
                              )


class GroupChangeView(LoginRequiredMixin, View):
    """Generic class-based view that permit to group member
    to modify a community (Group object)"""

    def get(self, request, pk):
        """Method GET to print community informations"""
        group = Group.objects.get(id=pk)

        group_form = GroupInscriptionForm(
            instance=group
        )
        address_form = AddressForm(
            instance=group.address
        )

        return render(
            request, 'group/group_modification.html',
            {
                'group_form': group_form,
                'address_form': address_form
            }
        )

    def post(self, request, pk):
        """Method POST to send datas input by user
        and modify a User object (user account)"""
        group = Group.objects.get(id=pk)

        if request.method == 'POST':
            group_form = GroupInscriptionForm(
                request.POST,
                request.FILES,
                instance=group
            )
            address_form = AddressForm(
                request.POST,
                instance=group.address
            )

            if group_form.is_valid() and address_form.is_valid():
                group_form.save()
                address = address_form.save()
                group = Group.objects.get(
                    name=request.POST['name']
                )
                # Add an address to group
                group.address = address
                group.save()
                messages.success(
                    request,
                    "Vous avez bien modifié la communauté !"
                )
                return redirect('group:community', group.pk)

            else:
                messages.error(
                    request,
                    "Une erreur est survenue, réessayez de remplir"
                    "le formulaire ou contactez un administrateur"
                )
                return render(
                    request, 'group/group_modification.html',
                    {
                        'group_form': group_form,
                        'address_form': address_form
                    }
                )
