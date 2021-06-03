
from django.views.generic.base import TemplateView


class Dashboard(TemplateView):

    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Example(TemplateView):

    template_name = 'dashboard/example.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


