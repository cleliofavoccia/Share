
from django.views.generic.base import TemplateView
from group.models import Group
from product.models import Product


class Dashboard(TemplateView):

    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        products = Product.objects.all()
        first_community_in_list = groups[0]

        context['communities'] = groups
        context['community_products'] = products.filter(group=first_community_in_list)
        return context


class Example(TemplateView):

    template_name = 'dashboard/example.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


