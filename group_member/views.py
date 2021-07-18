"""Views of favorites app"""
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from .forms import GroupMemberInscriptionForm
from .models import GroupMember


class GroupMemberInscription(LoginRequiredMixin, generic.View):
    """Generic class-based view to add Favorite objects in
    database"""

    def post(self, request):
        """Method POST data to FavoriteForm"""
        form = GroupMemberInscriptionForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('group_member:well_done')
        return redirect('group_member:fail')


class GroupMemberDesinscription(LoginRequiredMixin, generic.View):
    """Generic class-based view to add Favorite objects in
    database"""

    def post(self, request):
        """Method POST data to FavoriteForm"""
        form = GroupMemberInscriptionForm(request.POST)
        if form.is_valid():
            form.delete(request.user)
            return redirect('group_member:well_done')
        return redirect('group_member:fail')


class WellDoneView(LoginRequiredMixin, generic.View):
    """View to print favorite well added to database"""

    def get(self, request):
        """Method GET to print well done message"""
        context = {'msg_welldone': 'Félicitations ! Vous faîtes parti de la communauté !'}

        return render(request, 'group_member/well_done.html', context)


class FailView(LoginRequiredMixin, generic.View):
    """View listing to print favorite not added to database"""

    def get(self, request):
        """Method GET to print fail message"""
        context = {'msg_fail': 'Oups ! Il a dû se produire une erreur. Contactez le gérant du site'}

        return render(request, 'group_member/fail.html', context)
