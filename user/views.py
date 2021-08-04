"""Manage user app views"""

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import User
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
        if request.method == 'POST':

            user_form = ChangeUserForm(
                request.POST, instance=self.request.user
            )
            address_form = AddressUserForm(
                request.POST,
                instance=self.request.user.address
            )

            if user_form.is_valid() and address_form.is_valid():
                user_form.save()
                address = address_form.save()
                user = User.objects.get(
                    email=request.POST['email']
                )
                # Add an address to group
                user.address = address
                user.save()

                messages.success(
                    request,
                    "Vos données ont été mise à jour"
                )
                return redirect('user:account')

            else:
                messages.error(
                    request,
                    "Une erreur est survenue, réessayez vos"
                    "modifications ou contactez un administrateur"
                )
                return render(
                    request,
                    'user/user_account.html',
                    {
                        'user_form': user_form,
                        'address_form': address_form
                    }
                )
