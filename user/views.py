"""Manage views of user app"""

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ChangeUserForm, AddressUserForm


class UserDetailView(LoginRequiredMixin, View):
    """Generic class-based view to see and modify user profile
    (User object)"""

    def get(self, request):
        """Method GET to print user informations"""

        user_form = ChangeUserForm(
            instance=self.request.user
        )
        address_form = AddressUserForm(
            instance=self.request.user.address
        )

        return render(request, 'user/user_account.html',
                      {'user_form': user_form,
                       'address_form': address_form}
                      )

    def post(self, request):
        """Method POST to send datas input by user
        and modify a User object (user account)"""
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and
            # populate it with data from the request:
            user_form = ChangeUserForm(
                request.POST, instance=self.request.user
            )
            address_form = AddressUserForm(
                request.POST,
                instance=self.request.user.address
            )
            # check whether it's valid:
            if user_form.is_valid() and address_form.is_valid():
                user_form.save()
                address_form.save()

                # redirect to a new URL:
                return redirect('user:account')
            else:
                return render(
                    request,
                    'user/user_account.html',
                    {
                        'user_form': user_form,
                        'address_form': address_form
                    }
                )
