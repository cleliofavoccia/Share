from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Product
from group.models import Group
from group_member.models import GroupMember
from collective_decision.models import Estimation


class ProductDetailView(DetailView):

    model = Product

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        product = super().get_object()
        # Calculate product price
        cost_estimations = Estimation.objects.filter(product=product)
        estimation_numbers = cost_estimations.count()
        sum_product_cost = 0
        for estimation in cost_estimations:
            sum_product_cost += estimation.cost
        product.points = sum_product_cost // estimation_numbers
        product.save()

        context['group_products_list'] = Product.objects.filter(group=product.group)
        context['members_number'] = GroupMember.objects.filter(group=product.group).count()
        context['products_number'] = Product.objects.filter(group=product.group).count()

        if user.is_authenticated:
            current_group_member = GroupMember.objects.filter(user=user).filter(group=product.group)
            try:
                context['current_group_member_points'] = current_group_member[0].points_posseded
            except IndexError:
                pass
        else:
            current_group_member = None

        return context


class MySuppliedProductsListView(LoginRequiredMixin, ListView):

    model = Product
    template_name = 'product/supplied_products.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        current_user = GroupMember.objects.filter(user=user)
        context = super().get_context_data(**kwargs)
        supplied_products = Product.objects.filter(user_provider=current_user)

        context['supplied_products'] = supplied_products
        return context


class MyRentedProductsListView(LoginRequiredMixin, ListView):

    model = Product
    template_name = 'product/rented_products.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        current_user = GroupMember.objects.filter(user=user)
        context = super().get_context_data(**kwargs)
        rented_products = Product.objects.filter(tenant=current_user)

        context['rented_products'] = rented_products
        return context
