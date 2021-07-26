"""Views of group_member app"""

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from product.models import Product

from .models import GroupMember
from .forms import GroupMemberInscriptionForm, GroupMemberRentalForm


class GroupMemberInscription(LoginRequiredMixin, View):
    """Generic class-based view to add GroupMember objects,
    to user community inscription"""

    def post(self, request):
        """Method POST data to GroupMemberInscriptionForm
        and call save form class method"""
        form = GroupMemberInscriptionForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('group:community', request.POST['group'])
        return redirect('website:fail')


class GroupMemberUnsubscribe(LoginRequiredMixin, View):
    """Generic class-based view to delete GroupMember objects,
    to user community unsubscribe"""

    def post(self, request):
        """Method POST data to GroupMemberInscriptionForm
        and call delete form class method"""
        form = GroupMemberInscriptionForm(request.POST)
        if form.is_valid():
            form.delete(request.user)
            return redirect('group:community', request.POST['group'])
        return redirect('website:fail')


class GroupMemberRental(LoginRequiredMixin, View):
    """Generic class-based view to permit
    community member (GroupMember objects),
    to rent products (Product object)"""

    def post(self, request):
        """Method POST data to GroupMemberRentalForm
        and call save form class method"""

        try:
            group_member = GroupMember.objects.get(
                id=int(request.POST['group_member'])
            )
            product = Product.objects.get(
                id=int(request.POST['product'])
            )
        # In case of a user has not suscribed to product
        # community
        except ValueError:

            product = Product.objects.get(
                id=int(request.POST['product'])
            )

            return redirect('group:community', product.group.id)

        if product.points <= group_member.points_posseded:
            form = GroupMemberRentalForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('product:product', request.POST['product'])
            return redirect('website:fail')
        else:
            return redirect('product:product', request.POST['product'])


class GroupMemberRentalAnnulation(LoginRequiredMixin, View):
    """Generic class-based view to permit
    community member (GroupMember objects),
    to cancel the products rental  (Product object)"""

    def post(self, request):
        """Method POST data to GroupMemberRentalForm
        and call save form class method"""
        form = GroupMemberRentalForm(request.POST)

        if form.is_valid():
            form.delete()
            return redirect('product:product', request.POST['product'])
        return redirect('website:fail')
