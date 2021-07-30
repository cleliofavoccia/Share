"""Views of product app"""

import datetime

from django.views.generic import DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

from point_provider.utils import update_communities_informations
from group.models import Group
from group_member.models import GroupMember
from collective_decision.models import Estimation

from .models import Product
from .forms import ProductInscriptionForm, CostEstimationForm, ProductSuppressionForm


class ProductDetailView(DetailView):
    """Generic class-based Product detail view to print all
    informations about a product"""

    model = Product

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        product = super().get_object()
        community = product.group

        try:
            group_member = GroupMember.objects.get(
                user=user,
                group=community
            )
            context['member'] = group_member
        except GroupMember.DoesNotExist:
            pass
        except TypeError:
            pass

        group_products_list = Product.objects.filter(group=community)
        members_number = GroupMember.objects.filter(group=community).count()
        products_number = Product.objects.filter(group=community).count()

        # Calculate communities's products cost, total products cost,
        # points per community member
        update_communities_informations()

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

        return context


class MySuppliedProductsListView(LoginRequiredMixin, ListView):
    """Generic class-based Product list view to print all
    products the user has register in different communities"""

    model = Product
    template_name = 'product/supplied_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        groups = Group.objects.all()
        supplied_products = list()

        try:
            # Add all products provide by user in a context
            # to display it
            for group in groups:
                try:
                    current_user = GroupMember.objects.get(
                        user=user,
                        group=group
                    )

                    products = Product.objects.filter(
                        user_provider=current_user,
                        group=group
                    )

                    for product in products:
                        supplied_products.append(product)

                except GroupMember.DoesNotExist:
                    continue
                except Product.DoesNotExist:
                    continue

            context['supplied_products'] = supplied_products

        except ValueError:
            context['supplied_products'] = False

        return context


class MyRentedProductsListView(LoginRequiredMixin, ListView):
    """Generic class-based Product list view to print all
        products the user has rented in different communities"""

    model = Product
    template_name = 'product/rented_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        groups = Group.objects.all()
        rented_products = list()

        try:
            # Add all products provide by user in a context
            # to display it
            for group in groups:
                try:
                    current_user = GroupMember.objects.get(
                        user=user,
                        group=group
                    )
                    products = Product.objects.filter(
                        tenant=current_user,
                        group=group
                    )

                    for product in products:
                        rented_products.append(product)
                except GroupMember.DoesNotExist:
                    continue
                except Product.DoesNotExist:
                    continue

            context['rented_products'] = rented_products
        except ValueError:
            context['rented_products'] = False

        return context


class ProductInscriptionView(LoginRequiredMixin, View):
    """Generic class-based view that permit to user
    to add a Product object in a community (Group object)"""

    def get(self, request, pk):
        """Method GET to print user informations"""
        group = Group.objects.get(id=pk)
        group_member = GroupMember.objects.get(
            user=self.request.user,
            group=group
        )
        product_form = ProductInscriptionForm(request.POST)
        estimation_form = CostEstimationForm(request.POST)

        return render(request, 'product/product_inscription.html',
                      {
                          'product_form': product_form,
                          'estimation_form': estimation_form,
                          'group': group,
                          'group_member': group_member
                       },
                      )

    def post(self, request, pk):
        """Method POST to send datas input by user
        and modify a User object (user account)"""

        group = Group.objects.get(id=pk)
        group_member = GroupMember.objects.get(
            user=self.request.user,
            group=group
        )

        if request.method == 'POST':
            # create a form instance and
            # populate it with data from the request:
            product_form = ProductInscriptionForm(
                request.POST,
            )
            estimation_form = CostEstimationForm(
                request.POST,
            )
            # check whether it's valid:
            if product_form.is_valid() and estimation_form.is_valid():
                product = product_form.save(commit=False)
                product.group = group
                try:
                    if request.POST['group_member']:
                        product.user_provider = group_member
                except MultiValueDictKeyError:
                    product.group_provider = group

                product.save()

                estimation = estimation_form.save(commit=False)
                estimation.group_member = group_member
                estimation.product = product
                estimation.save()

                # Send an email to all community members
                community_members = GroupMember.objects.filter(group=group)

                for member in community_members:
                    subject = f'Voter pour le coût du nouveau produit : {product}'
                    html_message = render_to_string(
                        'collective_decision/estimation_mail.html',
                        {
                            'username': f'{member.user.username}',
                            'product': product,
                            'estimation_link': 'http://127.0.0.1:8000/collective_decision/estimation/' + str(product.pk)
                        }
                    )
                    plain_message = strip_tags(html_message)
                    from_email = 'favoccia.c@live.fr'
                    to = f'{member.user.email}'

                    send_mail(
                        subject,
                        plain_message,
                        from_email,
                        [to],
                        html_message=html_message
                    )

                # redirect to a new URL:
                return redirect('group:community', product.group.pk)
            else:
                return render(
                    request,
                    'product/product_inscription.html',
                    {
                        'product_form': product_form,
                        'estimation_form': estimation_form,
                        'group': group,
                        'group_member': group_member
                    }
                    )


class ProductChangeView(LoginRequiredMixin, View):
    """Generic class-based view that permit to user
    to modify a Product object in a community (Group object)"""

    def get(self, request, pk, id):
        """Method GET to print user informations"""
        group = Group.objects.get(id=pk)
        print(group)
        group_member = GroupMember.objects.get(
            user=self.request.user,
            group=group
        )
        product = Product.objects.get(id=id)
        print(product)

        estimation = Estimation.objects.get(
            group_member=group_member,
            product=product
        )

        product_form = ProductInscriptionForm(
            instance=product,
        )
        estimation_form = CostEstimationForm(
            instance=estimation,
        )

        return render(request, 'product/product_modification.html',
                      {
                          'product_form': product_form,
                          'estimation_form': estimation_form,
                          'group': group,
                          'group_member': group_member
                      },
                      )

    def post(self, request, pk, id):
        """Method POST to send datas input by user
        and modify a User object (user account)"""

        group = Group.objects.get(id=pk)
        group_member = GroupMember.objects.get(
            user=self.request.user,
            group=group
        )

        product = Product.objects.get(id=id)

        estimation = Estimation.objects.get(
            group_member=group_member,
            product=product
        )

        if request.method == 'POST':
            # create a form instance and
            # populate it with data from the request:
            product_form = ProductInscriptionForm(
                request.POST,
                instance=product
            )
            estimation_form = CostEstimationForm(
                request.POST,
                instance=estimation
            )
            # check whether it's valid:
            if product_form.is_valid() and estimation_form.is_valid():
                product = product_form.save(commit=False)
                product.group = group
                try:
                    if request.POST['group_member']:
                        product.user_provider = group_member
                except MultiValueDictKeyError:
                    product.group_provider = group

                product.save()

                estimation = estimation_form.save(commit=False)
                estimation.group_member = group_member
                estimation.product = product
                estimation.save()

                # Send an email to all community members
                community_members = GroupMember.objects.filter(group=group)

                for member in community_members:
                    subject = f'Voter pour le coût du produit modifié : {product}'
                    html_message = render_to_string(
                        'collective_decision/estimation_mail.html',
                        {
                            'username': f'{member.user.username}',
                            'product': product,
                            'modify': True
                        }
                    )
                    plain_message = strip_tags(html_message)
                    from_email = 'favoccia.c@live.fr'
                    to = f'{member.user.email}'

                    send_mail(
                        subject,
                        plain_message,
                        from_email,
                        [to],
                        html_message=html_message
                    )

                # redirect to a new URL:
                return redirect('group:community', product.group.pk)
            else:
                return render(request, 'product/product_modification.html',
                              {'product_form': product_form,
                               'estimation_form': estimation_form,
                               'group': group,
                               'group_member': group_member
                               }
                              )


class ProductSuppressionView(LoginRequiredMixin, View):
    """Generic class-based view that permit to user
    to delete a Product object in a community (Group object)"""

    def post(self, request):
        """Method POST to send datas input by user
        and modify a User object (user account)"""

        if request.method == 'POST':
            # create a form instance and
            # populate it with data from the request:
            form = ProductSuppressionForm(
                request.POST,
            )

            # check whether it's valid:
            if form.is_valid():
                form.delete()
                return redirect('group:community', request.POST['group'])
            return redirect('website:fail')


def do_delivery(request):
    """Assign rental end date of product"""

    product = Product.objects.get(id=int(request.POST['product']))

    today = timezone.now()

    duration = datetime.timedelta(days=product.points)

    product.rental_end = (today + duration)

    product.delivered = True
    product.save()

    return redirect('product:product', product.pk)


