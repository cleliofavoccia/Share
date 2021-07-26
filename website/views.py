"""Manage views of website app"""

from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class AboutView(TemplateView):
    """View to print vote not changed"""

    template_name = "website/about.html"


class FailView(LoginRequiredMixin, View):
    """View to print vote not changed"""

    def get(self, request):
        """Method GET to print fail message"""
        context = {
            'msg_fail': "Oups ! Il a dû se produire une erreur. "
                        "Réessayer ou bien,"
                        "en cas de persistence du problème, "
                        "contactez l'administration"
                        "du site"
        }

        return render(request, 'website/fail.html', context)
