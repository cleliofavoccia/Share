"""Manage website's app urls"""

from django.urls import path

from .views import *

app_name = 'website'
urlpatterns = [
    path('fail/', FailView.as_view(), name='fail'),
    path('about/', AboutView.as_view(), name='about'),

    ]
