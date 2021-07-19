"""Views of group_member app"""

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from .forms import GroupMemberInscriptionForm


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
