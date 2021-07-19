from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


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
