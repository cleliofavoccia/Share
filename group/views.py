from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from .models import Group
from product.models import Product
from group_member.models import GroupMember
from collective_decision.models import Estimation, Decision
from .forms import GroupInscriptionForm, ProductInscriptionForm, CostEstimationForm, AddressForm


class CommunityDetailView(DetailView):

    model = Group

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        community = super().get_object()

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
        # Save points per community member for each user
        community_members = GroupMember.objects.filter(group=community)
        for group_member in community_members:
            group_member.points_posseded = community.members_points
            group_member.save()

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

            # Create Decisions objects for group members who have made no decision
            for member in community_members:
                try:
                    Decision.objects.get(group=community, group_member=member)
                except Decision.DoesNotExist:
                    Decision.objects.create(group=community, group_member=member)

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


class GroupInscriptionView(LoginRequiredMixin, View):
    """View detailed user profile"""

    def get(self, request):
        """Method GET to print user informations"""
        group_form = GroupInscriptionForm(request.POST)
        address_form = AddressForm(request.POST)

        return render(request, 'group/group_inscription.html',
                      {'group_form': group_form,
                       'address_form': address_form},
                      )

    def post(self, request):
        """Method POST to send datas input by user
        and modify a User object (user account)"""
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and
            # populate it with data from the request:
            group_form = GroupInscriptionForm(request.POST)
            address_form = AddressForm(request.POST)
            # check whether it's valid:
            if group_form.is_valid() and address_form.is_valid():
                name = group_form.cleaned_data['name']
                image = group_form.cleaned_data['image']

                group_form.save()
                address_form.save()
                # redirect to a new URL:
                return redirect('website:index')
            else:
                return render(request, 'group/group_inscription.html',
                              {'product_form': group_form,
                               'address_form': address_form}
                              )


class ProductInscriptionView(LoginRequiredMixin, DetailView):
    """View detailed user profile"""
    model = Group

    # def get(self, request, pk):
    #     """Method GET to print user informations"""
        # product_form = ProductInscriptionForm(request.POST)
        # estimation_form = CostEstimationForm(request.POST)

        # return render(request, 'product/product_inscription.html',
        #               {'product_form': product_form,
        #                'estimation_form': estimation_form},
        #               )

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        product_form = ProductInscriptionForm(request.POST)
        estimation_form = CostEstimationForm(request.POST)

        context['product_form'] = product_form
        context['estimation_form'] = estimation_form

        return context

    def post(self, request):
        """Method POST to send datas input by user
        and modify a User object (user account)"""
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and
            # populate it with data from the request:
            product_form = ProductInscriptionForm(request.POST, instance=self.request.user)
            estimation_form = CostEstimationForm(request.POST, instance=self.request.user)
            # check whether it's valid:
            if product_form.is_valid() and estimation_form.is_valid():
                product_form.save()
                estimation_form.save()
                # redirect to a new URL:
                return redirect('website:index')
            else:
                return render(request, 'product/product_inscription.html',
                              {'product_form': product_form,
                               'estimation_form': estimation_form}
                              )
