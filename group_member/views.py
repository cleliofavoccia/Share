"""Views of group_member app"""

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models.deletion import ProtectedError

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
            messages.success(request, "Bienvenue dans la communauté :) !")
            return redirect('group:community', request.POST['group'])

        messages.error(
            request,
            "Une erreur est survenue, réessayez de vous inscrire"
            "à la communauté ou contactez un adminsitrateur"
        )
        return redirect('group:community', request.POST['group'])


class GroupMemberUnsubscribe(LoginRequiredMixin, View):
    """Generic class-based view to delete GroupMember objects,
    to user community unsubscribe"""

    def post(self, request):
        """Method POST data to GroupMemberInscriptionForm
        and call delete form class method"""
        form = GroupMemberInscriptionForm(request.POST)
        if form.is_valid():
            try:
                form.delete(request.user)
                messages.success(request, "Vous avez quitté la communauté :(")
            except ProtectedError:
                messages.error(request,
                               "Une erreur est survenue, vous ne pouvez pas"
                               " partir de la communauté tant qu'un de "
                               "vos produits est loué ou tant que "
                               "vous louez un des produits de la "
                               "communauté"
                               )
                return redirect('group:community', request.POST['group'])
            return redirect('group:community', request.POST['group'])

        messages.error(
            request,
            "Une erreur est survenue, réessayez de partir"
            "de la communauté ou contactez un adminsitrateur"
        )
        return redirect('group:community', request.POST['group'])


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
        # In case of an error in POST datas
        except ValueError:

            # In case of group_member is invalid
            try:
                product = Product.objects.get(
                    id=request.POST['product']
                )
                messages.error(
                    request,
                    "Vous n'êtes pas inscrit à la communauté"
                )
                return redirect('product:product', request.POST['product'])

            # In case of product is invalid
            except ValueError:
                messages.error(request, "Le produit n'existe pas")
                return redirect('product:product', request.POST['product'])

            except Product.DoesNotExist:
                messages.error(request, "Le produit n'existe pas")
                return redirect('product:product', request.POST['product'])

        # In case of a group_member not exist
        except GroupMember.DoesNotExist:
            messages.error(request, "Vous n'êtes pas inscrit à la communauté")
            return redirect('product:product', request.POST['product'])

        if product.points <= group_member.points_posseded:
            form = GroupMemberRentalForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produit loué !')
                return redirect('product:product', request.POST['product'])

            messages.error(
                request,
                'Une erreur est survenue, réessayez de louer '
                'un produit ou contactez un administrateur'
            )
            return redirect('website:fail')
        else:
            messages.error(request, 'Pas assez de points !')
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
            messages.success(request, "Vous avez bien annulé la location")
            return redirect('product:product', request.POST['product'])

        messages.error(
            request,
            "Une erreur est survenue, réessayez d'annuler"
            "la location ou contactez un adminsitrateur"
        )
        return redirect('product:product', request.POST['product'])
